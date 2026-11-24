import pandas as pd
import numpy as np
from scipy import stats
import os
from datetime import datetime

# Create output directory
os.makedirs('single_cat_diag_data/writeup_textfiles', exist_ok=True)

# Open output file for writing
output_file = 'single_cat_diag_data/writeup_textfiles/statistical_results.txt'
output_lines = []

def print_and_save(text=""):
    """Print to console and save to output list"""
    print(text)
    output_lines.append(text)

print_and_save("="*70)
print_and_save("STATISTICAL TESTS: X vs Y Items")
print_and_save(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print_and_save("="*70)

# ==========================================
# LOAD LEARNER SUBJECT IDS
# ==========================================
learners_cond1 = pd.read_csv('single_cat_diag_data/condition_1_learners.csv')['subject_id'].tolist()
learners_cond2 = pd.read_csv('single_cat_diag_data/condition_2_learners.csv')['subject_id'].tolist()

print_and_save(f"\nSample Sizes (≥70% accuracy on trained items at test):")
print_and_save(f"  Generative Study Condition: n = {len(learners_cond1)}")
print_and_save(f"  Classification Condition: n = {len(learners_cond2)}")

# ==========================================
# TEST PHASE ANALYSIS
# ==========================================
print_and_save("\n" + "="*70)
print_and_save("TEST PHASE: GENERALIZATION TO X vs Y ITEMS")
print_and_save("="*70)

# Load and filter test data
df_test_cond1 = pd.read_csv('single_cat_diag_data/condition_1_testPhase.csv')
df_test_cond2 = pd.read_csv('single_cat_diag_data/condition_2_testPhase.csv')

df_test_cond1 = df_test_cond1[df_test_cond1['subject_id'].isin(learners_cond1)]
df_test_cond2 = df_test_cond2[df_test_cond2['subject_id'].isin(learners_cond2)]

# Code responses as 1 if "Alpha", 0 otherwise
df_test_cond1['chose_A'] = df_test_cond1['response'].astype(str).str.lower().isin(['a', 'alpha']).astype(float)
df_test_cond2['chose_A'] = df_test_cond2['response'].astype(str).str.lower().isin(['a', 'alpha']).astype(float)

# Calculate mean response per subject for X and Y items
def get_subject_means(df):
    x_items = df[df['category'] == 'x'].groupby('subject_id')['chose_A'].mean()
    y_items = df[df['category'] == 'y'].groupby('subject_id')['chose_A'].mean()
    return x_items, y_items

x_cond1, y_cond1 = get_subject_means(df_test_cond1)
x_cond2, y_cond2 = get_subject_means(df_test_cond2)

# WITHIN-CONDITION TESTS (Paired t-tests)
print_and_save("\n--- WITHIN-CONDITION COMPARISONS (Paired t-tests) ---")

# Condition 1: X vs Y
t_stat_c1, p_val_c1 = stats.ttest_rel(x_cond1, y_cond1)
print_and_save(f"\nGenerative Study Condition:")
print_and_save(f"  Mean X items: {x_cond1.mean():.3f} (SD = {x_cond1.std():.3f})")
print_and_save(f"  Mean Y items: {y_cond1.mean():.3f} (SD = {y_cond1.std():.3f})")
print_and_save(f"  Paired t-test: t({len(x_cond1)-1}) = {t_stat_c1:.3f}, p = {p_val_c1:.4f}")
print_and_save(f"  Cohen's d = {(x_cond1.mean() - y_cond1.mean()) / x_cond1.std():.3f}")

# Condition 2: X vs Y
t_stat_c2, p_val_c2 = stats.ttest_rel(x_cond2, y_cond2)
print_and_save(f"\nClassification Condition:")
print_and_save(f"  Mean X items: {x_cond2.mean():.3f} (SD = {x_cond2.std():.3f})")
print_and_save(f"  Mean Y items: {y_cond2.mean():.3f} (SD = {y_cond2.std():.3f})")
print_and_save(f"  Paired t-test: t({len(x_cond2)-1}) = {t_stat_c2:.3f}, p = {p_val_c2:.4f}")
print_and_save(f"  Cohen's d = {(x_cond2.mean() - y_cond2.mean()) / x_cond2.std():.3f}")

# BETWEEN-CONDITION TESTS (Independent t-tests)
print_and_save("\n--- BETWEEN-CONDITION COMPARISONS (Independent t-tests) ---")

# X items: Condition 1 vs Condition 2
t_stat_x, p_val_x = stats.ttest_ind(x_cond1, x_cond2)
pooled_std_x = np.sqrt(((len(x_cond1)-1)*x_cond1.std()**2 + (len(x_cond2)-1)*x_cond2.std()**2) / (len(x_cond1)+len(x_cond2)-2))
cohens_d_x = (x_cond1.mean() - x_cond2.mean()) / pooled_std_x
print_and_save(f"\nX Items (Generative Study vs Classification):")
print_and_save(f"  Generative Study mean: {x_cond1.mean():.3f}")
print_and_save(f"  Classification mean: {x_cond2.mean():.3f}")
print_and_save(f"  Independent t-test: t({len(x_cond1)+len(x_cond2)-2}) = {t_stat_x:.3f}, p = {p_val_x:.4f}")
print_and_save(f"  Cohen's d = {cohens_d_x:.3f}")

# Y items: Condition 1 vs Condition 2
t_stat_y, p_val_y = stats.ttest_ind(y_cond1, y_cond2)
pooled_std_y = np.sqrt(((len(y_cond1)-1)*y_cond1.std()**2 + (len(y_cond2)-1)*y_cond2.std()**2) / (len(y_cond1)+len(y_cond2)-2))
cohens_d_y = (y_cond1.mean() - y_cond2.mean()) / pooled_std_y
print_and_save(f"\nY Items (Generative Study vs Classification):")
print_and_save(f"  Generative Study mean: {y_cond1.mean():.3f}")
print_and_save(f"  Classification mean: {y_cond2.mean():.3f}")
print_and_save(f"  Independent t-test: t({len(y_cond1)+len(y_cond2)-2}) = {t_stat_y:.3f}, p = {p_val_y:.4f}")
print_and_save(f"  Cohen's d = {cohens_d_y:.3f}")

# ==========================================
# TYPICALITY PHASE ANALYSIS
# ==========================================
print_and_save("\n" + "="*70)
print_and_save("TYPICALITY PHASE: RATINGS OF X vs Y ITEMS")
print_and_save("="*70)

# Load and filter typicality data
df_typ_cond1 = pd.read_csv('single_cat_diag_data/condition_1_typicality.csv')
df_typ_cond2 = pd.read_csv('single_cat_diag_data/condition_2_typicality.csv')

df_typ_cond1 = df_typ_cond1[df_typ_cond1['subject_id'].isin(learners_cond1)]
df_typ_cond2 = df_typ_cond2[df_typ_cond2['subject_id'].isin(learners_cond2)]

# Ensure responses are numeric
df_typ_cond1['response'] = pd.to_numeric(df_typ_cond1['response'], errors='coerce')
df_typ_cond2['response'] = pd.to_numeric(df_typ_cond2['response'], errors='coerce')

# Identify X and Y items based on stimId (not category column)
def get_subject_typ_means(df):
    # X items are those with stimId starting with 'X'
    x_items = df[df['stimId'].str.startswith('X')].groupby('subject_id')['response'].mean()
    # Y items are those with stimId starting with 'Y'
    y_items = df[df['stimId'].str.startswith('Y')].groupby('subject_id')['response'].mean()
    return x_items, y_items

x_typ_c1, y_typ_c1 = get_subject_typ_means(df_typ_cond1)
x_typ_c2, y_typ_c2 = get_subject_typ_means(df_typ_cond2)

# WITHIN-CONDITION TESTS (Paired t-tests)
print_and_save("\n--- WITHIN-CONDITION COMPARISONS (Paired t-tests) ---")

# Condition 1: X vs Y
t_stat_typ_c1, p_val_typ_c1 = stats.ttest_rel(x_typ_c1, y_typ_c1)
print_and_save(f"\nGenerative Study Condition:")
print_and_save(f"  Mean X items: {x_typ_c1.mean():.3f} (SD = {x_typ_c1.std():.3f})")
print_and_save(f"  Mean Y items: {y_typ_c1.mean():.3f} (SD = {y_typ_c1.std():.3f})")
print_and_save(f"  Paired t-test: t({len(x_typ_c1)-1}) = {t_stat_typ_c1:.3f}, p = {p_val_typ_c1:.4f}")
print_and_save(f"  Cohen's d = {(x_typ_c1.mean() - y_typ_c1.mean()) / x_typ_c1.std():.3f}")

# Condition 2: X vs Y
t_stat_typ_c2, p_val_typ_c2 = stats.ttest_rel(x_typ_c2, y_typ_c2)
print_and_save(f"\nClassification Condition:")
print_and_save(f"  Mean X items: {x_typ_c2.mean():.3f} (SD = {x_typ_c2.std():.3f})")
print_and_save(f"  Mean Y items: {y_typ_c2.mean():.3f} (SD = {y_typ_c2.std():.3f})")
print_and_save(f"  Paired t-test: t({len(x_typ_c2)-1}) = {t_stat_typ_c2:.3f}, p = {p_val_typ_c2:.4f}")
print_and_save(f"  Cohen's d = {(x_typ_c2.mean() - y_typ_c2.mean()) / x_typ_c2.std():.3f}")

# BETWEEN-CONDITION TESTS (Independent t-tests)
print_and_save("\n--- BETWEEN-CONDITION COMPARISONS (Independent t-tests) ---")

# X items: Condition 1 vs Condition 2
t_stat_typ_x, p_val_typ_x = stats.ttest_ind(x_typ_c1, x_typ_c2)
pooled_std_typ_x = np.sqrt(((len(x_typ_c1)-1)*x_typ_c1.std()**2 + (len(x_typ_c2)-1)*x_typ_c2.std()**2) / (len(x_typ_c1)+len(x_typ_c2)-2))
cohens_d_typ_x = (x_typ_c1.mean() - x_typ_c2.mean()) / pooled_std_typ_x
print_and_save(f"\nX Items (Generative Study vs Classification):")
print_and_save(f"  Generative Study mean: {x_typ_c1.mean():.3f}")
print_and_save(f"  Classification mean: {x_typ_c2.mean():.3f}")
print_and_save(f"  Independent t-test: t({len(x_typ_c1)+len(x_typ_c2)-2}) = {t_stat_typ_x:.3f}, p = {p_val_typ_x:.4f}")
print_and_save(f"  Cohen's d = {cohens_d_typ_x:.3f}")

# Y items: Condition 1 vs Condition 2
t_stat_typ_y, p_val_typ_y = stats.ttest_ind(y_typ_c1, y_typ_c2)
pooled_std_typ_y = np.sqrt(((len(y_typ_c1)-1)*y_typ_c1.std()**2 + (len(y_typ_c2)-1)*y_typ_c2.std()**2) / (len(y_typ_c1)+len(y_typ_c2)-2))
cohens_d_typ_y = (y_typ_c1.mean() - y_typ_c2.mean()) / pooled_std_typ_y
print_and_save(f"\nY Items (Generative Study vs Classification):")
print_and_save(f"  Generative Study mean: {y_typ_c1.mean():.3f}")
print_and_save(f"  Classification mean: {y_typ_c2.mean():.3f}")
print_and_save(f"  Independent t-test: t({len(y_typ_c1)+len(y_typ_c2)-2}) = {t_stat_typ_y:.3f}, p = {p_val_typ_y:.4f}")
print_and_save(f"  Cohen's d = {cohens_d_typ_y:.3f}")

print_and_save("\n" + "="*70)
print_and_save("ANALYSIS COMPLETE")
print_and_save("="*70)

# Save all output to file
with open(output_file, 'w') as f:
    f.write('\n'.join(output_lines))

print(f"\nStatistical results saved to: {output_file}")
