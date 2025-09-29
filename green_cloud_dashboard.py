import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
NUM_SERVERS = 5
MAX_POWER = 200  # Watts at 100% utilization
IDLE_POWER = 50  # Watts when idle (server on but barely used)

def simulate_servers():
    servers = []
    for i in range(NUM_SERVERS):
        utilization = random.randint(0, 100)  # random CPU utilization %
        if utilization > 0:
            energy = IDLE_POWER + (utilization / 100) * (MAX_POWER - IDLE_POWER)
        else:
            energy = 0
        servers.append({
            "Server": f"Server-{i+1}",
            "Utilization (%)": utilization,
            "Energy (Watts)": round(energy, 2),
            "Status": "Idle ⚠️ (Wasted Energy)" if utilization < 20 and utilization > 0 else 
                      ("Off 📴" if utilization == 0 else "Active ✅")
        })
    return pd.DataFrame(servers)

# ---------- STREAMLIT APP ----------
st.set_page_config(page_title="Green Cloud Dashboard", layout="wide")

st.title("🌱 Green Cloud Usage Dashboard")
st.write("Simulating cloud servers with CPU utilization and energy consumption.")

if st.button("🔄 Refresh Simulation"):
    st.session_state.df = simulate_servers()

# Initialize dataframe if first run
if "df" not in st.session_state:
    st.session_state.df = simulate_servers()

df = st.session_state.df

# Display data table
st.subheader("📊 Server Energy Report")
st.dataframe(df, use_container_width=True)

# Visualization
st.subheader("📈 Utilization vs Energy")

fig, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(df["Server"], df["Utilization (%)"], color="skyblue")
ax1.set_ylabel("CPU Utilization (%)", fontsize=12)

# Highlight idle servers
for i, bar in enumerate(bars):
    if df["Status"].iloc[i].startswith("Idle"):
        bar.set_color("lightcoral")

# Energy line
ax2 = ax1.twinx()
ax2.plot(df["Server"], df["Energy (Watts)"], color="green", marker="o", linewidth=2, label="Energy (Watts)")
ax2.set_ylabel("Energy (Watts)", fontsize=12)
ax2.legend(loc="upper left")

ax1.set_title("Server Utilization & Energy Consumption", fontsize=14)
st.pyplot(fig)
