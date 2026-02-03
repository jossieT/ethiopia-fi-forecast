import pandas as pd
import numpy as np

def run_baseline_forecast(df, indicator_code, start_year=2025, end_year=2027):
    """
    Runs a baseline trend forecast using numpy polyfit (linear) on historical data.
    Returns a dataframe with forecasted years.
    """
    hist = df[(df['indicator_code'] == indicator_code) & 
              (df['record_type'] == 'observation') & 
              (df['gender'] == 'all')].sort_values('data_year')
    
    if len(hist) < 2:
        return pd.DataFrame()
    
    x_hist = hist['data_year'].values
    y_hist = hist['value_numeric'].values
    
    # Linear fit: y = mx + c
    coefficients = np.polyfit(x_hist, y_hist, 1)
    polynomial = np.poly1d(coefficients)
    
    forecast_years = np.arange(start_year, end_year + 1)
    preds = polynomial(forecast_years)
    
    # Simple uncertainty: std of residuals
    resids = y_hist - polynomial(x_hist)
    uncertainty = np.std(resids) * 1.96 # 95% CI roughly
    
    forecast_df = pd.DataFrame({
        'data_year': forecast_years,
        'baseline_prediction': preds,
        'ci_lower': preds - uncertainty,
        'ci_upper': preds + uncertainty
    })
    
    # Ensure non-negative
    for col in ['baseline_prediction', 'ci_lower', 'ci_upper']:
        forecast_df[col] = forecast_df[col].clip(lower=0)
    
    return forecast_df

def apply_event_impacts(baseline_forecast, impact_model, scenario='base', indicator_code=None):
    """
    Applies event impacts to a baseline forecast.
    impact_model should be the joined impact/event dataframe from data_loader/Task 3.
    scenario: 'base', 'optimistic', 'pessimistic'
    """
    forecast = baseline_forecast.copy()
    
    # Magnitude modifiers for scenarios
    mod_map = {'optimistic': 1.5, 'base': 1.0, 'pessimistic': 0.5}
    modifier = mod_map.get(scenario, 1.0)
    
    # Is it a rate (%) or a count?
    is_rate = True
    if indicator_code and (indicator_code.startswith('USG_') and '_RATE' not in indicator_code):
        is_rate = False

    # Mapping impacts to years
    if is_rate:
        mag_map = {'high': 5.0, 'medium': 2.5, 'low': 1.0}
    else:
        # Growth factors for counts (fraction of baseline)
        mag_map = {'high': 0.20, 'medium': 0.10, 'low': 0.05}
    
    for _, row in impact_model.iterrows():
        impact_year = int(row['realized_year'])
        if impact_year in forecast['data_year'].values:
            base_mag = mag_map.get(str(row['impact_magnitude']).lower(), 0.0)
            direction = 1 if row['impact_direction'] == 'increase' else -1
            
            net_impact_val = base_mag * direction * modifier
            
            if is_rate:
                # Additive for rates (pp)
                forecast.loc[forecast['data_year'] >= impact_year, 'baseline_prediction'] += net_impact_val
            else:
                # Multiplicative for counts (growth)
                forecast.loc[forecast['data_year'] >= impact_year, 'baseline_prediction'] *= (1 + net_impact_val)

            
    # Ensure non-negative
    forecast['baseline_prediction'] = forecast['baseline_prediction'].clip(lower=0)
    
    return forecast
