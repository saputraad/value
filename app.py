import streamlit as st
from core.data_provider import get_company_data
from engines.growth import analyze_growth

# Mengamankan import engine valuation Anda
try:
    from engines.valuation import ValuationAnalyzer
except Exception as e:
    ValuationAnalyzer = None

# ==========================================
# CONFIG & REFRESH MECHANISM
# ==========================================

st.set_page_config(
    page_title="IDX Investment Intelligence",
    page_icon="📈",
    layout="wide"
)

# Tombol untuk membersihkan cache jika data yfinance macet
if st.sidebar.button("🔄 Clear Cache & Force Reload"):
    st.cache_data.clear()
    st.rerun()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("IDX Investment Intelligence")

ticker_input = st.sidebar.text_input(
    "Kode Saham IDX",
    value="BBCA"
).upper().strip()

# Memastikan ticker selalu menggunakan akhiran .JK untuk pasar Indonesia
ticker = ticker_input if ticker_input.endswith(".JK") else f"{ticker_input}.JK"

# 1. Ambil data utama untuk Dashboard melalui data_provider
data = get_company_data(ticker)

current_price = data.get("price") if data else None
market_cap = data.get("market_cap") if data else None
info = data.get("info", {}) if data else {}

# ==========================================
# 2. PANGGIL ENGINE VALUASI
# ==========================================
valuation_results = {}
if ValuationAnalyzer and data:
    try:
        analyzer = ValuationAnalyzer(data)
        valuation_results = analyzer.summary()
    except Exception as val_err:
        st.sidebar.error(f"Engine Valuation bermasalah: {val_err}")

st.sidebar.markdown("---")
st.sidebar.info(
    """
    V1 Foundation
    Data Source: Yahoo Finance
    """
)

# ==========================================
# HEADER & TABS
# ==========================================

st.title("📈 IDX Investment Intelligence")
st.caption("Value Investing + Growth Investing + Quality Investing + Technical Analysis")

tabs = st.tabs([
    "Dashboard", "Overview", "Valuation", "Growth", "Quality", "Risk", "Technical", "Recommendation"
])

# ==========================================
# 0. DASHBOARD
# ==========================================
with tabs[0]:
    st.subheader("Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Price",
        f"Rp {current_price:,.0f}" if current_price else "-"
    )

    col2.metric(
        "Market Cap",
        f"{market_cap/1e12:.1f} T" if market_cap else "-"
    )

    col3.metric("Sector", info.get("sector", "-"))
    col4.metric("Industry", info.get("industry", "-"))

# ==========================================
# 1. OVERVIEW
# ==========================================
with tabs[1]:
    st.subheader("Company Overview")
    st.write("**Company Name:**", info.get("longName", "-"))
    st.write("**Sector:**", info.get("sector", "-"))
    st.write("**Industry:**", info.get("industry", "-"))
    st.write("**Country:**", info.get("country", "-"))
    st.write("**Business Summary:**", info.get("longBusinessSummary", "Tidak ada ringkasan bisnis."))

# ==========================================
# 2. VALUATION
# ==========================================
with tabs[2]:
    st.subheader("Valuation Analysis")

    if not valuation_results:
        st.warning("Gagal memuat kalkulasi dari engines/valuation.py")
    else:
        # Mengambil keys dari dict summary() milik valuation.py Anda
        v_price = valuation_results.get("current_price")
        graham = valuation_results.get("graham_value")
        mos = valuation_results.get("margin_of_safety")
        per = valuation_results.get("pe")
        pbv = valuation_results.get("pbv")
        v_score = valuation_results.get("value_score")
        
        # Mengubah nilai desimal MOS ke persen (contoh: 0.25 -> 25.0%)
        mos_pct = mos * 100 if mos is not None else None

        # Tampilan Metrik Utama
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Current Price", f"Rp {v_price:,.0f}" if v_price else "-")
        m_col2.metric("Graham Fair Value", f"Rp {graham:,.0f}" if graham else "-")
        
        if mos_pct is not None:
            m_col3.metric("Margin of Safety (MOS)", f"{mos_pct:.1f}%", delta=f"{mos_pct:.1f}%")
        else:
            m_col3.metric("Margin of Safety (MOS)", "-")
            
        m_col4.metric("Overall Value Score", f"{v_score}/100" if v_score else "-")

        st.markdown("---")
        
        # Tampilan Detail Model Multi-Valuasi
        st.write("### Model Rincian Valuasi")
        d_col1, d_col2, d_col3 = st.columns(3)
        
        with d_col1:
            st.info("**Benjamin Graham Formula**")
            st.write(f"- Intrinsic Value: **Rp {graham:,.0f}**" if graham else "- Intrinsic Value: N/A")
            st.write(f"- Trailing P/E Ratio: **{per:.2f}x**" if per else "- Trailing P/E Ratio: N/A")
            
        with d_col2:
            st.info("**Justified P/B Model**")
            j_pbv = valuation_results.get("justified_pbv")
            f_pbv = valuation_results.get("fair_value_pbv")
            st.write(f"- Justified PBV Target: **{j_pbv:.2f}x**" if j_pbv else "- Justified PBV Target: N/A")
            st.write(f"- Fair Value via PBV: **Rp {f_pbv:,.0f}**" if f_pbv else "- Fair Value via PBV: N/A")
            
        with d_col3:
            st.info("**Relative Valuation**")
            e_yield = valuation_results.get("earnings_yield")
            e_yield_pct = e_yield * 100 if e_yield else None
            st.write(f"- Current P/B Ratio: **{pbv:.2f}x**" if pbv else "- Current P/B Ratio: N/A")
            st.write(f"- Earnings Yield: **{e_yield_pct:.2f}%**" if e_yield_pct else "- Earnings Yield: N/A")

# ==========================================
# 3. GROWTH
# ==========================================

with tabs[3]:

    st.subheader("Growth Analysis")

    try:

        growth = analyze_growth(data)

        revenue = growth["revenue"]
        earnings = growth["earnings"]
        equity = growth["equity"]

        score = growth["growth_score"]

        col1, col2, col3, col4 = st.columns(4)

        revenue_pct = (
            revenue.get("revenue_cagr", 0) * 100
        )

        earnings_pct = (
            earnings.get("earnings_cagr", 0) * 100
        )

        equity_pct = (
            equity.get("equity_cagr", 0) * 100
        )

        col1.metric(
            "Revenue CAGR",
            f"{revenue_pct:.2f}%"
        )

        col2.metric(
            "Net Income CAGR",
            f"{earnings_pct:.2f}%"
        )

        col3.metric(
            "Equity CAGR",
            f"{equity_pct:.2f}%"
        )

        col4.metric(
            "Growth Score",
            f"{score}/100"
        )

        st.markdown("---")

        st.write("### Interpretasi")

        if score >= 80:

            st.success(
                "Perusahaan menunjukkan pertumbuhan sangat kuat."
            )

        elif score >= 60:

            st.info(
                "Pertumbuhan cukup baik."
            )

        else:

            st.warning(
                "Pertumbuhan masih kurang konsisten."
            )

    except Exception as e:

        st.error(
            f"Growth Engine Error: {e}"
        )

# ==========================================
# 4. QUALITY
# ==========================================

with tabs[4]:
    st.write("Coming soon...")

# ==========================================
# 5. RISK
# ==========================================

with tabs[5]:
    st.write("Coming soon...")

# ==========================================
# 6. TECHNICAL
# ==========================================

with tabs[6]:
    st.write("Coming soon...")

# ==========================================
# 7. RECOMMENDATION
# ==========================================

with tabs[7]:
    st.write("Coming soon...")
