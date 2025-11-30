import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fashionista Price Optimizer",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        color: #FF1493;
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        color: #696969;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .result-box {
        background-color: #f0f8ff;
        border: 2px solid #FF1493;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .metric-card {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="main-header">👗 Fashionista Price Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ridge Regression Demand Model (R² = 0.9425)</div>', unsafe_allow_html=True)

st.markdown("---")

# API endpoint (updated to match running API on port 8001)
API_URL = "http://127.0.0.1:8001/optimize_price"

# Sidebar for API status and info
with st.sidebar:
    st.markdown("### 📊 API Information")
    
    # Check API status
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=2)
        st.success("✅ API Status: Connected")
        api_info = response.json()
        st.markdown(f"**Model R² Score:** {api_info.get('r_squared', 'N/A')}")
    except:
        st.error("❌ API Status: Disconnected")
        st.warning("Make sure the API server is running on http://127.0.0.1:8000")
    
    st.markdown("---")
    st.markdown("### 💡 How It Works")
    st.markdown("""
    1. Enter product details
    2. Input competitor prices
    3. Provide product metrics
    4. Get optimal price recommendation
    
    The model analyzes demand patterns and competitive landscape to recommend
    the price that maximizes your profit.
    """)
    
    st.markdown("---")
    st.markdown("### 📝 Model Features")
    st.markdown("""
    - **Unit Price Impact**: Negative correlation
    - **Product Score**: Higher scores increase demand
    - **Customer Count**: More customers = higher demand
    - **Competitor Analysis**: Tracks price ratios & differences
    - **Category Impact**: Category-specific pricing effects
    """)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 Product Details")
    
    # Category selection - Updated to match dataset
    category = st.selectbox(
        "Product Category",
        [
            "bed_bath_table",
            "computers_accessories",
            "consoles_games",
            "cool_stuff",
            "furniture_decor",
            "garden_tools",
            "health_beauty",
            "perfumery",
            "watches_gifts"
        ],
        help="Select the product category"
    )
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        cogs = st.number_input(
            "Cost of Goods Sold ($)",
            min_value=1.0,
            value=45.0,
            step=5.0,
            help="Production cost per unit"
        )
    
    with col1_2:
        freight = st.number_input(
            "Freight Cost ($)",
            min_value=0.0,
            value=15.0,
            step=1.0,
            help="Shipping/logistics cost per unit"
        )
    
    st.markdown("### 🏪 Competitor Prices")
    
    col1_3, col1_4, col1_5 = st.columns(3)
    with col1_3:
        comp1 = st.number_input(
            "Competitor 1 ($)",
            min_value=10.0,
            value=120.0,
            step=5.0,
            help="Price of competitor 1"
        )
    
    with col1_4:
        comp2 = st.number_input(
            "Competitor 2 ($)",
            min_value=10.0,
            value=150.0,
            step=5.0,
            help="Price of competitor 2"
        )
    
    with col1_5:
        comp3 = st.number_input(
            "Competitor 3 ($)",
            min_value=10.0,
            value=100.0,
            step=5.0,
            help="Price of competitor 3"
        )

with col2:
    st.markdown("### ⭐ Product Metrics")
    
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        score = st.slider(
            "Product Score/Rating",
            min_value=1.0,
            max_value=5.0,
            value=4.2,
            step=0.1,
            help="Product quality/satisfaction rating (1-5)"
        )
    
    with col2_2:
        customers = st.number_input(
            "Customer Count",
            min_value=1,
            value=50,
            step=5,
            help="Number of potential customers"
        )
    
    st.markdown("### 📊 Price Range Analysis")
    
    # Calculate suggested ranges for user context
    min_suggested = cogs + freight + 10
    max_suggested = max(comp1, comp2, comp3) * 2
    avg_comp = (comp1 + comp2 + comp3) / 3
    
    col2_3, col2_4, col2_5 = st.columns(3)
    with col2_3:
        st.metric("Min Price", f"${min_suggested:.2f}")
    with col2_4:
        st.metric("Avg Competitor", f"${avg_comp:.2f}")
    with col2_5:
        st.metric("Max Price", f"${max_suggested:.2f}")
    
    st.info(
        f"The optimizer will analyze prices between ${min_suggested:.2f} and ${max_suggested:.2f}"
    )

# Optimize button - Full width
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    optimize_button = st.button(
        "🚀 Optimize Price Now",
        use_container_width=True,
        type="primary"
    )

# Display results
if optimize_button:
    with st.spinner("🔄 Analyzing demand patterns and market conditions..."):
        try:
            # Prepare request payload
            payload = {
                "category": category,
                "cogs": cogs,
                "freight": freight,
                "comp1": comp1,
                "comp2": comp2,
                "comp3": comp3,
                "score": score,
                "customers": customers
            }
            
            # Make API request
            response = requests.post(API_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for error response from API
                if 'error' in result:
                    st.error(f"❌ API Error: {result['error']}")
                else:
                    try:
                        # Display results in attractive format
                        st.success("✅ Optimization Complete!")
                        
                        # Main results cards
                        col_r1, col_r2, col_r3 = st.columns(3)
                        
                        with col_r1:
                            st.markdown("""
                            <div class="metric-card">
                                <h3 style="color: #FF1493; margin-top: 0;">💰 Optimal Price</h3>
                                <h2 style="color: #000; margin: 0;">${:.2f}</h2>
                            </div>
                            """.format(result['optimal_price']), unsafe_allow_html=True)
                        
                        with col_r2:
                            st.markdown("""
                            <div class="metric-card">
                                <h3 style="color: #FF1493; margin-top: 0;">📈 Max Profit</h3>
                                <h2 style="color: #000; margin: 0;">${:.2f}</h2>
                            </div>
                            """.format(result['max_profit']), unsafe_allow_html=True)
                        
                        with col_r3:
                            st.markdown("""
                            <div class="metric-card">
                                <h3 style="color: #FF1493; margin-top: 0;">📦 Predicted Qty</h3>
                                <h2 style="color: #000; margin: 0;">{:.2f} units</h2>
                            </div>
                            """.format(result['predicted_qty']), unsafe_allow_html=True)
                        
                        # Additional insights
                        st.markdown("---")
                        st.markdown("### 📊 Additional Insights")
                        
                        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
                        
                        with col_i1:
                            cost_base = cogs + freight
                            markup = ((result['optimal_price'] - cost_base) / cost_base * 100) if cost_base > 0 else 0
                            st.metric("Markup %", f"{markup:.1f}%")
                        
                        with col_i2:
                            price_vs_avg = ((result['optimal_price'] / avg_comp) - 1) * 100
                            st.metric("vs Avg Competitor", f"{price_vs_avg:+.1f}%")
                        
                        with col_i3:
                            total_revenue = result['optimal_price'] * result['predicted_qty']
                            st.metric("Total Revenue", f"${total_revenue:.2f}")
                        
                        with col_i4:
                            profit_margin = (result['max_profit'] / total_revenue * 100) if total_revenue > 0 else 0
                            st.metric("Profit Margin", f"{profit_margin:.1f}%")
                        
                        # Recommendation box
                        st.markdown("---")
                        st.markdown("""
                        <div class="result-box">
                            <h3>✨ Recommendation</h3>
                            <p style="font-size: 1.1em;">
                            Set your product price at <strong style="color: #FF1493; font-size: 1.3em;">${:.2f}</strong> 
                            to maximize profit at <strong style="color: #FF1493;">${:.2f}</strong> with an estimated 
                            demand of <strong>{:.2f} units</strong>.
                            </p>
                        </div>
                        """.format(result['optimal_price'], result['max_profit'], result['predicted_qty']), 
                        unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"❌ Error displaying results: {str(e)}")
                
                # Input summary
                with st.expander("📝 Summary of Inputs"):
                    summary = f"""
                    **Product Details:**
                    - Category: {category.capitalize()}
                    - COGS: ${cogs:.2f}
                    - Freight: ${freight:.2f}
                    
                    **Competitor Prices:**
                    - Competitor 1: ${comp1:.2f}
                    - Competitor 2: ${comp2:.2f}
                    - Competitor 3: ${comp3:.2f}
                    
                    **Product Metrics:**
                    - Rating: {score:.1f}/5.0
                    - Customer Count: {customers}
                    
                    **Analysis Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """
                    st.markdown(summary)
            
            else:
                st.error(f"API Error: {response.status_code}")
                st.error(f"Details: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API server")
            st.error("Please ensure the API is running on http://127.0.0.1:8000")
            st.info("Start the API with: `python api.py`")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #696969; font-size: 0.9em; margin-top: 50px;">
    <p>🚀 Fashionista Price Optimization Platform | Powered by Ridge Regression ML Model (R² = 0.9425)</p>
    <p><small>© 2025 Price Optimization Services | All Rights Reserved</small></p>
</div>
""", unsafe_allow_html=True)
