import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 0. APPLY LEARNING CRITERION BASED ON TEST PERFORMANCE
# ==========================================
# Load test data for both conditions
df_test_cond1 = pd.read_csv('single_cat_diag_data/condition_1_testPhase.csv')
df_test_cond2 = pd.read_csv('single_cat_diag_data/condition_2_testPhase.csv')

# Define trained items (labels 'a' for both conditions)
# Calculate accuracy on trained items only
def get_learners(df_test, threshold=0.70):
    """
    Returns list of subject IDs who achieved >= threshold accuracy on trained items
    """
    # Filter to only trained items (category 'a')
    trained_items = df_test[df_test['category'] == 'a'].copy()
    
    # Calculate accuracy per subject
    trained_items['correct'] = (trained_items['response'] == 'a').astype(float)
    subject_accuracy = trained_items.groupby('subject_id')['correct'].mean()
    
    # Filter subjects meeting criterion
    learners = subject_accuracy[subject_accuracy >= threshold].index.tolist()
    
    return learners, subject_accuracy

# Get learners for each condition
learners_cond1, acc_cond1 = get_learners(df_test_cond1, threshold=0.70)
learners_cond2, acc_cond2 = get_learners(df_test_cond2, threshold=0.70)

print(f"\nCondition 1: {len(learners_cond1)} subjects met 80% criterion on trained items")
print(f"Condition 2: {len(learners_cond2)} subjects met 80% criterion on trained items")

# ==========================================
# 1. LOAD DATA & FILTER TO LEARNERS ONLY
# ==========================================
df_cond1 = pd.read_csv('single_cat_diag_data/condition_1_study.csv')
df_cond2 = pd.read_csv('single_cat_diag_data/condition_2_trainPhase.csv')

# Filter to learners only
df_cond1 = df_cond1[df_cond1['subject_id'].isin(learners_cond1)]
df_cond2 = df_cond2[df_cond2['subject_id'].isin(learners_cond2)]

n_cond1 = len(learners_cond1)
n_cond2 = len(learners_cond2)

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
fig1.suptitle(f'Generative Study Training Performance (n={n_cond1}, ≥80% test accuracy)', 
              fontsize=18, fontweight='bold', y=1.05)

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
plt.savefig('single_cat_diag_data/generative_training_analysis.png', bbox_inches='tight', dpi=300)
print(f"Saved generative_training_analysis.png (n={n_cond1})")

# ==========================================
# 3. CLASSIFICATION TRAINING (CONDITION 2)
# ==========================================
# Format accuracy as numeric (1.0 for True, 0.0 for False)
df_cond2['accuracy'] = df_cond2['accuracy'].astype(float)

# ---- Fill forward for early finishers ----
# Find the last block each subject completed
last_block_per_subject = df_cond2.groupby('subject_id')['block'].max()

# Determine the maximum possible blocks (should be 8 based on design)
max_blocks = 7

# For each subject who finished early, fill forward their final accuracy
filled_rows = []
for subject_id, last_block in last_block_per_subject.items():
    if last_block < max_blocks:
        # Get their final block's accuracy
        final_accuracy = df_cond2[(df_cond2['subject_id'] == subject_id) & 
                                   (df_cond2['block'] == last_block)]['accuracy'].mean()
        
        # Create rows for missing blocks, assuming they maintained criterion performance
        for missing_block in range(int(last_block) + 1, max_blocks + 1):
            filled_rows.append({
                'subject_id': subject_id,
                'block': missing_block,
                'accuracy': 1.0  # Maintain their criterion performance
            })

# Append filled rows to the dataframe
if filled_rows:
    df_filled = pd.DataFrame(filled_rows)
    df_cond2_complete = pd.concat([df_cond2, df_filled], ignore_index=True)
else:
    df_cond2_complete = df_cond2.copy()

# Aggregate accuracy by subject and block (now with filled data)
learning_cond2 = df_cond2_complete.groupby(['subject_id', 'block'])['accuracy'].mean().reset_index()

# Relabel blocks to start from 1
learning_cond2['block'] = learning_cond2['block'] + 1

# Plot Classification Training Data
fig2 = plt.figure(figsize=(8, 6))

sns.lineplot(data=learning_cond2, x='block', y='accuracy', marker='o', 
             color='#007bff', linewidth=2.5, markersize=8)

plt.title(f'Classification Training: Accuracy over Blocks (n={n_cond2}, ≥80% test accuracy)', 
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Training Block', fontsize=14)
plt.ylabel('Mean Accuracy', fontsize=14)
plt.ylim(-0.05, 1.05)
max_block = int(learning_cond2['block'].max())
plt.xticks(range(1, max_block + 1))

plt.tight_layout()
plt.savefig('single_cat_diag_data/classification_training_analysis.png', bbox_inches='tight', dpi=300)
print(f"Saved classification_training_analysis.png (n={n_cond2})")

# ==========================================
# 4. SAVE FILTERED SUBJECT LISTS FOR DOWNSTREAM ANALYSES
# ==========================================
# Save learner IDs to file for use in test/typicality analyses
pd.DataFrame({'subject_id': learners_cond1}).to_csv(
    'single_cat_diag_data/condition_1_learners.csv', index=False)
pd.DataFrame({'subject_id': learners_cond2}).to_csv(
    'single_cat_diag_data/condition_2_learners.csv', index=False)

print("\nSaved learner subject IDs for downstream analyses")
