import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directories
os.makedirs('single_cat_diag_data/figures', exist_ok=True)
os.makedirs('single_cat_diag_data/writeup_textfiles', exist_ok=True)

# ==========================================
# 0. APPLY LEARNING CRITERION BASED ON TEST PERFORMANCE
# ==========================================
# Load test data for both conditions
df_test_cond1 = pd.read_csv('single_cat_diag_data/condition_1_testPhase.csv')
df_test_cond2 = pd.read_csv('single_cat_diag_data/condition_2_testPhase.csv')

# Define trained items (labels 'a' for both conditions)
# Calculate accuracy on trained items only
# Using 5/7 = 71.4% criterion to match Exp 1's 6/8 = 75% criterion (allowing 2 errors)
LEARNING_CRITERION = 5/7  # 71.4% accuracy on trained items (allowing 2 errors, consistent with Exp 1)

def get_learners(df_test, threshold=LEARNING_CRITERION):
    """
    Returns list of subject IDs who achieved >= threshold accuracy on trained items
    
    Parameters:
    -----------
    df_test : DataFrame
        Test phase data with columns: subject_id, category, response, accuracy
    threshold : float
        Minimum proportion correct on trained items (default: 6/7 = 0.857)
    
    Returns:
    --------
    learners : list
        Subject IDs meeting criterion
    subject_accuracy : Series
        Accuracy on trained items for all subjects
    """
    # Filter to only trained items (category 'a')
    trained_items = df_test[df_test['category'] == 'a'].copy()
    
    # Verify we have the expected number of trained items per subject
    items_per_subject = trained_items.groupby('subject_id').size()
    expected_items = 7  # Should be 7 trained Alpha items
    
    if not all(items_per_subject == expected_items):
        print(f"WARNING: Not all subjects have {expected_items} trained items!")
        print(f"Items per subject range: {items_per_subject.min()} to {items_per_subject.max()}")
    
    # Calculate accuracy per subject on trained items
    # Use the 'accuracy' column if it exists, otherwise compute from response
    if 'accuracy' in trained_items.columns:
        subject_accuracy = trained_items.groupby('subject_id')['accuracy'].mean()
    else:
        trained_items['correct'] = (trained_items['response'] == 'a').astype(float)
        subject_accuracy = trained_items.groupby('subject_id')['correct'].mean()
    
    # Filter subjects meeting criterion
    learners = subject_accuracy[subject_accuracy >= threshold].index.tolist()
    
    return learners, subject_accuracy

# Get learners for each condition
learners_cond1, acc_cond1 = get_learners(df_test_cond1, threshold=LEARNING_CRITERION)
learners_cond2, acc_cond2 = get_learners(df_test_cond2, threshold=LEARNING_CRITERION)

print(f"\n{'='*60}")
print(f"LEARNING CRITERION: {LEARNING_CRITERION:.1%} ({int(LEARNING_CRITERION*7)}/7 correct on trained items)")
print(f"{'='*60}")
print(f"\nCondition 1 (Generative Study):")
print(f"  Total subjects: {len(acc_cond1)}")
print(f"  Met criterion: {len(learners_cond1)} ({len(learners_cond1)/len(acc_cond1)*100:.1f}%)")
print(f"  Excluded: {len(acc_cond1) - len(learners_cond1)}")
print(f"  Mean accuracy on trained items (all subjects): {acc_cond1.mean():.3f} (SD={acc_cond1.std():.3f})")
print(f"  Mean accuracy on trained items (learners only): {acc_cond1[learners_cond1].mean():.3f} (SD={acc_cond1[learners_cond1].std():.3f})")

print(f"\nCondition 2 (Classification):")
print(f"  Total subjects: {len(acc_cond2)}")
print(f"  Met criterion: {len(learners_cond2)} ({len(learners_cond2)/len(acc_cond2)*100:.1f}%)")
print(f"  Excluded: {len(acc_cond2) - len(learners_cond2)}")
print(f"  Mean accuracy on trained items (all subjects): {acc_cond2.mean():.3f} (SD={acc_cond2.std():.3f})")
print(f"  Mean accuracy on trained items (learners only): {acc_cond2[learners_cond2].mean():.3f} (SD={acc_cond2[learners_cond2].std():.3f})")

# ==========================================
# 1. LOAD DATA & FILTER TO LEARNERS ONLY
# ==========================================
df_cond1 = pd.read_csv('single_cat_diag_data/condition_1_study.csv')
df_cond2 = pd.read_csv('single_cat_diag_data/condition_2_trainPhase.csv')

# Store original counts before filtering
n_cond1_original = df_cond1['subject_id'].nunique()
n_cond2_original = df_cond2['subject_id'].nunique()

# Filter to learners only
df_cond1 = df_cond1[df_cond1['subject_id'].isin(learners_cond1)]
df_cond2 = df_cond2[df_cond2['subject_id'].isin(learners_cond2)]

n_cond1 = len(learners_cond1)
n_cond2 = len(learners_cond2)

print(f"\n{'='*60}")
print(f"TRAINING DATA LOADED")
print(f"{'='*60}")
print(f"Condition 1: {n_cond1} learners (from {n_cond1_original} total)")
print(f"Condition 2: {n_cond2} learners (from {n_cond2_original} total)")

# ==========================================
# 2. GENERATIVE STUDY ANALYSIS (CONDITION 1)
# ==========================================
# Ensure relevant columns are numeric
cols_cond1 = ['aimedTargetSize', 'chosenSize', 'aimedTargetShade', 'chosenShade', 'rt', 'trial']
for col in cols_cond1:
    df_cond1[col] = pd.to_numeric(df_cond1[col], errors='coerce')

# Calculate Euclidean distance (error)
df_cond1['error_distance'] = np.sqrt(
    (df_cond1['aimedTargetSize'] - df_cond1['chosenSize'])**2 + 
    (df_cond1['aimedTargetShade'] - df_cond1['chosenShade'])**2
)

# Aggregate data per subject per trial
trial_agg = df_cond1.groupby(['subject_id', 'trial']).agg(
    mean_error=('error_distance', 'mean'),
    mean_rt=('rt', 'mean'),
    num_attempts=('rt', 'count')
).reset_index()

# Relabel trials to start from 1
trial_agg['trial'] = trial_agg['trial'] + 1

# Plot Generative Study Data
sns.set_theme(style="whitegrid")
fig1, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# Plot 1: Average Error
sns.lineplot(data=trial_agg, x='trial', y='mean_error', marker='o', 
             color='#d9534f', linewidth=2.5, markersize=8, ax=axes[0])
axes[0].set_title('Average Error Distance per Trial', fontsize=14)
axes[0].set_xlabel('Trial Number', fontsize=12)
axes[0].set_ylabel('Mean Euclidean Error', fontsize=12)

# Plot 2: Average RT
sns.lineplot(data=trial_agg, x='trial', y='mean_rt', marker='o', 
             color='#f0ad4e', linewidth=2.5, markersize=8, ax=axes[1])
axes[1].set_title('Average Reaction Time per Trial', fontsize=14)
axes[1].set_xlabel('Trial Number', fontsize=12)
axes[1].set_ylabel('Mean Reaction Time (ms)', fontsize=12)

# Plot 3: Number of Attempts
sns.lineplot(data=trial_agg, x='trial', y='num_attempts', marker='o', 
             color='#5bc0de', linewidth=2.5, markersize=8, ax=axes[2])
axes[2].set_title('Number of Attempts per Trial', fontsize=14)
axes[2].set_xlabel('Trial Number', fontsize=12)
axes[2].set_ylabel('Average Attempts until Correct', fontsize=12)

# Set integer x-ticks for all subplots
for ax in axes:
    max_trial = int(trial_agg['trial'].max())
    ax.set_xticks(range(1, max_trial + 1))

plt.tight_layout()
plt.savefig('single_cat_diag_data/figures/generative_training_analysis.png', bbox_inches='tight', dpi=300)
plt.savefig('single_cat_diag_data/figures/generative_training_analysis.pdf', bbox_inches='tight')
print(f"Saved generative_training_analysis.png and .pdf (n={n_cond1})")

# Save figure caption
caption_gen = """Figure: Generative Study Training Performance
Shows learning curves across 7 training trials for subjects who met the learning criterion.
Left panel: Mean Euclidean error distance between target and created stimuli.
Middle panel: Mean reaction time per trial.
Right panel: Mean number of attempts required to match target within tolerance threshold.
Error bars represent standard error of the mean."""

with open('single_cat_diag_data/writeup_textfiles/generative_training_analysis_caption.txt', 'w') as f:
    f.write(caption_gen)

# ==========================================
# 3. CLASSIFICATION TRAINING (CONDITION 2)
# ==========================================
# Format accuracy as numeric (1.0 for True, 0.0 for False)
df_cond2['accuracy'] = df_cond2['accuracy'].astype(float)

# Verify data structure matches expected format from project notes
print(f"\n{'='*60}")
print(f"CONDITION 2 DATA VERIFICATION")
print(f"{'='*60}")
print(f"Columns: {df_cond2.columns.tolist()}")
print(f"Unique blocks: {sorted(df_cond2['block'].unique())}")
print(f"Trials per block per subject: {df_cond2.groupby(['subject_id', 'block']).size().unique()}")
print(f"Sample of data structure:")
print(df_cond2[['trial', 'block', 'stimId', 'category', 'response', 'accuracy', 'subject_id']].head(10))

# ---- Fill forward for early finishers ----
# Find the last block each subject completed
last_block_per_subject = df_cond2.groupby('subject_id')['block'].max()

# Determine the maximum possible blocks (should be 8 based on design, 0-indexed so max is 7)
max_blocks = 7

# Track how many subjects finished early
early_finishers = (last_block_per_subject < max_blocks).sum()
print(f"\nSubjects who finished early: {early_finishers}/{len(last_block_per_subject)}")

# For each subject who finished early, fill forward their final accuracy
filled_rows = []
for subject_id, last_block in last_block_per_subject.items():
    if last_block < max_blocks:
        # Get their final block's accuracy
        final_block_data = df_cond2[(df_cond2['subject_id'] == subject_id) & 
                                     (df_cond2['block'] == last_block)]
        final_accuracy = final_block_data['accuracy'].mean()
        
        # Create rows for missing blocks, assuming they maintained criterion performance
        # Use 1.0 (perfect accuracy) as they met criterion to advance early
        for missing_block in range(int(last_block) + 1, max_blocks + 1):
            filled_rows.append({
                'subject_id': subject_id,
                'block': missing_block,
                'accuracy': 1.0  # Assume criterion performance maintained
            })

# Append filled rows to the dataframe
if filled_rows:
    df_filled = pd.DataFrame(filled_rows)
    df_cond2_complete = pd.concat([df_cond2, df_filled], ignore_index=True)
    print(f"Added {len(filled_rows)} filled rows for early finishers")
else:
    df_cond2_complete = df_cond2.copy()
    print("No early finishers to fill forward")

# Aggregate accuracy by subject and block (now with filled data)
learning_cond2 = df_cond2_complete.groupby(['subject_id', 'block'])['accuracy'].mean().reset_index()

# Relabel blocks to start from 1 for plotting
learning_cond2['block'] = learning_cond2['block'] + 1

# Plot Classification Training Data
fig2 = plt.figure(figsize=(8, 6))

sns.lineplot(data=learning_cond2, x='block', y='accuracy', marker='o', 
             color='#007bff', linewidth=2.5, markersize=8)
plt.xlabel('Training Block', fontsize=14)
plt.ylabel('Mean Accuracy', fontsize=14)
plt.ylim(-0.05, 1.05)
max_block = int(learning_cond2['block'].max())
plt.xticks(range(1, max_block + 1))

plt.tight_layout()
plt.savefig('single_cat_diag_data/figures/classification_training_analysis.png', bbox_inches='tight', dpi=300)
plt.savefig('single_cat_diag_data/figures/classification_training_analysis.pdf', bbox_inches='tight')
print(f"Saved classification_training_analysis.png and .pdf (n={n_cond2})")

# Save figure caption
caption_class = """Figure: Classification Training Performance
Shows learning curves across 8 training blocks for subjects who met the learning criterion.
Mean accuracy on Alpha vs Not Alpha classification with corrective feedback.
For subjects who finished early by achieving perfect accuracy, remaining blocks are imputed
as maintaining criterion-level performance (accuracy = 1.0).
Error bars represent standard error of the mean."""

with open('single_cat_diag_data/writeup_textfiles/classification_training_analysis_caption.txt', 'w') as f:
    f.write(caption_class)

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}")
print("\nGenerated files:")
print("  - learning_statistics.txt (comprehensive statistics)")
print("  - condition_1_learners.csv (subject IDs)")
print("  - condition_2_learners.csv (subject IDs)")
print("  - generative_training_analysis.png/.pdf")
print("  - generative_training_analysis_caption.txt")
print("  - classification_training_analysis.png/.pdf")
print("  - classification_training_analysis_caption.txt")

# ==========================================
# 4. SAVE COMPREHENSIVE STATISTICS TO TEXT FILES
# ==========================================

# Create comprehensive statistics report
stats_output = []
stats_output.append("="*80)
stats_output.append("EXPERIMENT 3: LEARNING PHASE STATISTICS")
stats_output.append("="*80)
stats_output.append("")
stats_output.append(f"Learning Criterion: {LEARNING_CRITERION:.1%} ({int(LEARNING_CRITERION*7)}/7 correct on trained items at test)")
stats_output.append("")

# Condition 1 Statistics
stats_output.append("-"*80)
stats_output.append("CONDITION 1: GENERATIVE STUDY")
stats_output.append("-"*80)
stats_output.append(f"Total subjects recruited: {n_cond1_original}")
stats_output.append(f"Subjects meeting criterion: {n_cond1} ({n_cond1/n_cond1_original*100:.1f}%)")
stats_output.append(f"Subjects excluded: {n_cond1_original - n_cond1}")
stats_output.append("")
stats_output.append("Test Phase Performance on Trained Items:")
stats_output.append(f"  All subjects - Mean: {acc_cond1.mean():.3f}, SD: {acc_cond1.std():.3f}")
stats_output.append(f"  All subjects - Range: {acc_cond1.min():.3f} to {acc_cond1.max():.3f}")
stats_output.append(f"  Learners only - Mean: {acc_cond1[learners_cond1].mean():.3f}, SD: {acc_cond1[learners_cond1].std():.3f}")
stats_output.append(f"  Learners only - Range: {acc_cond1[learners_cond1].min():.3f} to {acc_cond1[learners_cond1].max():.3f}")
stats_output.append("")

# Training phase statistics for Condition 1
if len(trial_agg) > 0:
    stats_output.append("Training Phase Performance (Generative Study):")
    stats_output.append(f"  Mean error distance - First trial: {trial_agg[trial_agg['trial']==1]['mean_error'].mean():.3f}")
    stats_output.append(f"  Mean error distance - Last trial: {trial_agg[trial_agg['trial']==trial_agg['trial'].max()]['mean_error'].mean():.3f}")
    stats_output.append(f"  Mean RT - First trial: {trial_agg[trial_agg['trial']==1]['mean_rt'].mean():.1f} ms")
    stats_output.append(f"  Mean RT - Last trial: {trial_agg[trial_agg['trial']==trial_agg['trial'].max()]['mean_rt'].mean():.1f} ms")
    stats_output.append(f"  Mean attempts - First trial: {trial_agg[trial_agg['trial']==1]['num_attempts'].mean():.2f}")
    stats_output.append(f"  Mean attempts - Last trial: {trial_agg[trial_agg['trial']==trial_agg['trial'].max()]['num_attempts'].mean():.2f}")
stats_output.append("")

# Condition 2 Statistics
stats_output.append("-"*80)
stats_output.append("CONDITION 2: CLASSIFICATION")
stats_output.append("-"*80)
stats_output.append(f"Total subjects recruited: {n_cond2_original}")
stats_output.append(f"Subjects meeting criterion: {n_cond2} ({n_cond2/n_cond2_original*100:.1f}%)")
stats_output.append(f"Subjects excluded: {n_cond2_original - n_cond2}")
stats_output.append("")
stats_output.append("Test Phase Performance on Trained Items:")
stats_output.append(f"  All subjects - Mean: {acc_cond2.mean():.3f}, SD: {acc_cond2.std():.3f}")
stats_output.append(f"  All subjects - Range: {acc_cond2.min():.3f} to {acc_cond2.max():.3f}")
stats_output.append(f"  Learners only - Mean: {acc_cond2[learners_cond2].mean():.3f}, SD: {acc_cond2[learners_cond2].std():.3f}")
stats_output.append(f"  Learners only - Range: {acc_cond2[learners_cond2].min():.3f} to {acc_cond2[learners_cond2].max():.3f}")
stats_output.append("")

# Training phase statistics for Condition 2
if len(learning_cond2) > 0:
    stats_output.append("Training Phase Performance (Classification):")
    block_means = learning_cond2.groupby('block')['accuracy'].mean()
    stats_output.append(f"  Mean accuracy - Block 1: {block_means.iloc[0]:.3f}")
    stats_output.append(f"  Mean accuracy - Block {len(block_means)}: {block_means.iloc[-1]:.3f}")
    stats_output.append(f"  Subjects who finished early: {early_finishers}/{n_cond2}")
stats_output.append("")

stats_output.append("="*80)
stats_output.append("END OF REPORT")
stats_output.append("="*80)

# Save to file
with open('single_cat_diag_data/writeup_textfiles/learning_statistics.txt', 'w') as f:
    f.write('\n'.join(stats_output))

print(f"\n{'='*60}")
print("Saved comprehensive statistics to learning_statistics.txt")
print(f"{'='*60}")

# ==========================================
# 5. SAVE FILTERED SUBJECT LISTS FOR DOWNSTREAM ANALYSES
# ==========================================
# Save learner IDs to file for use in test/typicality analyses
pd.DataFrame({'subject_id': learners_cond1}).to_csv(
    'single_cat_diag_data/condition_1_learners.csv', index=False)
pd.DataFrame({'subject_id': learners_cond2}).to_csv(
    'single_cat_diag_data/condition_2_learners.csv', index=False)

print("\nSaved learner subject IDs for downstream analyses")
print(f"  Condition 1: {len(learners_cond1)} learners")
print(f"  Condition 2: {n_cond2} learners")
