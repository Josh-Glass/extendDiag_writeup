"""A priori simulations: explore model behavior across parameter space.

For each model (DIVA, GCM), samples parameter space and generates
predictions to show the model's behavioral repertoire before seeing
human data.

Usage:
    python run_apriori.py --experiment exp3 --model diva --n_samples 500
    python run_apriori.py --experiment exp2 --model gcm --grid
"""

import numpy as np
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from modeling_utils import (
    load_experiment_config,
    prepare_stimuli_for_models,
    save_results
)
import diva
import gcm


# ============================================================================
# PARAMETER SPACE DEFINITIONS
# ============================================================================

DIVA_PARAM_SPACE = {
    'n_hid': [2, 3, 4, 5, 6, 8],
    'lr': [0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
    'wr': [0.5, 1.0, 1.5, 2.0],
    'beta': [0, 1, 2, 3, 5]
}

GCM_PARAM_SPACE = {
    'c': [0.5, 1, 2, 4, 6, 8, 10],
    'r': [1],  # City-block for separable dimensions
    'phi': [0.5, 1, 2, 4, 6, 8, 10],
    'w1': np.linspace(0.1, 0.9, 9),  # Attention to feature 1
    # w2 = 1 - w1 (attention weights sum to 1)
}


# ============================================================================
# PARAMETER SAMPLING
# ============================================================================

def sample_diva_params(n_samples, rng):
    """Random sampling from DIVA parameter space.
    
    Args:
        n_samples: number of parameter sets to sample
        rng: numpy random generator
    
    Returns:
        list of dicts, each containing one parameter set
    """
    samples = []
    for _ in range(n_samples):
        params = {
            'n_hid': rng.choice(DIVA_PARAM_SPACE['n_hid']),
            'lr': rng.choice(DIVA_PARAM_SPACE['lr']),
            'wr': rng.choice(DIVA_PARAM_SPACE['wr']),
            'beta': rng.choice(DIVA_PARAM_SPACE['beta'])
        }
        samples.append(params)
    return samples


def grid_gcm_params():
    """Full grid over GCM parameter space.
    
    Returns:
        list of dicts, each containing one parameter set
    """
    samples = []
    for c in GCM_PARAM_SPACE['c']:
        for phi in GCM_PARAM_SPACE['phi']:
            for w1 in GCM_PARAM_SPACE['w1']:
                params = {
                    'c': c,
                    'r': 1,  # Fixed city-block
                    'phi': phi,
                    'w1': w1,
                    'w2': 1 - w1
                }
                samples.append(params)
    return samples


# ============================================================================
# MODEL TRAINING AND TESTING
# ============================================================================

def train_diva(train_stimuli, train_labels, cfg, rng, n_epochs=32):
    """Train DIVA model.
    
    Args:
        train_stimuli: (n_train, n_features) array
        train_labels: (n_train,) array of category indices
        cfg: DIVA config dict
        rng: numpy random generator
        n_epochs: number of training epochs
    
    Returns:
        trained parameters dict
    """
    # Initialize model with correct number of features
    n_feat = train_stimuli.shape[1]
    iw, ow = diva.get_wts(n_feat, cfg['n_hid'], 2, rng, 
                          cfg['wr'], 0.0, cfg.get('init', 'uniform'))
    params = {'iw': iw, 'ow': ow}
    
    # Encode stimuli
    x_train = diva.encode(train_stimuli, cfg.get('coding', 'pm1'))
    
    # Training loop
    for epoch in range(n_epochs):
        order = rng.permutation(len(train_stimuli))
        for idx in order:
            diva.trial(params, x_train[idx], train_labels[idx], cfg)
    
    return params


def test_diva(params, test_stimuli, cfg):
    """Get DIVA predictions on test items.
    
    Args:
        params: trained DIVA parameters
        test_stimuli: (n_test, n_features) array
        cfg: DIVA config dict
    
    Returns:
        (n_test, 2) array of category probabilities
    """
    x_test = diva.encode(test_stimuli, cfg.get('coding', 'pm1'))
    probs = np.array([diva.response(params, x, cfg) for x in x_test])
    return probs


def test_gcm(train_stimuli, train_labels, test_stimuli, params):
    """Get GCM predictions on test items.
    
    Args:
        train_stimuli: (n_train, n_features) array (exemplars)
        train_labels: (n_train,) array of category indices
        test_stimuli: (n_test, n_features) array
        params: dict with c, r, phi, w1, w2
    
    Returns:
        (n_test, 2) array of category probabilities
    """
    # Build GCM params structure
    n_cat = 2
    exemplar_labels = np.eye(n_cat)[train_labels]
    
    gcm_params = gcm.build_params(train_stimuli.shape[1], exemplar_labels)
    gcm_params['attention_weights'] = np.array([[params['w1'], params['w2']]])
    
    # Get predictions
    probs = gcm.response(gcm_params, test_stimuli, train_stimuli,
                        params['c'], params['r'], params['phi'])
    
    return probs


# ============================================================================
# A PRIORI SIMULATION
# ============================================================================

def run_apriori_diva(experiment, n_samples=500, n_reps=10, seed=42):
    """Run a priori DIVA simulations.
    
    Args:
        experiment: 'exp2' or 'exp3'
        n_samples: number of parameter sets to sample
        n_reps: number of replications per parameter set (DIVA is stochastic)
        seed: random seed
    
    Returns:
        dict with results
    """
    rng = np.random.default_rng(seed)
    
    # Load experiment data
    config = load_experiment_config(experiment)
    stim_data = prepare_stimuli_for_models(experiment)
    
    # Sample parameters
    param_samples = sample_diva_params(n_samples, rng)
    
    # Run simulations
    results = []
    for param_set in tqdm(param_samples, desc="DIVA parameter sets"):
        # Merge with defaults
        cfg = {**diva.DEFAULTS, **param_set}
        
        # Run multiple replications
        rep_probs = []
        for rep in range(n_reps):
            params = train_diva(stim_data['train_stimuli'],
                              stim_data['train_labels'],
                              cfg, rng)
            probs = test_diva(params, stim_data['test_stimuli'], cfg)
            rep_probs.append(probs)
        
        # Average across replications
        avg_probs = np.mean(rep_probs, axis=0)
        
        # Store results
        for i, item_id in enumerate(stim_data['test_ids']):
            results.append({
                'item_id': item_id,
                'p_cat0': float(avg_probs[i, 0]),
                'p_cat1': float(avg_probs[i, 1]),
                **param_set
            })
    
    return {
        'model': 'diva',
        'n_samples': n_samples,
        'n_reps': n_reps,
        'seed': seed,
        'predictions': results
    }


def run_apriori_gcm(experiment, seed=42):
    """Run a priori GCM simulations (full grid).
    
    Args:
        experiment: 'exp2' or 'exp3'
        seed: random seed (for consistency, though GCM is deterministic)
    
    Returns:
        dict with results
    """
    # Load experiment data
    config = load_experiment_config(experiment)
    stim_data = prepare_stimuli_for_models(experiment)
    
    # Get all parameter combinations
    param_samples = grid_gcm_params()
    
    # Run simulations
    results = []
    for param_set in tqdm(param_samples, desc="GCM parameter sets"):
        probs = test_gcm(stim_data['train_stimuli'],
                        stim_data['train_labels'],
                        stim_data['test_stimuli'],
                        param_set)
        
        # Store results
        for i, item_id in enumerate(stim_data['test_ids']):
            results.append({
                'item_id': item_id,
                'p_cat0': float(probs[i, 0]),
                'p_cat1': float(probs[i, 1]),
                **param_set
            })
    
    return {
        'model': 'gcm',
        'n_samples': len(param_samples),
        'seed': seed,
        'predictions': results
    }


# ============================================================================
# VISUALIZATION
# ============================================================================

def visualize_apriori(results, experiment, output_dir):
    """Create visualization of a priori predictions.
    
    Args:
        results: dict from run_apriori_*
        experiment: 'exp2' or 'exp3'
        output_dir: where to save plots
    """
    import pandas as pd
    
    config = load_experiment_config(experiment)
    critical_items = config['critical_items']
    
    df = pd.DataFrame(results['predictions'])
    
    # For exp3: compute X - Y difference score
    if experiment == 'exp3':
        x_items = [i for i in critical_items if i.startswith('X')]
        y_items = [i for i in critical_items if i.startswith('Y')]
        
        # Get mean p(Alpha) for X and Y items per parameter set
        if results['model'] == 'diva':
            group_cols = ['n_hid', 'lr', 'wr', 'beta']
        else:
            group_cols = ['c', 'phi', 'w1']
        
        x_df = df[df['item_id'].isin(x_items)].groupby(group_cols)['p_cat0'].mean()
        y_df = df[df['item_id'].isin(y_items)].groupby(group_cols)['p_cat0'].mean()
        diff_scores = (x_df - y_df).reset_index(name='x_minus_y')
        
        # Plot distribution
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(diff_scores['x_minus_y'], bins=50, edgecolor='black', alpha=0.7)
        ax.axvline(0, color='red', linestyle='--', label='No difference')
        ax.set_xlabel('P(Alpha|X) - P(Alpha|Y)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{results["model"].upper()} A Priori: X vs Y Difference')
        ax.legend()
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path / f'apriori_{results["model"]}_xvsy.pdf', bbox_inches='tight')
        fig.savefig(output_path / f'apriori_{results["model"]}_xvsy.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    # For exp2: plot T3 and T4 separately
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        for ax, item in zip(axes, ['T3', 'T4']):
            item_df = df[df['item_id'] == item]
            ax.hist(item_df['p_cat0'], bins=50, edgecolor='black', alpha=0.7)
            ax.axvline(0.5, color='red', linestyle='--', label='Chance')
            ax.set_xlabel('P(Alpha)')
            ax.set_ylabel('Frequency')
            ax.set_title(f'{results["model"].upper()}: {item}')
            ax.legend()
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path / f'apriori_{results["model"]}_critical.pdf', bbox_inches='tight')
        fig.savefig(output_path / f'apriori_{results["model"]}_critical.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"Plots saved to: {output_dir}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Run a priori model simulations')
    parser.add_argument('--experiment', type=str, required=True,
                       choices=['exp2', 'exp3'],
                       help='Which experiment to simulate')
    parser.add_argument('--model', type=str, required=True,
                       choices=['diva', 'gcm'],
                       help='Which model to simulate')
    parser.add_argument('--n_samples', type=int, default=500,
                       help='Number of parameter sets (DIVA only)')
    parser.add_argument('--n_reps', type=int, default=10,
                       help='Replications per parameter set (DIVA only)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    parser.add_argument('--output_dir', type=str, default=None,
                       help='Output directory (default: {experiment}_data/modeling)')
    
    args = parser.parse_args()
    
    # Set output directory
    if args.output_dir is None:
        exp_dir = 'single_cat_diag_data' if args.experiment == 'exp3' else 'globloc_data'
        args.output_dir = f'{exp_dir}/modeling'
    
    # Run simulation
    print(f"\nRunning a priori {args.model.upper()} simulation for {args.experiment}...")
    
    if args.model == 'diva':
        results = run_apriori_diva(args.experiment, args.n_samples, 
                                  args.n_reps, args.seed)
    else:
        results = run_apriori_gcm(args.experiment, args.seed)
    
    # Save results
    save_results(results, args.experiment, args.output_dir,
                f'apriori_{args.model}')
    
    # Visualize
    visualize_apriori(results, args.experiment, args.output_dir)
    
    print("\nA priori simulation complete!")


if __name__ == '__main__':
    main()
