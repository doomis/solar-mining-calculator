import streamlit as st

# Miner Specifications
# S21 = 200 TH/s, 3500W; M60S = 186 TH/s, 3600W.
MINER_SPECS = {
    'Antminer S21': {'hashrate': 200, 'power': 3500},
    'Whatsminer M60S': {'hashrate': 186, 'power': 3600}
}

# Page configuration
st.set_page_config(
    page_title="Solar Bitcoin Miner Economics",
    page_icon="☀️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("☀️ Solar Bitcoin Mining Economics")
st.markdown("---")

# Sidebar - Inputs
st.sidebar.header("System Inputs")

solar_size = st.sidebar.number_input("Solar System Size (kW)", value=10.0, step=1.0, help="Rated capacity of your solar installation.")
miner_model = st.sidebar.selectbox("Miner Model", options=list(MINER_SPECS.keys()))
miner_qty = st.sidebar.number_input("Miner Quantity", value=1, min_value=1, step=1)
grid_cost = st.sidebar.number_input("Electricity Cost (Grid) ($/kWh)", value=0.12, step=0.01, format="%.2f")
btc_price = st.sidebar.number_input("Bitcoin Price ($)", value=95000, step=500)
hashprice = st.sidebar.number_input("Network Hashprice ($/TH/day)", value=0.08, step=0.005, format="%.4f")

# Logic Core
spec = MINER_SPECS[miner_model]
total_hashrate = spec['hashrate'] * miner_qty
total_power_watts = spec['power'] * miner_qty

# Calculations
daily_revenue = total_hashrate * hashprice
daily_cost = (total_power_watts / 1000) * 24 * grid_cost
net_profit = daily_revenue - daily_cost

# Visual Appearance
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Daily Revenue", f"${daily_revenue:,.2f}")

with col2:
    st.metric("Daily Power Cost", f"${daily_cost:,.2f}")

with col3:
    st.metric(
        "Net Profit", 
        f"${net_profit:,.2f}", 
        delta=f"${net_profit:,.2f}",
        delta_color="normal" if net_profit >= 0 else "inverse"
    )

# Unprofitable Warning
if net_profit < 0:
    st.warning("⚠️ Unprofitable at current Grid Rates")

# Operation Summary
st.markdown("---")
st.subheader("Operational Summary")
d_col1, d_col2 = st.columns(2)

with d_col1:
    st.write(f"**Hardware:** {miner_qty}x {miner_model}")
    st.write(f"**Total Hashrate:** {total_hashrate:,.0f} TH/s")
    st.write(f"**Efficiency:** {spec['power']/spec['hashrate']:.2f} J/TH")

with d_col2:
    st.write(f"**Power Draw:** {total_power_watts:,.0f} Watts ({(total_power_watts/1000):.2f} kW)")
    st.write(f"**Solar Capacity:** {solar_size:,.2f} kWp")
    st.write("**Uptime:** 100% (Assume Grid Fallback)")

st.caption("Note: This V1 version assumes 100% grid uptime. Solar generation curves and battery storage are not yet modeled.")
