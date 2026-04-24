import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config for that "Dark Mode" Fitness look
st.set_page_config(page_title="ProLift Analytics", layout="wide")

st.title("🏋️‍♂️ ProLift: Your Progress Dashboard")
st.markdown("---")

# 1. Load your CSV data
# Assuming your file is 'MasterWorkouts.csv'
df = pd.read_csv('MasterWorkouts.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Weight'] = df['Weight'].str.replace(' lbs', '').astype(float)

# 2. Key Metric: Estimated 1-Rep Max (Brzycki Formula)
# This shows 'Strength' even if reps/weight change
df['E1RM'] = df['Weight'] * (36 / (37 - df['Reps']))

# 3. Sidebar Filters
exercise_list = df['Exercise'].unique()
selected_exercise = st.sidebar.selectbox("Select Exercise", exercise_list)

# Filter Data
filtered_df = df[df['Exercise'] == selected_exercise]

# 4. Visuals
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📈 Strength Trend: {selected_exercise}")
    fig_strength = px.line(filtered_df, x='Date', y='E1RM', 
                           title="Estimated 1RM Over Time",
                           template="plotly_dark", line_shape="spline")
    st.plotly_chart(fig_strength, use_container_width=True)

with col2:
    st.subheader("🔥 Volume Distribution")
    # Calculate Total Volume per session (Weight * Reps)
    filtered_df['Volume'] = filtered_df['Weight'] * filtered_df['Reps']
    fig_vol = px.bar(filtered_df, x='Date', y='Volume', 
                     color='Volume', title="Total Volume per Set",
                     template="plotly_dark")
    st.plotly_chart(fig_vol, use_container_width=True)

# 5. Raw Data Table
with st.expander("See Raw Training Log"):
    st.dataframe(filtered_df.sort_values(by='Date', ascending=False))