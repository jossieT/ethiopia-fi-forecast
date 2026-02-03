import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import numpy as np

# Add src to path for data_loader and forecaster
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_loader import load_data
from forecaster import run_baseline_forecast, apply_event_impacts

st.set_page_config(page_title="Ethiopia FI Forecast Dashboard", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def get_processed_data():
    df, df_impact = load_data()
    
    # Prepare impact model for forecasting
    events_df = df[df['record_type'] == 'event'][['record_id', 'indicator', 'start_date', 'data_year']]
    events_df.rename(columns={'indicator': 'event_name', 'start_date': 'event_date', 'data_year': 'event_year'}, inplace=True)
    impact_model = pd.merge(df_impact, events_df, left_on='parent_id', right_on='record_id', how='left')
    impact_model['realized_year'] = impact_model['event_year'] + (impact_model['lag_months'].fillna(0) / 12.0)
    
    return df, impact_model

df, impact_model = get_processed_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🚀 Overview", "📈 Trends Explorer", "🔮 Forecast Analysis", "🎯 Inclusion Targets"])

# --- PAGE: OVERVIEW ---
if page == "🚀 Overview":
    st.title("Ethiopia Financial Inclusion Overview")
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Get latest Access %
    acc_latest = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['record_type'] == 'observation') & (df['gender'] == 'all')].sort_values('data_year').iloc[-1]['value_numeric']
    col1.metric("Latest Access (%)", f"{acc_latest:.1f}%", "Historical (2024)")
    
    # P2P/ATM Ratio
    p2p_val = df[(df['indicator_code'] == 'USG_P2P_VALUE') & (df['record_type'] == 'observation')].sort_values('data_year').iloc[-1]['value_numeric']
    atm_val = df[(df['indicator_code'] == 'USG_ATM_VALUE') & (df['record_type'] == 'observation')].sort_values('data_year').iloc[-1]['value_numeric']
    ratio = p2p_val / atm_val if atm_val > 0 else 0
    col2.metric("P2P/ATM Ratio", f"{ratio:.2f}x", "Usage Shift")
    
    # 4G Coverage
    net_cov = df[(df['indicator_code'] == 'ACC_4G_COV') & (df['record_type'] == 'observation')].iloc[-1]['value_numeric']
    col3.metric("4G Coverage (%)", f"{net_cov:.1f}%")
    
    # Number of Events
    event_count = len(df[df['record_type'] == 'event'])
    col4.metric("Events Tracked", event_count)
    
    st.markdown("---")
    
    # High Level Trends Chart
    st.subheader("Key Indicator Trends")
    indicators = st.multiselect("Select Indicators", df['indicator_code'].unique(), default=['ACC_OWNERSHIP', 'ACC_MOBILE_PEN'])
    
    trend_df = df[(df['indicator_code'].isin(indicators)) & (df['record_type'] == 'observation') & (df['gender'] == 'all')]
    fig = px.line(trend_df, x='data_year', y='value_numeric', color='indicator_code', markers=True, 
                  labels={'value_numeric': 'Value', 'data_year': 'Year'},
                  title="Historical Growth")
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE: TRENDS EXPLORER ---
elif page == "📈 Trends Explorer":
    st.title("Detailed Trends Explorer")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        target_ind = st.selectbox("Select Indicator", df['indicator_code'].unique())
        gender_filter = st.selectbox("Gender", df['gender'].unique() if 'gender' in df.columns else ['all'])
        
    with col2:
        plot_df = df[(df['indicator_code'] == target_ind) & (df['record_type'] == 'observation')]
        if 'gender' in plot_df.columns:
            plot_df = plot_df[plot_df['gender'] == gender_filter]
            
        fig = px.bar(plot_df, x='data_year', y='value_numeric', title=f"Historical: {target_ind}",
                     color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
        
    st.dataframe(plot_df[['data_year', 'indicator', 'value_numeric', 'source_name']])

# --- PAGE: FORECAST ANALYSIS ---
elif page == "🔮 Forecast Analysis":
    st.title("Scenario-Based Forecasts (2025-2027)")
    
    target = st.selectbox("Select Project Target", ['ACC_OWNERSHIP', 'USG_P2P_COUNT'])
    
    # Run Forecast
    baseline = run_baseline_forecast(df, target)
    target_impacts = impact_model[impact_model['related_indicator'] == target]
    
    scenarios = ['pessimistic', 'base', 'optimistic']
    colors = {'pessimistic': '#e74c3c', 'base': '#3498db', 'optimistic': '#2ecc71'}
    
    fig = go.Figure()
    
    # Historical Data
    hist = df[(df['indicator_code'] == target) & (df['record_type'] == 'observation') & (df['gender'] == 'all')].sort_values('data_year')
    fig.add_trace(go.Scatter(x=hist['data_year'], y=hist['value_numeric'], name='Historical', mode='lines+markers', line=dict(color='black', width=3)))
    
    # Scenarios
    for scn in scenarios:
        res = apply_event_impacts(baseline, target_impacts, scenario=scn, indicator_code=target)
        fig.add_trace(go.Scatter(x=res['data_year'], y=res['baseline_prediction'], name=scn.capitalize(), line=dict(color=colors[scn], dash='dash')))
        
        if scn == 'base':
            fig.add_trace(go.Scatter(
                x=list(res['data_year']) + list(res['data_year'][::-1]),
                y=list(res['ci_upper']) + list(res['ci_lower'][::-1]),
                fill='toself',
                fillcolor=f"rgba(52, 152, 219, 0.2)",
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name="Confidence Interval (95%)"
            ))
            
    fig.update_layout(title=f"Forecast: {target}", xaxis_title="Year", yaxis_title="Value", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Data Table")
    st.dataframe(res) # Last scenario computed
    
    csv = res.to_csv(index=False).encode('utf-8')
    st.download_button("Download Forecast CSV", csv, "forecast_export.csv", "text/csv")

# --- PAGE: INCLUSION TARGETS ---
elif page == "🎯 Inclusion Targets":
    st.title("Path to 60% Financial Inclusion")
    
    target_val = 60.0
    
    # Run base forecast for Access
    baseline_acc = run_baseline_forecast(df, 'ACC_OWNERSHIP', start_year=2025, end_year=2030)
    acc_impacts = impact_model[impact_model['related_indicator'] == 'ACC_OWNERSHIP']
    base_proj = apply_event_impacts(baseline_acc, acc_impacts, scenario='base', indicator_code='ACC_OWNERSHIP')
    
    latest_acc = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['record_type'] == 'observation')].iloc[-1]['value_numeric']
    gap = target_val - latest_acc
    
    col1, col2 = st.columns(2)
    col1.metric("Progress to 60%", f"{latest_acc:.1f}%", f"-{gap:.1f}% Gap")
    
    # Estimate Year of Success
    success_year = base_proj[base_proj['baseline_prediction'] >= target_val]
    if not success_year.empty:
        year_val = success_year.iloc[0]['data_year']
        col2.success(f"Projected Target Reached in: {int(year_val)}")
    else:
        col2.warning("Target not reached by 2030 in Base Scenario")
        
    # Visual Target Tracker
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = latest_acc,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Account Ownership %"},
        gauge = {
            'axis': {'range': [None, 100]},
            'steps': [
                {'range': [0, 45], 'color': "lightgray"},
                {'range': [45, 60], 'color': "gray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60}
        }
    ))
    st.plotly_chart(fig)
    
    st.markdown("""
    ### Consortium Key Questions
    1. **Will we hit the 60% goal?** Yes, the base scenario predicts success by 2028.
    2. **Which events matter most?** The Digital ID (Fayda) rollout is the single largest accelerator for access.
    3. **What about usage?** P2P payments are growing much faster than account ownership, suggesting deepening usage among existing users.
    """)
