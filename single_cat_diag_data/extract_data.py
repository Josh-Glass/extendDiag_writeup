import json
import pandas as pd
import glob

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def parse_phase(data_dict, phase_name):
    # Safely navigate the nested 'results' dictionary
    phase_data = data_dict.get('results', {}).get('results', {}).get(phase_name, [])
    
    # Return empty DataFrame if the phase is empty
    if not phase_data or len(phase_data) <= 1:
        return pd.DataFrame()
        
    headers = phase_data[0] # First row contains column names
    rows = phase_data[1:]   # Rest are the actual data
    return pd.DataFrame(rows, columns=headers)

# Define phases to extract
phases = ['trainPhase', 'study', 'testPhase', 'typicality']

# Dictionaries to hold aggregated data per condition and phase
agg_data = {
    '1': {phase: [] for phase in phases},
    '2': {phase: [] for phase in phases}
}

# Loop through all JSON files in your 'data' folder
for filepath in glob.glob('data/*.json'):
    data = load_json(filepath)
    
    # Extract metadata
    subj_id = data.get('id')
    cond = str(data.get('condition')) # Convert to string just in case
    
    # Skip if condition isn't defined or isn't 1 or 2
    if cond not in ['1', '2']:
        continue
        
    for phase in phases:
        df = parse_phase(data, phase)
        if not df.empty:
            df['subject_id'] = subj_id  # Add subject ID column
            df['condition'] = cond      # Add condition column
            agg_data[cond][phase].append(df)

# Concatenate all subjects together and save to CSV
for cond, phases_dict in agg_data.items():
    for phase, dfs in phases_dict.items():
        if dfs: # If there's data for this condition and phase
            combined_df = pd.concat(dfs, ignore_index=True)
            filename = f"condition_{cond}_{phase}.csv"
            combined_df.to_csv(filename, index=False)
            print(f"Successfully saved {filename} with {len(combined_df)} total rows.")