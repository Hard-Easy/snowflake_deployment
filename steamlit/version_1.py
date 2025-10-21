import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
from numpy import busday_count

# ---------------------------------------
# 📦 Sample Data (with Start/End dates)
# ---------------------------------------
activity_data = [

]

df = pd.DataFrame(activity_data)
for col in ['Date', 'Start Date', 'End Date']:
    df[col] = pd.to_datetime(df[col])

st.set_page_config(layout="wide")
st.title("📊 Data Mart Activity Dashboard")

# ---------------------------------------
# 🧭 Sidebar Selections
# ---------------------------------------
with st.sidebar:
    st.header("🔍 Filter")
    selected_set = st.selectbox("📁 Select Set", df['Set'].unique())
    filtered_df = df[df['Set'] == selected_set]
    selected_mart = st.selectbox("🗂️ Select Data Mart", filtered_df['Data Mart'].unique())
    mart_df = filtered_df[filtered_df['Data Mart'] == selected_mart]

# ---------------------------------------
# 🔧 Utility: Chart Builders
# ---------------------------------------
def build_stacked_bar(df, y_col, title, unit_labels=True):
    df = df.copy()
    df['Pending Units'] = df['Total Units'] - df['Completed Units']
    df['Progress %'] = (df['Completed Units'] / df['Total Units'] * 100).round(1)
    df['Pending %'] = 100 - df['Progress %']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df[y_col],
        x=df['Progress %'],
        name='Completed',
        orientation='h',
        marker_color='green',
        text=df['Completed Units'].astype(str) + ' done' if unit_labels else None,
        textposition='inside',
        insidetextanchor='start'
    ))
    fig.add_trace(go.Bar(
        y=df[y_col],
        x=df['Pending %'],
        name='Pending',
        orientation='h',
        marker_color='lightgray',
        text=df['Pending Units'].astype(str) + ' pending' if unit_labels else None,
        textposition='inside',
        insidetextanchor='end'
    ))
    fig.update_layout(
        barmode='stack',
        xaxis=dict(title='Progress (%)', range=[0, 100]),
        yaxis=dict(autorange='reversed'),
        height=200 + len(df) * 30,
        showlegend=True,
        title=title
    )
    return fig

def build_radar_chart(df, label):
    df = df.copy()
    df['Progress %'] = (df['Completed Units'] / df['Total Units'] * 100).round(1)
    return go.Figure(go.Scatterpolar(
        r=df['Progress %'],
        theta=df['Activity'],
        fill='toself',
        name=label,
        marker_color='green'
    )).update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400,
        title=f"🕸️ Radar: Activity Completion for {label}"
    )

# ---------------------------------------
# 📊 Summary Section
# ---------------------------------------
st.markdown("## 📌 Summary Progress by Data Mart")

summary = (
    filtered_df.groupby(['Data Mart', 'Activity'])
    .apply(lambda x: x.loc[x['Date'].idxmax()])
    .reset_index(drop=True)
    .groupby('Data Mart')
    .agg({'Completed Units': 'sum', 'Total Units': 'sum'})
    .assign(
        Progress_pct=lambda x: (x['Completed Units'] / x['Total Units'] * 100).round(1),
        Pending_Units=lambda x: x['Total Units'] - x['Completed Units'],
        Pending_pct=lambda x: 100 - x['Progress_pct']
    )
    .reset_index()
)

st.plotly_chart(build_stacked_bar(summary, 'Data Mart', "Overall Data Mart Progress"), use_container_width=True)

# ---------------------------------------
# 📅 Date Table
# ---------------------------------------
st.markdown(f"## 📅 Activity Schedule for `{selected_mart}`")

latest_mart = mart_df.groupby('Activity').apply(lambda x: x.loc[x['Date'].idxmax()]).reset_index(drop=True)
latest_mart['Remaining Weekdays'] = latest_mart['End Date'].apply(
    lambda d: max(0, busday_count(date.today(), d.date()))
)

with st.expander("🔎 View Remaining Schedule"):
    date_table = latest_mart[['Activity', 'Start Date', 'End Date', 'Remaining Weekdays']].copy()
    date_table['Start Date'] = date_table['Start Date'].dt.strftime('%Y-%m-%d')
    date_table['End Date'] = date_table['End Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(date_table, use_container_width=True)

# ---------------------------------------
# 📊 Activity Progress
# ---------------------------------------
st.markdown("## 📈 Activity Breakdown")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(build_stacked_bar(latest_mart, 'Activity', f"Detailed Progress - {selected_mart}"), use_container_width=True)

with col2:
    radar_fig = build_radar_chart(latest_mart, selected_mart)
    st.plotly_chart(radar_fig, use_container_width=True)
