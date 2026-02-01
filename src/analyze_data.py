import pandas as pd
import numpy as np
from data_loader import load_data

def calculate_cagr(start_val, end_val, periods):
    if start_val == 0 or periods == 0:
        return np.nan
    return (end_val / start_val) ** (1 / periods) - 1

def analyze_access_slowdown(df):
    """
    Analyzes the slowdown in account ownership growth (2021-2024).
    """
    acc_df = df[
        (df['record_type'] == 'observation') & 
        (df['indicator_code'] == 'ACC_OWNERSHIP') & 
        (df['gender'] == 'all')
    ].sort_values('data_year')
    
    if len(acc_df) < 2:
        return "Insufficient data for access analysis."
        
    acc_df['growth_pp'] = acc_df['value_numeric'].diff()
    acc_df['years_diff'] = acc_df['data_year'].diff()
    acc_df['avg_annual_growth_pp'] = acc_df['growth_pp'] / acc_df['years_diff']
    
    return acc_df[['data_year', 'value_numeric', 'growth_pp', 'avg_annual_growth_pp']]

def analyze_gender_gap(df):
    """
    Calculates gender gap over time.
    """
    gender_df = df[
        (df['record_type'] == 'observation') & 
        (df['indicator_code'] == 'ACC_OWNERSHIP') & 
        (df['gender'].isin(['male', 'female']))
    ].pivot(index='data_year', columns='gender', values='value_numeric')
    
    if gender_df.empty:
        return "No gender data available."
        
    gender_df['gap_pp'] = gender_df['male'] - gender_df['female']
    return gender_df

def get_key_insights():
    df = load_data()
    
    print("--- Access Trajectory ---")
    print(analyze_access_slowdown(df))
    
    print("\n--- Gender Gap ---")
    print(analyze_gender_gap(df))
    
    return "Analysis Complete"

if __name__ == "__main__":
    get_key_insights()
