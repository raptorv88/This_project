import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Portfolio Dashboard", layout="wide")

st.title("📊 Portfolio Analysis Dashboard")

# =========================
# LOAD EXCEL FILE
# =========================

excel_file = "portfolio.xlsx"

try:
    # Diversification starts from row 8
    div_df = pd.read_excel(excel_file, sheet_name="Diversification", header=7)

    # Clutter starts from row 9
    clutter_df = pd.read_excel(excel_file, sheet_name="Clutter", header=8)

    # Portfolio Balance starts from row 7
    balance_df = pd.read_excel(excel_file, sheet_name="Porfolio Balance", header=6)

    # Risk sheet
    risk_df = pd.read_excel(excel_file, sheet_name="Risk Vs Reward (Equity)", header=7)

    # Clean column names
    div_df.columns = div_df.columns.astype(str).str.strip()
    clutter_df.columns = clutter_df.columns.astype(str).str.strip()
    balance_df.columns = balance_df.columns.astype(str).str.strip()
    risk_df.columns = risk_df.columns.astype(str).str.strip()

    # Remove Unnamed columns
    div_df = div_df.loc[:, ~div_df.columns.str.contains("Unnamed")]
    clutter_df = clutter_df.loc[:, ~clutter_df.columns.str.contains("Unnamed")]
    balance_df = balance_df.loc[:, ~balance_df.columns.str.contains("Unnamed")]
    risk_df = risk_df.loc[:, ~risk_df.columns.str.contains("Unnamed")]

except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# =========================
# DIVERSIFICATION
# =========================

st.header("📌 Diversification")

div_clean = div_df.iloc[:-1]
st.dataframe(div_clean, use_container_width=True)

# =========================
# PORTFOLIO TOTALS
# =========================

st.subheader("📊 Portfolio Totals")

div_clean["Invested Amount"] = pd.to_numeric(
    div_clean["Invested Amount"], errors="coerce"
)

div_clean["Current Amount"] = pd.to_numeric(
    div_clean["Current Amount"], errors="coerce"
)

total_invested = div_clean["Invested Amount"].sum()
total_current = div_clean["Current Amount"].sum()

st.write(f"**Total Invested Amount = ₹ {total_invested:,.2f}**")
st.write(f"**Total Current Amount = ₹ {total_current:,.2f}**")

# =========================
# CORE / SATELLITE / TAIL
# =========================

st.header("📊 Core / Satellite / Tail Allocation")

clutter_clean = clutter_df.iloc[:-1]

category_col = None
for col in clutter_clean.columns:
    if "holding" in col.lower() or "category" in col.lower():
        category_col = col

current_col = None
for col in clutter_clean.columns:
    if "current" in col.lower():
        current_col = col

if category_col is None or current_col is None:
    st.error("Required columns not found in Clutter sheet.")
    st.write("Available columns:", clutter_clean.columns.tolist())
else:
    clutter_clean[current_col] = pd.to_numeric(
        clutter_clean[current_col], errors="coerce"
    )

    category_data = clutter_clean.groupby(category_col)[current_col].sum()

    st.subheader("Category Wise Current Amount")
    st.dataframe(category_data.reset_index(), use_container_width=True)

    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(category_data, labels=category_data.index, autopct='%1.1f%%')
    ax1.set_title("Core / Satellite / Tail Distribution")
    st.pyplot(fig1)

# =========================
# SECTOR ALLOCATION
# =========================

st.header("🏭 Sector Allocation")

balance_clean = balance_df.iloc[:-1]

sector_col = None
for col in balance_clean.columns:
    if "sector" in col.lower():
        sector_col = col

current_balance_col = None
for col in balance_clean.columns:
    if "current" in col.lower():
        current_balance_col = col

if sector_col is None or current_balance_col is None:
    st.error("Required columns not found in Portfolio Balance sheet.")
    st.write("Available columns:", balance_clean.columns.tolist())
else:
    balance_clean[current_balance_col] = pd.to_numeric(
        balance_clean[current_balance_col], errors="coerce"
    )

    sector_data = balance_clean.groupby(sector_col)[current_balance_col].sum()

    st.subheader("Sector Wise Current Amount")
    st.dataframe(sector_data.reset_index(), use_container_width=True)

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.pie(sector_data, labels=sector_data.index, autopct='%1.1f%%')
    ax2.set_title("Sector Distribution")
    st.pyplot(fig2)

# =========================
# RISK VS REWARD
# =========================

st.header("💰 Risk Vs Reward (Equity)")
st.dataframe(risk_df, use_container_width=True)
