import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff

# Page configuration
st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.title("E-Commerce Customer Behavior & Purchase Patterns Dashboard")
st.markdown("Explore customer metrics, engagement on app vs. website, membership duration, and spending patterns interactively.")

# Sidebar & CSV Upload Option
st.sidebar.header("📁 Data Source & Filters")
uploaded_file = st.sidebar.file_uploader("Upload custom CSV (optional)", type=["csv"])

@st.cache_data
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    else:
        return pd.read_csv("ecommerce_customers.csv")

try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.subheader("🔍 Filter Data")
min_mem = float(df['Length of Membership'].min())
max_mem = float(df['Length of Membership'].max())
membership_range = st.sidebar.slider("Length of Membership (Years)", min_mem, max_mem, (min_mem, max_mem))

min_spend = float(df['Yearly Amount Spent'].min())
max_spend = float(df['Yearly Amount Spent'].max())
spend_range = st.sidebar.slider("Yearly Amount Spent ($)", min_spend, max_spend, (min_spend, max_spend))

# Filtered DataFrame
filtered_df = df[
    (df['Length of Membership'] >= membership_range[0]) & 
    (df['Length of Membership'] <= membership_range[1]) &
    (df['Yearly Amount Spent'] >= spend_range[0]) & 
    (df['Yearly Amount Spent'] <= spend_range[1])
]

# 4 Key Metrics on Top
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_customers = len(filtered_df)
avg_spend = filtered_df['Yearly Amount Spent'].mean()
avg_membership = filtered_df['Length of Membership'].mean()
max_spend_val = filtered_df['Yearly Amount Spent'].max()

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{total_customers:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg. Yearly Spend</div>
            <div class="metric-value">${avg_spend:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg. Membership</div>
            <div class="metric-value">{avg_membership:.2f} yrs</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Highest Yearly Spend</div>
            <div class="metric-value">${max_spend_val:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 5 Graphs
st.markdown("## 📈 Data Visualizations & Insights")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Univariate (Spend)", 
    "2. Bivariate (App vs Spend)", 
    "3. Correlation Heatmap", 
    "4. Membership vs Spend", 
    "5. Website vs App Time"
])

with tab1:
    st.subheader("Distribution of Yearly Amount Spent (Univariate)")
    fig = px.histogram(filtered_df, x="Yearly Amount Spent", nbins=30, marginal="box", 
                       color_discrete_sequence=['#1f77b4'], title="Yearly Amount Spent Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Most customers spend between $450 and $600 annually, showing a normal distribution curve.")

with tab2:
    st.subheader("Time on App vs. Yearly Amount Spent (Bivariate)")
    fig = px.scatter(filtered_df, x="Time on App", y="Yearly Amount Spent", trendline="ols",
                     color="Length of Membership", color_continuous_scale="Viridis",
                     title="Time on App vs Yearly Amount Spent")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Positive relationship between time spent on the mobile app and total yearly spend.")

with tab3:
    st.subheader("Correlation Heatmap")
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r",
                    title="Correlation Matrix of Numeric Features")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Length of Membership shows the strongest positive correlation with Yearly Amount Spent.")

with tab4:
    st.subheader("Length of Membership vs. Yearly Amount Spent")
    fig = px.scatter(filtered_df, x="Length of Membership", y="Yearly Amount Spent", trendline="ols",
                     color_discrete_sequence=['#2ca02c'], title="Membership Duration Impact on Spending")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Longer membership duration strongly correlates with higher spending tiers.")

with tab5:
    st.subheader("App Time vs Website Time Comparison")
    filtered_df['Platform Preference'] = np.where(filtered_df['Time on App'] > filtered_df['Time on Website'], 'App User', 'Website User')
    fig = px.box(filtered_df, x='Platform Preference', y='Yearly Amount Spent', color='Platform Preference',
                 title="Spending Comparison: App Users vs Website Users")
    st.plotly_chart(fig, use_container_width=True)
    st.info("App users tend to show slightly higher median spending compared to website users.")

st.markdown("---")

# Raw Data Checkbox
if st.checkbox("Show Raw Data Table"):
    st.subheader("Raw Dataset Preview")
    st.dataframe(filtered_df)

# Main Findings Section
st.markdown("## 📝 Main Findings & Business Recommendations")
st.markdown("""
1. **Primary Growth Driver:** Length of membership is the most significant predictor of high customer lifetime value and yearly spend.
2. **Digital Engagement:** Customers engaging more via the mobile app exhibit higher monetary value compared to desktop web users.
3. **Recommendation:** The company should invest heavily in retention programs (loyalty rewards, VIP perks) to extend membership longevity and optimize the mobile app UI/UX to drive higher conversion.
""")
