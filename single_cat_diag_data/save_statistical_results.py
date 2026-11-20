import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

# Create output file
output_file = 'single_cat_diag_data/statistical_results.txt'
with open(output_file, 'w') as f:
    # Header
    f.write("="*70 + "\n")
    f.write("EXPERIMENT 3: STATISTICAL TESTS - X vs Y Items\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*70 + "\n")
    
    # ==========================================
    # LOAD LEARNER SUBJECT IDS
    # ==========================================
    learners_cond1 = pd.read_csv('single_cat_diag_data/condition_1_learners.csv')['subject_id'].tolist()
    learners_cond2 = pd.read_csv('single_cat_diag_data/condition_2_learners.csv')['subject_id'].tolist()
    
    f.write(f"\nSample Sizes (≥70% accuracy on trained items at test):\n")
    f.write(f"  Generative Study Condition: n = {len(learners_cond1)}\n")
    f.write(f"  Classification Condition: n = {len(learners_cond2)}\n")
    
    # ==========================================
    # TEST PHASE ANALYSIS
    # ==========================================
    f.write("\n" + "="*70 + "\n")
    f.write("TEST PHASE: GENERALIZATION TO X vs Y ITEMS\n")
    f.write("="*70 + "\n")
    
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
    f.write("\n--- WITHIN-CONDITION COMPARISONS (Paired t-tests) ---\n")
    
    # Generative Study: X vs Y
    t_stat_c1, p_val_c1 = stats.ttest_rel(x_cond1, y_cond1)
    f.write(f"\nGenerative Study Condition:\n")
    f.write(f"  Mean X items: {x_cond1.mean():.3f} (SD = {x_cond1.std():.3f})\n")
    f.write(f"  Mean Y items: {y_cond1.mean():.3f} (SD = {y_cond1.std():.3f})\n")
    f.write(f"  Paired t-test: t({len(x_cond1)-1}) = {t_stat_c1:.3f}, p = {p_val_c1:.4f}\n")
    f.write(f"  Cohen's d = {(x_cond1.mean() - y_cond1.mean()) / x_cond1.std():.3f}\n")
    
    # Classification: X vs Y
    t_stat_c2, p_val_c2 = stats.ttest_rel(x_cond2, y_cond2)
    f.write(f"\nClassification Condition:\n")
    f.write(f"  Mean X items: {x_cond2.mean():.3f} (SD = {x_cond2.std():.3f})\n")
    f.write(f"  Mean Y items: {y_cond2.mean():.3f} (SD = {y_cond2.std():.3f})\n")
    f.write(f"  Paired t-test: t({len(x_cond2)-1}) = {t_stat_c2:.3f}, p = {p_val_c2:.4f}\n")
    f.write(f"  Cohen's d = {(x_cond2.mean() - y_cond2.mean()) / x_cond2.std():.3f}\n")
    
    # BETWEEN-CONDITION TESTS (Independent t-tests)
    f.write("\n--- BETWEEN-CONDITION COMPARISONS (Independent t-tests) ---\n")
    
    # X items: Generative Study vs Classification
    t_stat_x, p_val_x = stats.ttest_ind(x_cond1, x_cond2)
    f.write(f"\nX Items (Generative Study vs Classification):\n")
    f.write(f"  Generative Study mean: {x_cond1.mean():.3f}\n")
    f.write(f"  Classification mean: {x_cond2.mean():.3f}\n")
    f.write(f"  Independent t-test: t({len(x_cond1)+len(x_cond2)-2}) = {t_stat_x:.3f}, p = {p_val_x:.4f}\n")
    
    # Y items: Generative Study vs Classification
    t_stat_y, p_val_y = stats.ttest_ind(y_cond1, y_cond2)
    f.write(f"\nY Items (Generative Study vs Classification):\n")
    f.write(f"  Generative Study mean: {y_cond1.mean():.3f}\n")
    f.write(f"  Classification mean: {y_cond2.mean():.3f}\n")
    f.write(f"  Independent t-test: t({len(y_cond1)+len(y_cond2)-2}) = {t_stat_y:.3f}, p = {p_val_y:.4f}\n")
    
    # ==========================================
    # TYPICALITY PHASE ANALYSIS
    # ==========================================
    f.write("\n" + "="*70 + "\n")
    f.write("TYPICALITY PHASE: RATINGS OF X vs Y ITEMS\n")
    f.write("="*70 + "\n")
    
    # Load and filter typicality data
    df_typ_cond1 = pd.read_csv('single_cat_diag_data/condition_1_typicality.csv')
    df_typ_cond2 = pd.read_csv('single_cat_diag_data/condition_2_typicality.csv')
    
    df_typ_cond1 = df_typ_cond1[df_typ_cond1['subject_id'].isin(learners_cond1)]
    df_typ_cond2 = df_typ_cond2[df_typ_cond2['subject_id'].isin(learners_cond2)]
    
    # Ensure responses are numeric
    df_typ_cond1['response'] = pd.to_numeric(df_typ_cond1['response'], errors='coerce')
    df_typ_cond2['response'] = pd.to_numeric(df_typ_cond2['response'], errors='coerce')
    
    # Identify X and Y items based on stimId
    def get_subject_typ_means(df):
        x_items = df[df['stimId'].str.startswith('X')].groupby('subject_id')['response'].mean()
        y_items = df[df['stimId'].str.startswith('Y')].groupby('subject_id')['response'].mean()
        return x_items, y_items
    
    x_typ_c1, y_typ_c1 = get_subject_typ_means(df_typ_cond1)
    x_typ_c2, y_typ_c2 = get_subject_typ_means(df_typ_cond2)
    
    # WITHIN-CONDITION TESTS (Paired t-tests)
    f.write("\n--- WITHIN-CONDITION COMPARISONS (Paired t-tests) ---\n")
    
    # Generative Study: X vs Y
    t_stat_typ_c1, p_val_typ_c1 = stats.ttest_rel(x_typ_c1, y_typ_c1)
    f.write(f"\nGenerative Study Condition:\n")
    f.write(f"  Mean X items: {x_typ_c1.mean():.3f} (SD = {x_typ_c1.std():.3f})\n")
    f.write(f"  Mean Y items: {y_typ_c1.mean():.3f} (SD = {y_typ_c1.std():.3f})\n")
    f.write(f"  Paired t-test: t({len(x_typ_c1)-1}) = {t_stat_typ_c1:.3f}, p = {p_val_typ_c1:.4f}\n")
    f.write(f"  Cohen's d = {(x_typ_c1.mean() - y_typ_c1.mean()) / x_typ_c1.std():.3f}\n")
    
    # Classification: X vs Y
    t_stat_typ_c2, p_val_typ_c2 = stats.ttest_rel(x_typ_c2, y_typ_c2)
    f.write(f"\nClassification Condition:\n")
    f.write(f"  Mean X items: {x_typ_c2.mean():.3f} (SD = {x_typ_c2.std():.3f})\n")
    f.write(f"  Mean Y items: {y_typ_c2.mean():.3f} (SD = {y_typ_c2.std():.3f})\n")
    f.write(f"  Paired t-test: t({len(x_typ_c2)-1}) = {t_stat_typ_c2:.3f}, p = {p_val_typ_c2:.4f}\n")
    f.write(f"  Cohen's d = {(x_typ_c2.mean() - y_typ_c2.mean()) / x_typ_c2.std():.3f}\n")
    
    # BETWEEN-CONDITION TESTS (Independent t-tests)
    f.write("\n--- BETWEEN-CONDITION COMPARISONS (Independent t-tests) ---\n")
    
    # X items: Generative Study vs Classification
    t_stat_typ_x, p_val_typ_x = stats.ttest_ind(x_typ_c1, x_typ_c2)
    f.write(f"\nX Items (Generative Study vs Classification):\n")
    f.write(f"  Generative Study mean: {x_typ_c1.mean():.3f}\n")
    f.write(f"  Classification mean: {x_typ_c2.mean():.3f}\n")
    f.write(f"  Independent t-test: t({len(x_typ_c1)+len(x_typ_c2)-2}) = {t_stat_typ_x:.3f}, p = {p_val_typ_x:.4f}\n")
    
    # Y items: Generative Study vs Classification
    t_stat_typ_y, p_val_typ_y = stats.ttest_ind(y_typ_c1, y_typ_c2)
    f.write(f"\nY Items (Generative Study vs Classification):\n")
    f.write(f"  Generative Study mean: {y_typ_c1.mean():.3f}\n")
    f.write(f"  Classification mean: {y_typ_c2.mean():.3f}\n")
    f.write(f"  Independent t-test: t({len(y_typ_c1)+len(y_typ_c2)-2}) = {t_stat_typ_y:.3f}, p = {p_val_typ_y:.4f}\n")
    
    f.write("\n" + "="*70 + "\n")
    f.write("ANALYSIS COMPLETE\n")
    f.write("="*70 + "\n")

print(f"Statistical results saved to: {output_file}")
print("Run complete!")
