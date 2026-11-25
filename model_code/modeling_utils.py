"""Shared utilities for DIVA/GCM modeling across experiments.

Provides:
- Experiment configuration loading (stimuli, data paths, critical items)
- Human data loading and aggregation
- Stimulus preparation for models
- MSE calculation between model and human probabilities
- Standardized result saving
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime


# ============================================================================
# EXPERIMENT CONFIGURATIONS
# ============================================================================

def load_experiment_config(experiment):
    """Load experiment-specific configuration.
    
    Args:
        experiment: 'exp2' (globloc) or 'exp3' (single_cat_diag)
    
    Returns:
        dict with keys:
            - train_data_path: path to training data CSV
            - test_data_path: path to test data CSV
            - stimuli_coords: dict of numpy arrays for each item type
            - critical_items: list of item IDs to focus analysis on
            - n_features: number of stimulus features
            - n_categories: number of categories
            - category_labels: list of category names
    """
    if experiment == 'exp3':
        return {
            'train_data_path': 'single_cat_diag_data/condition_2_trainPhase.csv',
            'test_data_path': 'single_cat_diag_data/condition_2_testPhase.csv',
            'stimuli_coords': {
                # Training items (A: diagonal correlation, NotA: scattered)
                'A': np.array([
                    [.250, .050], [.325, .125], [.400, .200], 
                    [.475, .275], [.550, .350], [.625, .425], [.700, .500]
                ]),
                'NotA': np.array([
                    [.125, .625], [.200, .550], [.275, .475], [.350, .400],
                    [.600, .150], [.675, .075], [.750, .000]
                ]),
                # X items: on Alpha diagonal (critical for coherence)
                'X': np.array([
                    [.8, .7], [.9, .8], [1.0, .9],  # Diag 1 (closest, 3 items)
                    [.9, .7], [1.0, .8],            # Diag 2 (2 items)
                    [1.0, .7]                       # Diag 3 (corner, 1 item)
                ]),
                # Y items: parallel diagonal (control for correlation strength)
                'Y': np.array([
                    [.7, .8], [.8, .9], [.9, 1.0],  # Diag 1 (closest, 3 items)
                    [.7, .9], [.8, 1.0],            # Diag 2 (2 items)
                    [.7, 1.0]                       # Diag 3 (corner, 1 item)
                ])
            },
            'critical_items': ['X1', 'X2', 'X3', 'X4', 'X5', 'X6',
                             'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6'],
            'n_features': 2,
            'n_categories': 2,
            'category_labels': ['a', 'NotA']  # As used in data files
        }
    
    elif experiment == 'exp2':
        return {
            'train_data_path': 'globloc_data/trainPhase.csv',
            'test_data_path': 'globloc_data/testPhase.csv',
            'stimuli_coords': {
                # Training items (Alpha: diagonal, Beta: scattered)
                'Alpha': np.array([
                    [.2, .1], [.3, .2], [.4, .3],
                    [.5, .4], [.6, .5], [.7, .6]
                ]),
                'Beta': np.array([
                    [.3, .7], [.4, .6], [.5, .8],
                    [.6, .7], [.7, .8], [.8, .7]
                ]),
                # Critical test items
                'T3': np.array([[.8, .7]]),
                'T4': np.array([[.9, .8]])
            },
            'critical_items': ['T3', 'T4'],
            'n_features': 2,
            'n_categories': 2,
            'category_labels': ['Alpha', 'Beta']
        }
    
    else:
        raise ValueError(f"Unknown experiment: {experiment}. Use 'exp2' or 'exp3'.")


# ============================================================================
# HUMAN DATA LOADING
# ============================================================================

def load_human_data(experiment, phase='test', learning_criterion=None):
    """Load and aggregate human response data.
    
    Args:
        experiment: 'exp2' or 'exp3'
        phase: 'train' or 'test'
        learning_criterion: dict with 'min_correct' and 'total_items' for filtering
                          If None, loads all subjects
    
    Returns:
        dict mapping item_id -> {
            'p_cat0': probability of first category,
            'p_cat1': probability of second category,
            'n_subjects': number of subjects,
            'responses': list of individual responses (0 or 1)
        }
    """
    config = load_experiment_config(experiment)
    data_path = config['test_data_path'] if phase == 'test' else config['train_data_path']
    
    # Load data
    df = pd.read_csv(data_path)
    
    # Apply learning criterion if specified
    if learning_criterion is not None:
        # Calculate per-subject accuracy on trained items at test
        if phase == 'test':
            train_items = list(config['stimuli_coords']['A']) if experiment == 'exp3' else \
                         list(config['stimuli_coords']['Alpha'])
            
            # Get trained item IDs from config
            if experiment == 'exp3':
                trained_ids = [f'A{i+1}' for i in range(len(config['stimuli_coords']['A']))]
            else:
                trained_ids = [f'Alpha{i+1}' for i in range(len(config['stimuli_coords']['Alpha']))]
            
            # Filter to trained items only
            train_df = df[df['stimId'].isin(trained_ids)]
            
            # Calculate accuracy per subject
            subject_acc = train_df.groupby('subject_id')['accuracy'].mean()
            
            # Keep only subjects meeting criterion
            threshold = learning_criterion['min_correct'] / learning_criterion['total_items']
            passing_subjects = subject_acc[subject_acc >= threshold].index
            df = df[df['subject_id'].isin(passing_subjects)]
    
    # Aggregate responses by item
    results = {}
    for item_id in df['stimId'].unique():
        item_df = df[df['stimId'] == item_id]
        
        # Map responses to category indices (0 or 1)
        cat_labels = config['category_labels']
        responses = item_df['response'].map({cat_labels[0]: 0, cat_labels[1]: 1}).values
        
        results[item_id] = {
            'p_cat0': (responses == 0).mean(),
            'p_cat1': (responses == 1).mean(),
            'n_subjects': len(responses),
            'responses': responses.tolist()
        }
    
    return results


# ============================================================================
# STIMULUS PREPARATION FOR MODELS
# ============================================================================

def prepare_stimuli_for_models(experiment):
    """Convert stimulus coordinates to model-ready format.
    
    Args:
        experiment: 'exp2' or 'exp3'
    
    Returns:
        dict with keys:
            - train_stimuli: (n_train, n_features) array in [0,1]
            - train_labels: (n_train,) array of category indices
            - test_stimuli: (n_test, n_features) array in [0,1]
            - test_ids: list of item IDs for test stimuli
            - item_coords: dict mapping item_id -> coordinates
    """
    config = load_experiment_config(experiment)
    coords = config['stimuli_coords']
    
    # Prepare training data
    if experiment == 'exp3':
        train_a = coords['A']
        train_nota = coords['NotA']
        train_stimuli = np.vstack([train_a, train_nota])
        train_labels = np.array([0] * len(train_a) + [1] * len(train_nota))
        
        # Test stimuli: trained items + X + Y
        test_stimuli = np.vstack([train_a, train_nota, coords['X'], coords['Y']])
        test_ids = ([f'A{i+1}' for i in range(len(train_a))] +
                   [f'NotA{i+1}' for i in range(len(train_nota))] +
                   [f'X{i+1}' for i in range(len(coords['X']))] +
                   [f'Y{i+1}' for i in range(len(coords['Y']))])
        
    else:  # exp2
        train_alpha = coords['Alpha']
        train_beta = coords['Beta']
        train_stimuli = np.vstack([train_alpha, train_beta])
        train_labels = np.array([0] * len(train_alpha) + [1] * len(train_beta))
        
        # Test stimuli: trained items + T3 + T4
        test_stimuli = np.vstack([train_alpha, train_beta, coords['T3'], coords['T4']])
        test_ids = ([f'Alpha{i+1}' for i in range(len(train_alpha))] +
                   [f'Beta{i+1}' for i in range(len(train_beta))] +
                   ['T3', 'T4'])
    
    # Create item_id -> coordinates mapping
    item_coords = {item_id: test_stimuli[i] for i, item_id in enumerate(test_ids)}
    
    return {
        'train_stimuli': train_stimuli,
        'train_labels': train_labels,
        'test_stimuli': test_stimuli,
        'test_ids': test_ids,
        'item_coords': item_coords
    }


# ============================================================================
# MSE CALCULATION
# ============================================================================

def calculate_mse(model_probs, human_probs, items=None):
    """Calculate MSE between model and human response probabilities.
    
    Args:
        model_probs: dict mapping item_id -> [p_cat0, p_cat1]
        human_probs: dict mapping item_id -> {'p_cat0': float, 'p_cat1': float}
        items: list of item_ids to include (if None, use all common items)
    
    Returns:
        dict with keys:
            - mse: overall mean squared error
            - per_item_errors: dict mapping item_id -> squared error
            - n_items: number of items included
    """
    if items is None:
        items = list(set(model_probs.keys()) & set(human_probs.keys()))
    
    errors = {}
    for item_id in items:
        if item_id not in model_probs or item_id not in human_probs:
            continue
        
        # Get probabilities (use first category for comparison)
        model_p = model_probs[item_id][0]  # p(cat0)
        human_p = human_probs[item_id]['p_cat0']
        
        errors[item_id] = (model_p - human_p) ** 2
    
    mse = np.mean(list(errors.values())) if errors else np.nan
    
    return {
        'mse': float(mse),
        'per_item_errors': errors,
        'n_items': len(errors)
    }


# ============================================================================
# RESULT SAVING
# ============================================================================

def save_results(results, experiment, output_dir, filename):
    """Save results to JSON with metadata.
    
    Args:
        results: dict of results to save
        experiment: 'exp2' or 'exp3'
        output_dir: directory to save in (will be created if needed)
        filename: name of output file (without extension)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Add metadata
    output = {
        'metadata': {
            'experiment': experiment,
            'timestamp': datetime.now().isoformat(),
            'filename': filename
        },
        'results': results
    }
    
    # Save as JSON
    output_file = output_path / f"{filename}.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: {output_file}")
    
    return str(output_file)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_critical_item_mse(model_probs, human_probs, experiment):
    """Calculate MSE for critical items only.
    
    Args:
        model_probs: dict mapping item_id -> [p_cat0, p_cat1]
        human_probs: dict mapping item_id -> {'p_cat0': float, 'p_cat1': float}
        experiment: 'exp2' or 'exp3'
    
    Returns:
        dict with MSE for critical items
    """
    config = load_experiment_config(experiment)
    critical_items = config['critical_items']
    
    return calculate_mse(model_probs, human_probs, items=critical_items)


def format_parameter_string(params):
    """Format parameter dict as readable string for logging.
    
    Args:
        params: dict of parameter names -> values
    
    Returns:
        formatted string
    """
    return ', '.join([f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}" 
                     for k, v in params.items()])
