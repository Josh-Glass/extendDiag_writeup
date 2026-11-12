import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD DATA & CALCULATE SAMPLE SIZES
# ==========================================
# Load the generated CSV files
df_cond1 = pd.read_csv('condition_1_study.csv')
df_cond2 = pd.read_csv('condition_2_trainPhase.csv')

# Calculate unique subjects dynamically
n_cond1 = df_cond1['subject_id'].nunique()
n_cond2 = df_cond2['subject_id'].nunique()

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

# Plot Generative Study Data
sns.set_theme(style="whitegrid")
fig1, axes = plt.subplots(1, 3, figsize=(18, 5.5))
fig1.suptitle(f'Generative Study Training Performance (n={n_cond1})', fontsize=18, fontweight='bold', y=1.05)

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
    ax.set_xticks(range(int(trial_agg['trial'].max() + 1)))

plt.tight_layout()
plt.savefig('generative_training_analysis.png', bbox_inches='tight', dpi=300)
print(f"Saved generative_training_analysis.png (n={n_cond1})")

# ==========================================
# 3. CLASSIFICATION TRAINING (CONDITION 2)
# ==========================================
# Format accuracy as numeric (1.0 for True, 0.0 for False)
df_cond2['accuracy'] = df_cond2['accuracy'].astype(float)

# Aggregate accuracy by subject and block
learning_cond2 = df_cond2.groupby(['subject_id', 'block'])['accuracy'].mean().reset_index()

# Plot Classification Training Data
fig2 = plt.figure(figsize=(8, 6))

sns.lineplot(data=learning_cond2, x='block', y='accuracy', marker='o', 
             color='#007bff', linewidth=2.5, markersize=8)

plt.title(f'Classification Training: Accuracy over Blocks (n={n_cond2})', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Training Block', fontsize=14)
plt.ylabel('Mean Accuracy', fontsize=14)
plt.ylim(-0.05, 1.05)
plt.xticks(range(int(learning_cond2['block'].max() + 1)))

plt.tight_layout()
plt.savefig('classification_training_analysis.png', bbox_inches='tight', dpi=300)
print(f"Saved classification_training_analysis.png (n={n_cond2})")

# Optional: plt.show() if you are running this interactively in Jupyter/Spyder