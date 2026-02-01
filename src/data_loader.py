import pandas as pd
import os

def load_data(
    data_path=r"data/raw/ethiopia_fi_unified_data.xlsx",
    enrichment_path=None # Optional, derived from Task 1 logs
):
    """
    Loads the official XLSX dataset and appends the enrichment data found in Task 1.
    """
    
    # 1. Load Main XLSX Data
    # Determine the absolute path relative to the project root if needed, 
    # but here we assume the script is run from project root or notebooks folder handling.
    # Adjusting path handling to be robust.
    if not os.path.exists(data_path):
        # Try finding it relative to current working directory if not found
        if os.path.exists(os.path.join("..", data_path)):
            data_path = os.path.join("..", data_path)
        else:
            raise FileNotFoundError(f"Main data file not found at: {data_path}")
    
    print(f"Loading data from {data_path}...")
    
    # Read the 'data' sheet - find sheet with 'record_id' column
    xls = pd.ExcelFile(data_path)
    target_sheet = None
    for sheet in xls.sheet_names:
        try:
            df_preview = pd.read_excel(data_path, sheet_name=sheet, nrows=1)
            if 'record_id' in df_preview.columns:
                target_sheet = sheet
                break
        except:
            continue
            
    if target_sheet:
        df = pd.read_excel(data_path, sheet_name=target_sheet)
    else:
        # Fallback to first sheet
        df = pd.read_excel(data_path, sheet_name=0)
        
    print(f"Loaded {len(df)} records from Excel.")

    # 2. Define Enrichment Data (from Task 1)
    # These are observations we found that were missing from the starter set
    enrichment_records = [
        # Event: Foreign Bank Entry Directive
        {
            'record_id': 'EVT_NEW_01', 'record_type': 'event', 'category': 'policy', 
            'indicator': 'NBE Directive SBB/94/2025 (Foreign Banks)', 'start_date': '2025-06-25', 'data_year': 2025,
            'source_name': 'NBE', 'source_url': 'https://nbe.gov.et', 'confidence': 'high',
            'notes': 'Official directive opening sector to foreign banks'
        },
        # Impact Link: Foreign Bank -> Service Quality
        {
            'record_id': 'IMP_NEW_01', 'parent_id': 'EVT_NEW_01', 'record_type': 'impact_link', 
            'pillar': 'QUALITY', 'impact_direction': 'increase', 'impact_magnitude': 'high', 'lag_months': 12,
            'notes': 'Competition expected to improve service quality'
        },
         # Event: Telebirr 62.5M Target
        {
            'record_id': 'EVT_NEW_02', 'record_type': 'target', 'pillar': 'USAGE',
            'indicator': 'Telebirr User Target 2026', 'indicator_code': 'USG_TELEBIRR_USERS',
            'value_numeric': 62500000, 'unit': 'users', 'unit_type': 'count',
            'observation_date': '2026-06-30', 'data_year': 2026,
            'source_name': 'Ethio Telecom', 'source_url': 'https://ethiotelecom.et', 'confidence': 'medium'
        }
    ]
    
    # 3. Merge
    print(f"Enriching with {len(enrichment_records)} new records...")
    df_enrich = pd.DataFrame(enrichment_records)
    
    # Align columns
    for col in df.columns:
        if col not in df_enrich.columns:
            df_enrich[col] = None
            
    df_unified = pd.concat([df, df_enrich], ignore_index=True)
    
    # Ensure correct types for dates
    date_cols = ['observation_date', 'start_date', 'end_date', 'collection_date']
    for col in date_cols:
        if col in df_unified.columns:
            df_unified[col] = pd.to_datetime(df_unified[col], errors='coerce')
            
    return df_unified

if __name__ == "__main__":
    # Test
    try:
        df = load_data()
        print("Success! Data Head:")
        print(df[['record_id', 'record_type', 'pillar', 'indicator']].head())
        print("Success! Enrichment Check (New Records):")
        print(df[df['record_id'].str.contains('NEW', na=False)][['record_id', 'indicator']])
    except Exception as e:
        print(f"Error: {e}")
