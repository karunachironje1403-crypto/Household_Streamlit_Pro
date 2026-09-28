import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Household Power Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
.hero {
    padding: 2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #eef6ff, #f8fbff);
    border: 1px solid #d9e8f7;
    margin-bottom: 1.5rem;
}
.hero h1 {margin-bottom: .3rem;}
.card {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    border: 1px solid #e4e8ee;
    background: white;
}
.small {color: #667085; font-size: .92rem;}
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).resolve().parent / "data" / "household_power_consumption.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, na_values=["?", "NA", "N/A"])
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")
        df["Hour"] = df["Time"].dt.hour
    numeric = [
        "Global_active_power", "Global_reactive_power", "Voltage",
        "Global_intensity", "Sub_metering_1", "Sub_metering_2",
        "Sub_metering_3"
    ]
    for col in numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    sub = [c for c in ["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"] if c in df.columns]
    if sub:
        df["Total_Submetering"] = np.sum(df[sub], axis=1)
    return df

st.sidebar.title("⚡ Household Power")
st.sidebar.markdown("### Navigation")
st.sidebar.info("Use the pages below to explore the dataset.")

if DATA_PATH.exists():
    df = load_data(DATA_PATH)
else:
    st.error("Dataset not found. Keep household_power_consumption.csv inside the data folder.")
    st.stop()

st.markdown("""
<div class="hero">
<h1>⚡ Household Power Consumption Analysis</h1>
<p>Explore household electricity usage through an interactive Streamlit dashboard.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Records", f"{len(df):,}")
c2.metric("Features", len(df.columns))
c3.metric("Missing Cells", f"{int(df.isna().sum().sum()):,}")
c4.metric(
    "Avg Active Power",
    f"{df['Global_active_power'].mean():.2f}" if "Global_active_power" in df else "N/A"
)

st.subheader("📌 Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

st.subheader("📅 Dataset Period")
if "Date" in df:
    st.write(f"**From:** {df['Date'].min().date()} &nbsp;&nbsp; **To:** {df['Date'].max().date()}")

st.markdown("""
### What this project contains
- **Introduction:** project objective, dataset information and features.
- **EDA:** interactive **Univariate, Bivariate and Multivariate** analysis buttons.
- **Conclusion:** key observations and practical interpretation.
""")
