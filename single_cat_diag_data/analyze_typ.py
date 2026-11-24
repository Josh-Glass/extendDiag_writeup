import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directories
os.makedirs('single_cat_diag_data/figures', exist_ok=True)

# ==========================================
# 0. LOAD LEARNER SUBJECT IDS
# ==========================================
learners_cond1 = pd.read_csv('single_cat_diag_data/condition_1_learners.csv')['subject_id'].tolist()
learners_cond2 = pd.read_csv('single_cat_diag_data/condition_2_learners.csv')['subject_id'].tolist()

print(f"Filtering to {len(learners_cond1)} learners in Condition 1")
print(f"Filtering to {len(learners_cond2)} learners in Condition 2")

# ==========================================
# 1. LOAD TYPICALITY DATA & FILTER TO LEARNERS
# ==========================================
df_cond1_typ = pd.read_csv('single_cat_diag_data/condition_1_typicality.csv')
df_cond2_typ = pd.read_csv('single_cat_diag_data/condition_2_typicality.csv')

print("\n=== DIAGNOSTIC: RAW DATA ===")
print(f"Condition 1 raw rows: {len(df_cond1_typ)}")
print(f"Condition 2 raw rows: {len(df_cond2_typ)}")
print(f"Condition 1 raw subjects: {df_cond1_typ['subject_id'].nunique()}")
print(f"Condition 2 raw subjects: {df_cond2_typ['subject_id'].nunique()}")

# Filter to learners only
df_cond1_typ = df_cond1_typ[df_cond1_typ['subject_id'].isin(learners_cond1)]
df_cond2_typ = df_cond2_typ[df_cond2_typ['subject_id'].isin(learners_cond2)]

print("\n=== DIAGNOSTIC: AFTER FILTERING TO LEARNERS ===")
print(f"Condition 1 filtered rows: {len(df_cond1_typ)}")
print(f"Condition 2 filtered rows: {len(df_cond2_typ)}")
print(f"Condition 1 filtered subjects: {df_cond1_typ['subject_id'].nunique()}")
print(f"Condition 2 filtered subjects: {df_cond2_typ['subject_id'].nunique()}")

# Check what categories exist
print("\n=== DIAGNOSTIC: CATEGORY LABELS ===")
print(f"Condition 1 unique categories: {df_cond1_typ['category'].unique()}")
print(f"Condition 2 unique categories: {df_cond2_typ['category'].unique()}")
print(f"Condition 1 category counts:\n{df_cond1_typ['category'].value_counts()}")
print(f"Condition 2 category counts:\n{df_cond2_typ['category'].value_counts()}")

# Ensure responses are numeric
df_cond1_typ['response'] = pd.to_numeric(df_cond1_typ['response'], errors='coerce')
df_cond2_typ['response'] = pd.to_numeric(df_cond2_typ['response'], errors='coerce')

print("\n=== DIAGNOSTIC: RESPONSE VALUES ===")
print(f"Condition 1 NaN responses: {df_cond1_typ['response'].isna().sum()}")
print(f"Condition 2 NaN responses: {df_cond2_typ['response'].isna().sum()}")
print(f"Condition 1 response range: {df_cond1_typ['response'].min()} to {df_cond1_typ['response'].max()}")
print(f"Condition 2 response range: {df_cond2_typ['response'].min()} to {df_cond2_typ['response'].max()}")

# Calculate Sample Sizes
n_cond1 = df_cond1_typ['subject_id'].nunique()
n_cond2 = df_cond2_typ['subject_id'].nunique()

print(f"\nCondition 1: {n_cond1} subjects in typicality analysis")
print(f"Condition 2: {n_cond2} subjects in typicality analysis")

# 2. Define the Stimulus Coordinates (Same as Test Phase)
dataX = np.array([
    [.8, .7], [.9, .8], [1.0, .9],  
    [.9, .7], [1.0, .8],            
    [1.0, .7]                       
])

dataY = np.array([
    [.7, .8], [.8, .9], [.9, 1.0],  
    [.7, .9], [.8, 1.0],            
    [.7, 1.0]                       
])

dataA = np.array([
    [.250, .050], [.325, .125], [.400, .200], 
    [.475, .275], [.550, .350], [.625, .425], [.700, .500]
])

dataNotA = np.array([
    [.125, .625], [.200, .550], [.275, .475], [.350, .400], 
    [.600, .150], [.675, .075], [.750, .000]  
])

# 3. Create Mapping Dictionary
coord_map = {}
for i, coord in enumerate(dataX): coord_map[f'X{i+1}'] = coord
for i, coord in enumerate(dataY): coord_map[f'Y{i+1}'] = coord
for i, coord in enumerate(dataA): coord_map[f'A{i+1}'] = coord
for i, coord in enumerate(dataNotA): coord_map[f'NotA{i+1}'] = coord

def process_typicality_data(df, cond_name):
    # Map (x,y) coordinates to the stimuli
    df['x'] = df['stimId'].apply(lambda s: coord_map.get(s, [np.nan, np.nan])[0])
    df['y'] = df['stimId'].apply(lambda s: coord_map.get(s, [np.nan, np.nan])[1])
    
    print(f"\n=== DIAGNOSTIC: {cond_name} COORDINATE MAPPING ===")
    print(f"Rows with valid x coordinates: {df['x'].notna().sum()}")
    print(f"Rows with valid y coordinates: {df['y'].notna().sum()}")
    print(f"Unique stimIds: {df['stimId'].unique()}")
    print(f"Sample of mapped coordinates:")
    print(df[['stimId', 'x', 'y', 'category']].head(10))
    
    # Aggregate mean typicality per coordinate
    agg = df.groupby(['stimId', 'x', 'y', 'category'])['response'].mean().reset_index()
    agg['condition'] = cond_name
    
    print(f"\n=== DIAGNOSTIC: {cond_name} AGGREGATED DATA ===")
    print(f"Total aggregated rows: {len(agg)}")
    print(f"X items: {len(agg[agg['category'] == 'x'])}")
    print(f"Y items: {len(agg[agg['category'] == 'y'])}")
    print(f"A items: {len(agg[agg['category'] == 'a'])}")
    print(f"Sample of aggregated data:")
    print(agg.head(10))
    
    return agg

agg_cond1_typ = process_typicality_data(df_cond1_typ, f'Generative Learning (n={n_cond1})')
agg_cond2_typ = process_typicality_data(df_cond2_typ, f'Classification Learning (n={n_cond2})')

# ==========================================
# 4. PLOTTING THE TYPICALITY SPATIAL HEATMAP
# ==========================================
sns.set_theme(style="white")
fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharex=True, sharey=True)

# Fix color scale from 0 to 6 (slider bounds)
vmin, vmax = 0, 6

for i, (cond_name, df_plot) in enumerate([(agg_cond1_typ['condition'].iloc[0], agg_cond1_typ), 
                                          (agg_cond2_typ['condition'].iloc[0], agg_cond2_typ)]):
    ax = axes[i]
    
    # We use 'viridis' (yellow/green/blue) here to distinguish it from the accuracy map (red/blue)
    scatter = ax.scatter(df_plot['x'], df_plot['y'], 
                         c=df_plot['response'], cmap='viridis', 
                         s=350, edgecolor='black', linewidth=1, vmin=vmin, vmax=vmax)
    
    # Label each point with its stimId
    for _, row in df_plot.iterrows():
        ax.text(row['x'], row['y'] + 0.035, row['stimId'], 
                ha='center', va='bottom', fontsize=9, alpha=0.8)
        
    ax.set_title(f'{cond_name}\nMean Typicality Rating', fontsize=14)
    ax.set_xlabel('Feature Dimension 1 (Size)', fontsize=12)
    ax.set_ylabel('Feature Dimension 2 (Shade)', fontsize=12)
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 1.15)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.plot([0, 1.15], [0, 1.15], color='gray', linestyle='--', alpha=0.5, label='y=x Boundary')

# Add a shared colorbar on the right side
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(scatter, cax=cbar_ax)
cbar.set_label('Typicality Rating (0 = Low, 6 = High)', fontsize=13, labelpad=15)

plt.subplots_adjust(right=0.9)
plt.savefig('single_cat_diag_data/figures/typicality_spatial_heatmap.png', bbox_inches='tight', dpi=300)
plt.savefig('single_cat_diag_data/figures/typicality_spatial_heatmap.pdf', bbox_inches='tight')
print("\nSaved typicality_spatial_heatmap.png and .pdf")
# plt.show()
