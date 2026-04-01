import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Steam Digital Twin", layout="wide")
st.title("🔥 Steamflow analysis in Digital Twin Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("steam_flow_predictive_maintenance_output (3).csv")
    df['timestamp_ist'] = pd.to_datetime(df['timestamp_ist'])
    return df

df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['timestamp_ist'].min(), df['timestamp_ist'].max()]
)

if len(date_range) != 2:
    st.warning("Select valid date range")
    st.stop()

show_anomaly = st.sidebar.checkbox("Show Anomalies", value=True)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    (df['timestamp_ist'].dt.date >= date_range[0]) &
    (df['timestamp_ist'].dt.date <= date_range[1])
]

if filtered_df.empty:
    st.warning("No data available")
    st.stop()

filtered_df = filtered_df.copy()

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Steam Flow", round(filtered_df['steam_flow'].iloc[-1], 2))
col2.metric("Predicted Flow", round(filtered_df['predicted_steam_flow'].iloc[-1], 2))
col3.metric("Health Index", round(filtered_df['health_index'].iloc[-1], 2))
col4.metric("Maintenance Required", int(filtered_df['maintenance_required'].iloc[-1]))

# -----------------------------
# ACTUAL VS PREDICTED
# -----------------------------
st.subheader("📈 Steam Flow vs Prediction")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered_df['timestamp_ist'],
    y=filtered_df['steam_flow'],
    name='Actual'
))

fig.add_trace(go.Scatter(
    x=filtered_df['timestamp_ist'],
    y=filtered_df['predicted_steam_flow'],
    name='Predicted'
))

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ANOMALY DETECTION
# -----------------------------
st.subheader("🚨 Anomaly Detection")

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=filtered_df['timestamp_ist'],
    y=filtered_df['steam_flow'],
    name='Steam Flow'
))

if show_anomaly:
    anomalies = filtered_df[filtered_df['anomaly_flag'] == 1]

    fig2.add_trace(go.Scatter(
        x=anomalies['timestamp_ist'],
        y=anomalies['steam_flow'],
        mode='markers',
        marker=dict(color='red', size=8),
        name='Anomaly'
    ))

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# HEALTH INDEX
# -----------------------------
st.subheader("❤️ Health Index")

fig3 = px.line(filtered_df, x='timestamp_ist', y='health_index')
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# DEVIATION (IMPORTANT INSIGHT)
# -----------------------------
st.subheader("📉 Deviation (Error)")

fig4 = px.line(filtered_df, x='timestamp_ist', y='deviation')
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# MAINTENANCE ALERTS
# -----------------------------
st.subheader("🔧 Maintenance Alerts")

maintenance_df = filtered_df[filtered_df['maintenance_required'] == 1]

st.write(f"Total Alerts: {len(maintenance_df)}")

st.dataframe(maintenance_df.tail(10))

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🚀 Digital Twin for Steam System Monitoring")