import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern, Clean & Professional UI Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .main {
            background-color: #0f172a;
        }

        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0b1120;
            border-right: 1px solid #334155;
        }
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }

        /* Metric Card Styling */
        .metric-card {
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid #38bdf8;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            text-align: center;
            transition: transform 0.2s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: #818cf8;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 700;
            color: #38bdf8;
        }
        .metric-label {
            font-size: 13px;
            color: #94a3b8;
            font-weight: 500;
        }

        h1, h2, h3 {
            color: #38bdf8 !important;
            font-weight: 700 !important;
        }

        /* Insight Box Styling */
        .insight-box {
            background: rgba(15, 23, 42, 0.8);
            border-left: 5px solid #38bdf8;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            color: #cbd5e1;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.title("E-Commerce Customer Behavior & Purchase Patterns Dashboard")
st.markdown("<p style='color:#cbd5e1; font-size:1.1rem;'>Explore customer metrics, engagement on app vs. website, membership duration, and spending patterns interactively.</p>", unsafe_allow_html=True)

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
    st.error(f"⚠️ Error loading data: {e}. Please ensure 'ecommerce_customers.csv' is in the same folder.")
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

if filtered_df.empty:
    st.warning("⚠️ Selected filters ke mutabiq koi data available nahi hai. Please sidebar ranges adjust karein.")
    st.stop()

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

# 5 Tabs with Visualizations (Plotly Dark Template Matched)
st.markdown("## 📈 Data Visualizations & Insights")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Univariate (Spend)", 
    "2. Bivariate (App vs Spend)", 
    "3. Correlation Heatmap", 
    "4. Membership vs Spend", 
    "5. Website vs App Time"
])

chart_theme = "plotly_dark"
color_palette = ["#38bdf8", "#818cf8", "#f472b6", "#34d399", "#fbbf24"]

with tab1:
    st.subheader("Distribution of Yearly Amount Spent (Univariate)")
    fig1 = px.histogram(
        filtered_df, x="Yearly Amount Spent", nbins=30, marginal="box", 
        color_discrete_sequence=['#38bdf8'], title="Yearly Amount Spent Distribution",
        template=chart_theme
    )
    fig1.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)
    st.info("💡 Most customers spend between $450 and $600 annually, showing a normal distribution curve.")

with tab2:
    st.subheader("Time on App vs. Yearly Amount Spent (Bivariate)")
    fig2 = px.scatter(
        filtered_df, x="Time on App", y="Yearly Amount Spent",
        color="Length of Membership", color_continuous_scale="Viridis",
        title="Time on App vs Yearly Amount Spent",
        template=chart_theme
    )
    fig2.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)
    st.info("💡 Positive relationship between time spent on the mobile app and total yearly spend.")

with tab3:
    st.subheader("Correlation Heatmap")
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    corr = numeric_df.corr().round(2)
    fig3 = px.imshow(
        corr, text_auto=True, aspect="auto", color_continuous_scale="Blues",
        title="Correlation Matrix of Numeric Features",
        template=chart_theme
    )
    fig3.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", height=450)
    st.plotly_chart(fig3, use_container_width=True)
    st.info("💡 Length of Membership shows the strongest positive correlation with Yearly Amount Spent.")

with tab4:
    st.subheader("Length of Membership vs. Yearly Amount Spent")
    fig4 = px.scatter(
        filtered_df, x="Length of Membership", y="Yearly Amount Spent",
        color_discrete_sequence=['#34d399'], title="Membership Duration Impact on Spending",
        template=chart_theme
    )
    fig4.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)
    st.info("💡 Longer membership duration strongly correlates with higher spending tiers.")

with tab5:
    st.subheader("App Time vs Website Time Comparison")
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['Platform Preference'] = np.where(
        filtered_df_copy['Time on App'] > filtered_df_copy['Time on Website'], 'App User', 'Website User'
    )
    fig5 = px.box(
        filtered_df_copy, x='Platform Preference', y='Yearly Amount Spent', color='Platform Preference',
        title="Spending Comparison: App Users vs Website Users",
        color_discrete_sequence=color_palette,
        template=chart_theme
    )
    fig5.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    st.info("💡 App users tend to show slightly higher median spending compared to website users.")

st.markdown("---")

# Raw Data Checkbox
if st.checkbox("📂 Show Raw Data Table"):
    st.subheader("Raw Dataset Preview")
    st.dataframe(filtered_df, use_container_width=True)

# Main Findings Section
st.markdown("## 📝 Main Findings & Business Recommendations")
st.markdown("""
<div class="insight-box">
    <ol>
        <li><b>Primary Growth Driver:</b> Length of membership is the most significant predictor of high customer lifetime value and yearly spend.</li>
        <li><b>Digital Engagement:</b> Customers engaging more via the mobile app exhibit higher monetary value compared to desktop web users.</li>
        <li><b>Strategic Recommendation:</b> The company should invest heavily in retention programs (loyalty rewards, VIP perks) to extend membership longevity and optimize the mobile app UI/UX to drive higher conversion.</li>
    </ol>
</div>
""", unsafe_allow_html=True)
