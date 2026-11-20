import pandas as pd
import numpy as np
from scipy import stats

print("="*70)
print("STATISTICAL TESTS: X vs Y Items")
print("="*70)

# ==========================================
# LOAD LEARNER SUBJECT IDS
# ==========================================
learners_cond1 = pd.read_csv('single_cat_diag_data/condition_1_learners.csv')['subject_id'].tolist()
learners_cond2 = pd.read_csv('single_cat_diag_data/condition_2_learners.csv')['subject_id'].tolist()

# ==========================================
# TEST PHASE ANALYSIS
# ==========================================
print("\n" + "="*70)
print("TEST PHASE: GENERALIZATION TO X vs Y ITEMS")
print("="*70)

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
print("\n--- WITHIN-CONDITION COMPARISONS (Paired t-tests) ---")

# Condition 1: X vs Y
t_stat_c1, p_val_c1 = stats.ttest_rel(x_cond1, y_cond1)
print(f"\nCondition 1 (Generative Learning):")
print(f"  Mean X items: {x_cond1.mean():.3f} (SD = {x_cond1.std():.3f})")
print(f"  Mean Y items: {y_cond1.mean():.3f} (SD = {y_cond1.std():.3f})")
print(f"  Paired t-test: t({len(x_cond1)-1}) = {t_stat_c1:.3f}, p = {p_val_c1:.4f}")
print(f"  Cohen's d = {(x_cond1.mean() - y_cond1.mean()) / x_cond1.std():.3f}")

# Condition 2: X vs Y
t_stat_c2, p_val_c2 = stats.ttest_rel(x_cond2, y_cond2)
print(f"\nCondition 2 (Classification Learning):")
print(f"  Mean X items: {x_cond2.mean():.3f} (SD = {x_cond2.std():.3f})")
print(f"  Mean Y items: {y_cond2.mean():.3f} (SD = {y_cond2.std():.3f})")
print(f"  Paired t-test: t({len(x_cond2)-1}) = {t_stat_c2:.3f}, p = {p_val_c2:.4f}")
print(f"  Cohen's d = {(x_cond2.mean() - y_cond2.mean()) / x_cond2.std():.3f}")

# BETWEEN-CONDITION TESTS (Independent t-tests)
print("\n--- BETWEEN-CONDITION COMPARISONS (Independent t-tests) ---")

# X items: Condition 1 vs Condition 2
t_stat_x, p_val_x = stats.ttest_ind(x_cond1, x_cond2)
print(f"\nX Items across conditions:")
print(f"  Condition 1 mean: {x_cond1.mean():.3f}")
print(f"  Condition 2 mean: {x_cond2.mean():.3f}")
print(f"  Independent t-test: t({len(x_cond1)+len(x_cond2)-2}) = {t_stat_x:.3f}, p = {p_val_x:.4f}")

# Y items: Condition 1 vs Condition 2
t_stat_y, p_val_y = stats.ttest_ind(y_cond1, y_cond2)
print(f"\nY Items across conditions:")
print(f"  Condition 1 mean: {y_cond1.mean():.3f}")
print(f"  Condition 2 mean: {y_cond2.mean():.3f}")
print(f"  Independent t-test: t({len(y_cond1)+len(y_cond2)-2}) = {t_stat_y:.3f}, p = {p_val_y:.4f}")

# ==========================================
# TYPICALITY PHASE ANALYSIS
# ==========================================
print("\n" + "="*70)
print("TYPICALITY PHASE: RATINGS OF X vs Y ITEMS")
print("="*70)

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
print("\n--- WITHIN-CONDITION COMPARISONS (Paired t-tests) ---")

# Condition 1: X vs Y
t_stat_typ_c1, p_val_typ_c1 = stats.ttest_rel(x_typ_c1, y_typ_c1)
print(f"\nCondition 1 (Generative Learning):")
print(f"  Mean X items: {x_typ_c1.mean():.3f} (SD = {x_typ_c1.std():.3f})")
print(f"  Mean Y items: {y_typ_c1.mean():.3f} (SD = {y_typ_c1.std():.3f})")
print(f"  Paired t-test: t({len(x_typ_c1)-1}) = {t_stat_typ_c1:.3f}, p = {p_val_typ_c1:.4f}")
print(f"  Cohen's d = {(x_typ_c1.mean() - y_typ_c1.mean()) / x_typ_c1.std():.3f}")

# Condition 2: X vs Y
t_stat_typ_c2, p_val_typ_c2 = stats.ttest_rel(x_typ_c2, y_typ_c2)
print(f"\nCondition 2 (Classification Learning):")
print(f"  Mean X items: {x_typ_c2.mean():.3f} (SD = {x_typ_c2.std():.3f})")
print(f"  Mean Y items: {y_typ_c2.mean():.3f} (SD = {y_typ_c2.std():.3f})")
print(f"  Paired t-test: t({len(x_typ_c2)-1}) = {t_stat_typ_c2:.3f}, p = {p_val_typ_c2:.4f}")
print(f"  Cohen's d = {(x_typ_c2.mean() - y_typ_c2.mean()) / x_typ_c2.std():.3f}")

# BETWEEN-CONDITION TESTS (Independent t-tests)
print("\n--- BETWEEN-CONDITION COMPARISONS (Independent t-tests) ---")

# X items: Condition 1 vs Condition 2
t_stat_typ_x, p_val_typ_x = stats.ttest_ind(x_typ_c1, x_typ_c2)
print(f"\nX Items across conditions:")
print(f"  Condition 1 mean: {x_typ_c1.mean():.3f}")
print(f"  Condition 2 mean: {x_typ_c2.mean():.3f}")
print(f"  Independent t-test: t({len(x_typ_c1)+len(x_typ_c2)-2}) = {t_stat_typ_x:.3f}, p = {p_val_typ_x:.4f}")

# Y items: Condition 1 vs Condition 2
t_stat_typ_y, p_val_typ_y = stats.ttest_ind(y_typ_c1, y_typ_c2)
print(f"\nY Items across conditions:")
print(f"  Condition 1 mean: {y_typ_c1.mean():.3f}")
print(f"  Condition 2 mean: {y_typ_c2.mean():.3f}")
print(f"  Independent t-test: t({len(y_typ_c1)+len(y_typ_c2)-2}) = {t_stat_typ_y:.3f}, p = {p_val_typ_y:.4f}")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
