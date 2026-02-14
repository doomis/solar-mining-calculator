import streamlit as st

# Miner Specifications: [Hashrate in TH/s, Power in Watts]
MINER_SPECS = {
    'Antminer S21': {'hashrate': 200, 'power': 3500},
    'Whatsminer M60S': {'hashrate': 186, 'power': 3600}
}

st.set_page_config(page_title="Solar BTC Mining Calculator", page_icon="⚡")
st.title("☀️ Solar Bitcoin Mining Economics")

# --- Inputs (Sidebar) ---
st.sidebar.header("Configuration")

solar_size = st.sidebar.number_input("Solar System Size (kW)", value=10.0, step=1.0)
miner_model = st.sidebar.selectbox("Miner Model", list(MINER_SPECS.keys()))
miner_qty = st.sidebar.number_input("Miner Quantity", value=1, min_value=1, step=1)
grid_cost = st.sidebar.number_input("Electricity Cost (Grid) ($/kWh)", value=0.12, step=0.01)
btc_price = st.sidebar.number_input("Bitcoin Price ($)", value=95000, step=1000)
hashprice = st.sidebar.number_input("Network Hashprice ($/TH/day)", value=0.08, format="%.4f")

# --- Logic Core ---
spec = MINER_SPECS[miner_model]
total_hashrate = spec['hashrate'] * miner_qty
total_watts = spec['power'] * miner_qty

# Calculate Daily Revenue: (Total Hashrate * Hashprice)
daily_revenue = total_hashrate * hashprice

# Calculate Daily Cost: (Total Watts / 1000 * 24 hours * Grid Cost)
daily_cost = (total_watts / 1000) * 24 * grid_cost

# Calculate Net Profit: Revenue - Cost
net_profit = daily_revenue - daily_cost

# --- Visuals ---
st.subheader("Daily Performance Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Daily Revenue", f"${daily_revenue:.2f}")
col2.metric("Daily Power Cost", f"${daily_cost:.2f}")
col3.metric("Net Profit", f"${net_profit:.2f}", delta=f"{net_profit:.2f}")

if net_profit < 0:
    st.warning("⚠️ Unprofitable at current Grid Rates")
else:
    st.success("✅ Operation is currently profitable!")

# Summary Table
st.write("---")
st.write(f"**Operational Stats:** {total_hashrate} TH/s total power consuming {total_watts/1000:.2f} kW continuous load.")
