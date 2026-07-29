import streamlit as st  
import pandas as pd 
import plotly.express as px  

# Page configuration
st.set_page_config(page_title="CSV KPI Dashboard", layout="wide") 

# Background styling 
st.markdown( 
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1503264116251-35a269479413");
        background-size: cover;  
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("📊 CSV KPI Dashboard")
st.markdown("Upload a CSV file to instantly generate key metrics and visual insights.")

# 1. File Upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None: 
    # Read Data
    df = pd.read_csv(uploaded_file)
    
    # 2. Data Validation & Preview
    with st.expander("👀 View Raw Data Preview"):
        st.dataframe(df.head()) 

    # Filter for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    if not numeric_columns:
        st.error("No numeric columns found in this CSV. Please upload a file with numerical data.")
    else:
        # 3. User Selection
        st.sidebar.header("Dashboard Settings")
        selected_col = st.sidebar.selectbox("Select Numeric Column for KPIs", numeric_columns)
        
        # 4. KPI Calculation
        total_sum = df[selected_col].sum() 
        avg_val = df[selected_col].mean() 
        max_val = df[selected_col].max()
        min_val = df[selected_col].min()

        # 5. Display KPIs
        st.subheader(f"📈 Key Metrics: {selected_col}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Sum", f"{total_sum:,.2f}")
        col2.metric("Average", f"{avg_val:,.2f}")
        col3.metric("Maximum", f"{max_val:,.2f}")
        col4.metric("Minimum", f"{min_val:,.2f}")

        st.divider()

        # 6. Interactive Charts
        st.subheader("📊 Visual Insights") 
        
        tab1, tab2, tab3 = st.tabs(["Line Chart", "Bar Chart", "Distribution"])  

        with tab1:
            fig_line = px.line(df, y=selected_col, title=f"{selected_col} Trend Over Rows")
            st.plotly_chart(fig_line, use_container_width=True)

        with tab2:
            fig_bar = px.bar(df, y=selected_col, title=f"{selected_col} Bar Comparison")
            st.plotly_chart(fig_bar, use_container_width=True)

        with tab3:
            fig_hist = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}", nbins=20)
            st.plotly_chart(fig_hist, use_container_width=True)

else:
    st.info("💡 Please upload a CSV file via the sidebar to get started.") 
