import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# =========================================================================
# ⚙️ 1. DASHBOARD RUNTIME CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="Executive Campaign Insights Platform", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Relational Database Connection Settings
DB_USER = 'postgres'
DB_PASSWORD = 'Post@2026' 
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'demo'                  

# Safely URL-encode credentials
safe_password = quote_plus(DB_PASSWORD)
conn_str = f'postgresql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

@st.cache_data(ttl=600)
def fetch_comprehensive_warehouse_data():
    engine = create_engine(conn_str)
    
    # Query matching your verified normalized multi-table database schema
    query = """
    SELECT 
        c.customer_id, c."Education", c."Marital_Status", c."Income", c."Country", c."Age", c."Children",
        s."MntWines", s."MntFruits", s."MntMeatProducts", s."MntFishProducts", s."MntSweetProducts", s."MntGoldProds", s."Total_Spend",
        a."NumDealsPurchases", a."NumWebPurchases", a."NumCatalogPurchases", a."NumStorePurchases", a."NumWebVisitsMonth",
        r."AcceptedCmp1", r."AcceptedCmp2", r."AcceptedCmp3", r."AcceptedCmp4", r."AcceptedCmp5", r."Response"
    FROM customers c
    JOIN customer_spend s ON c.customer_id = s.customer_id
    JOIN customer_activity a ON c.customer_id = a.customer_id
    JOIN campaign_responses r ON c.customer_id = r.customer_id;
    """
    df = pd.read_sql(query, con=engine)
    
    # Unified cohort grouping logic
    conditions = [
        (df['Total_Spend'] >= 1500),
        (df['Income'] >= 75000) & (df['Total_Spend'] < 1500),
        (df['Income'] >= 40000) & (df['Income'] < 75000) & (df['Total_Spend'] < 1500),
        (df['Income'] < 40000)
    ]
    choices = ['High Spender', 'High Income Elite', 'Standard Retail Profile', 'Family Shopper']
    df['customer_segment'] = np.select(conditions, choices, default='Standard Retail Profile')
    
    # Add grouping bins for business queries
    df['age_band'] = pd.cut(df['Age'], bins=[0, 34, 55, 120], labels=['Young (<35)', 'Middle-Aged (35-55)', 'Senior (>55)'])
    df['income_band'] = pd.cut(df['Income'], bins=[0, 40000, 75000, 1000000], labels=['Low (<$40k)', 'Moderate ($40k-$75k)', 'Premium (>$75k)'])
    
    return df

try:
    df = fetch_comprehensive_warehouse_data()

    # =========================================================================
    # 🎛️ 2. GLOBAL FILTERS
    # =========================================================================
    st.sidebar.title("🎯 Strategy Controls")
    selected_countries = st.sidebar.multiselect("Filter Regions:", options=sorted(df['Country'].unique()), default=sorted(df['Country'].unique()))
    
    # Filter dataset globally based on sidebar input
    df_filtered = df[df['Country'].isin(selected_countries)]

    st.title("📊 Enterprise Marketing Campaign & Cohort Analytics")
    st.markdown("This operational interface provides interactive, data-driven insights answering our core business use cases.")
    st.markdown("---")

    # =========================================================================
    # 📑 3. STRATEGIC BUSINESS USE CASE TABS
    # =========================================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Campaign Conversion Performance", 
        "🛍️ Product Spending Dynamics", 
        "🌐 Channel Ingestion & Web Traffic", 
        "🔮 Under-Served & Target Customer Blueprints"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: CAMPAIGN RESPONSE RATES (USE CASE 1)
    # -------------------------------------------------------------------------
    with tab1:
        st.subheader("💡 Use Case: Customer Segment Response Rates Across Campaigns")
        st.markdown("Identify which consumer cohorts yield the highest conversion returns overall and across specific marketing efforts (Cmp1-5).")
        
        cmp_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']
        
        # Calculate conversion percentages per segment
        cmp_summary = df_filtered.groupby('customer_segment')[cmp_cols].mean() * 100
        cmp_summary.columns = ['Campaign 1 %', 'Campaign 2 %', 'Campaign 3 %', 'Campaign 4 %', 'Campaign 5 %', 'Latest Response %']
        
        st.dataframe(cmp_summary.round(2), use_container_width=True)
        
        # Visualization of Latest Response Rate
        st.write("**Latest Campaign Response Rate Comparison (%)**")
        st.bar_chart(data=cmp_summary.reset_index(), x="customer_segment", y="Latest Response %", color="#4db6ac")

    # -------------------------------------------------------------------------
    # TAB 2: PRODUCT SPENDING PATTERNS (USE CASE 2)
    # -------------------------------------------------------------------------
    with tab2:
        st.subheader("💡 Use Case: Spending Variations Across Product Lines")
        st.markdown("Analyze how purchasing behavior across categories shifts based on demographic variables.")
        
        prod_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        
        demo_choice = st.selectbox("Pivot Spend Patterns By:", options=['age_band', 'income_band', 'Marital_Status', 'Country'])
        
        spend_summary = df_filtered.groupby(demo_choice)[prod_cols].mean()
        st.dataframe(spend_summary.round(2), use_container_width=True)
        
        st.write(f"**Total Average Expenditure Trends by {demo_choice} Context**")
        total_spend_trend = df_filtered.groupby(demo_choice)['Total_Spend'].mean().reset_index()
        st.bar_chart(data=total_spend_trend, x=demo_choice, y="Total_Spend", color="#ff8a65")

    # -------------------------------------------------------------------------
    # TAB 3: CHANNELS & WEB VISITS (USE CASE 3)
    # -------------------------------------------------------------------------
    with tab3:
        st.subheader("💡 Use Case: Ingestion Channel Distribution & Site Interaction")
        st.markdown("Track exactly where high-value customers complete checkouts and look at how often they browse our digital storefront.")
        
        channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumDealsPurchases']
        
        channel_summary = df_filtered.groupby('customer_segment').agg(
            Avg_Web_Purchases=('NumWebPurchases', 'mean'),
            Avg_Catalog_Purchases=('NumCatalogPurchases', 'mean'),
            Avg_Store_Purchases=('NumStorePurchases', 'mean'),
            Avg_Deals_Purchases=('NumDealsPurchases', 'mean'),
            Avg_Monthly_Web_Visits=('NumWebVisitsMonth', 'mean')
        )
        st.dataframe(channel_summary.round(2), use_container_width=True)
        
        st.write("**Digital Browsing Engagement Frequency (Average Monthly Web Visits)**")
        st.bar_chart(data=channel_summary.reset_index(), x="customer_segment", y="Avg_Monthly_Web_Visits", color="#008080")

    # -------------------------------------------------------------------------
    # TAB 4: UNDER-SERVED & TARGET BLUEPRINTS (USE CASE 4 & 5)
    # -------------------------------------------------------------------------
    with tab4:
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            st.subheader("🔍 Under-Served Cohort Discovery")
            st.markdown("*Criteria: High web traffic (Visits > 5), but low checkout value (Spend < $500).*")
            
            # Isolate under-served market rows
            underserved_df = df_filtered[(df_filtered['NumWebVisitsMonth'] > 5) & (df_filtered['Total_Spend'] < 500)]
            
            st.metric(label="Identified Under-Served Profiles Count", value=f"{len(underserved_df):,}")
            st.write("**Top Concentration of Under-Served Users by Segment Group:**")
            st.dataframe(underserved_df['customer_segment'].value_counts(), use_container_width=True)
            
        with sub_col2:
            st.subheader("🎯 Ideal Future Target Customer Template")
            st.markdown("*Criteria: High conversion success (Response = 1) paired with optimal spend activity.*")
            
            converted_df = df_filtered[df_filtered['Response'] == 1]
            
            if len(converted_df) > 0:
                st.write("**Optimal Target Age Range:**")
                st.write(f"Average Age: {int(converted_df['Age'].mean())} years old (Range: {int(converted_df['Age'].min())} - {int(converted_df['Age'].max())})")
                
                st.write("**Optimal Target Income Bracket:**")
                st.write(f"Average Income: ${converted_df['Income'].mean():,.2f}")
                
                st.write("**Top Converting Marital & Family Profiles:**")
                st.dataframe(converted_df['Marital_Status'].value_counts().head(2), use_container_width=True)
            else:
                st.info("No campaign converted profiles match current filters.")

except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    import os




