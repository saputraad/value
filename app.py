import streamlit as st
from core.data_provider import get_company_data
from engines.growth import analyze_growth
from engines.quality import analyze_quality
from engines.risk import RiskAnalyzer
from engines.technical import TechnicalAnalyzer
from engines.recommendation import RecommendationEngine
from engines.sector_classifier import SectorClassifier
from engines.bank_valuation import BankValuationAnalyzer
from engines.data_audit import DataAudit
from engines.forecast import ForecastEngine
from engines.cashflow_quality import (
    CashflowQualityAnalyzer
)
from engines.fraud_detection import FraudDetectionAnalyzer
from engines.expected_return import (
    ExpectedReturnEngine
)

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
data = get_company_data(
    ticker
)
st.subheader("Balance Sheet Rows")

st.write(
    data["balance_sheet"].index.tolist()
)
st.write(
    data["income_statement"].index.tolist()
)

st.subheader("Cashflow Debug")
st.write(data["cashflow"])

audit = DataAudit(
    data
)

audit_result = audit.summary()

cashflow = CashflowQualityAnalyzer(
    data
).summary()

fraud = FraudDetectionAnalyzer(
    ticker
).summary()

st.subheader("Cashflow Score Debug")
st.json(cashflow)

st.subheader("Fraud Detection Debug")
st.json(fraud)

forecast = ForecastEngine(
    ticker,
    data
).summary()

st.write(
    "Forecast Debug",
    forecast
)

from engines.roic import (
    ROICAnalyzer
)

roic = ROICAnalyzer(
    data
).summary()

st.subheader(
    "ROIC Debug"
)

st.json(roic)

growth_debug = analyze_growth(
    data
)

current_price = data.get("price") if data else None
market_cap = data.get("market_cap") if data else None

profile = data.get("profile", {}) if data else {}


# ==========================================
# 2. PANGGIL ENGINE VALUASI
# ==========================================

valuation_results = {}

try:

    sector = SectorClassifier(
        ticker
    ).classify()

    if sector == "BANK":

        analyzer = BankValuationAnalyzer(
            ticker,
            data
        )

    else:

        analyzer = ValuationAnalyzer(
            ticker,
            data
        )

    valuation_results = (
        analyzer.summary()
    )

    st.subheader(
        "Valuation Debug"
    )

    st.json(
        valuation_results
    )

    st.subheader(
        "Profile Debug"
    )

    st.json({
        "market_cap": data.get(
            "market_cap"
        ),
        "shares": data.get(
            "shares_outstanding"
        ),
        "price": data.get(
            "price"
        )
    })

except Exception as e:

    st.sidebar.error(
        f"Valuation Engine Error: {e}"
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

    st.subheader("Investment Dashboard")

    try:

        rec_engine = RecommendationEngine(
            ticker=ticker,
            data=data,
            valuation_results=valuation_results
        )
        growth = analyze_growth(data)
        rec = rec_engine.summary()

        current_price = data.get("price")

        fair_value = valuation_results.get(
            "graham_value"
        )

        mos = valuation_results.get(
            "margin_of_safety"
        )

        recommendation = rec.get(
            "recommendation"
        )

        overall_score = rec.get(
            "overall_score"
        )

        business_quality = rec.get(
            "business_quality_score"
        )

        # ==========================
        # MAIN METRICS
        # ==========================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Current Price",
            f"Rp {current_price:,.0f}"
            if current_price else "-"
        )
        
        col2.metric(
            "Fair Value",
            f"Rp {fair_value:,.0f}"
            if fair_value else "-"
        )
        
        col3.metric(
            "Margin of Safety",
            f"{mos*100:.1f}%"
            if mos is not None else "-"
        )
        
        col4.metric(
            "Recommendation",
            recommendation
        )
        st.metric(
            "Business Quality",
            business_quality
        )
        st.markdown("---")
        st.write("### Interpretasi Detail")

        for item in growth.get(
            "commentary",
            []
        ):
            st.write(f"• {item}")

        # ==========================
        # SCORE BREAKDOWN
        # ==========================

        s1, s2, s3, s4, s5 = st.columns(5)

        s1.metric(
            "Valuation",
            rec["valuation_score"]
        )

        s2.metric(
            "Growth",
            rec["growth_score"]
        )

        s3.metric(
            "Quality",
            rec["quality_score"]
        )

        s4.metric(
            "Risk",
            rec["risk_score"]
        )

        s5.metric(
            "Technical",
            rec["technical_score"]
        )

        st.markdown("---")

        st.write(
            f"### Overall Score: {overall_score}/100"
        )

        st.progress(
            min(
                max(
                    overall_score / 100,
                    0
                ),
                1
            )
        )

    except Exception as e:

        st.error(
            f"Dashboard Error: {e}"
        )
# ==========================================
# 1. OVERVIEW
# ==========================================
with tabs[1]:

    st.subheader("Company Overview")

    st.write(
        "**Company Name:**",
        profile.get("name", "-")
    )

    st.write(
        "**Sector:**",
        profile.get("sector", "-")
    )

    st.write(
        "**Industry:**",
        profile.get("industry", "-")
    )

    st.write(
        "**Country:**",
        profile.get("country", "-")
    )

    st.write(
        "**Website:**",
        profile.get("website", "-")
    )

    st.write("---")

    st.write("Raw Profile Data")

    st.json(profile)

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

        # ==========================================
        # COMMENTARY
        # ==========================================

        st.markdown("---")

    except Exception as e:

        st.error(
            f"Growth Engine Error: {e}"
        )



# ==========================================
# 4. QUALITY
# ==========================================

with tabs[4]:

    st.subheader("Quality Analysis")

    try:

        quality = analyze_quality(data)

        roe = quality["roe"]
        roa = quality["roa"]
        debt = quality["debt_to_equity"]
        score = quality["quality_score"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "ROE",
            f"{roe*100:.2f}%"
            if roe is not None
            else "-"
        )

        col2.metric(
            "ROA",
            f"{roa*100:.2f}%"
            if roa is not None
            else "-"
        )

        col3.metric(
            "Debt / Equity",
            f"{debt:.2f}x"
            if debt is not None
            else "-"
        )

        col4.metric(
            "Quality Score",
            f"{score}/100"
        )

        st.markdown("---")

        if score >= 80:

            st.success(
                "Perusahaan berkualitas tinggi."
            )

        elif score >= 60:

            st.info(
                "Kualitas perusahaan cukup baik."
            )

        else:

            st.warning(
                "Kualitas perusahaan masih perlu diperhatikan."
            )

    except Exception as e:

        st.error(
            f"Quality Engine Error: {e}"
        )

# ==========================================
# 5. RISK
# ==========================================

with tabs[5]:

    st.subheader("Risk Analysis")

    try:

        risk = RiskAnalyzer(ticker)

        result = risk.summary()

        piotroski = result.get(
            "piotroski_score"
        )

        altman = result.get(
            "altman_z"
        )

        beneish = result.get(
            "beneish_m"
        )

        score = result.get(
            "risk_score"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Piotroski",
            piotroski if piotroski is not None else "-"
        )

        col2.metric(
            "Altman Z",
            altman if altman is not None else "-"
        )

        col3.metric(
            "Beneish M",
            beneish if beneish is not None else "-"
        )

        col4.metric(
            "Risk Score",
            score if score is not None else "-"
        )

        st.markdown("---")

        if score is not None:

            if score >= 80:

                st.success(
                    "Financial risk rendah."
                )

            elif score >= 60:

                st.info(
                    "Financial risk moderat."
                )

            else:

                st.warning(
                    "Financial risk cukup tinggi."
                )

    except Exception as e:

        st.error(
            f"Risk Engine Error: {e}"
        )

# ==========================================
# 6. TECHNICAL
# ==========================================

with tabs[6]:

    st.subheader("Technical Analysis")

    try:

        tech = TechnicalAnalyzer(ticker)

        result = tech.summary()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "MA20",
            f"{result['ma20']:,.0f}"
        )

        col2.metric(
            "MA50",
            f"{result['ma50']:,.0f}"
        )

        col3.metric(
            "MA200",
            f"{result['ma200']:,.0f}"
        )

        col4.metric(
            "RSI",
            f"{result['rsi']:.2f}"
        )

        st.markdown("---")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Trend",
            result["trend"]
        )

        c2.metric(
            "Golden Cross",
            "YES" if result["golden_cross"] else "NO"
        )

        c3.metric(
            "Entry Score",
            result["entry_score"]
        )

        st.markdown("---")

        if result["entry_score"] >= 80:

            st.success(
                "Timing entry sangat menarik."
            )

        elif result["entry_score"] >= 60:

            st.info(
                "Timing entry cukup baik."
            )

        else:

            st.warning(
                "Belum ideal untuk entry."
            )

    except Exception as e:

        st.error(
            f"Technical Error: {e}"
        )
# ==========================================
# 7. RECOMMENDATION
# ==========================================

with tabs[7]:

    st.subheader("Final Recommendation")

    try:

        engine = RecommendationEngine(
            ticker=ticker,
            data=data,
            valuation_results=valuation_results
        )

        result = engine.summary()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Overall Score",
            result["overall_score"]
        )

        col2.metric(
            "Recommendation",
            result["recommendation"]
        )

        col3.metric(
            "Risk Score",
            result["risk_score"]
        )

        st.markdown("---")

        st.write("### Score Breakdown")

        st.write(
            f"Valuation Score: {result['valuation_score']}"
        )

        st.write(
            f"Growth Score: {result['growth_score']}"
        )

        st.write(
            f"Quality Score: {result['quality_score']}"
        )

        st.write(
            f"Risk Score: {result['risk_score']}"
        )

        st.write(
            f"Technical Score: {result['technical_score']}"
        )

        st.markdown("---")

        recommendation = result[
            "recommendation"
        ]

        if recommendation == "STRONG BUY":

            st.success(
                "Sangat menarik untuk akumulasi."
            )

        elif recommendation == "BUY":

            st.success(
                "Layak dipertimbangkan untuk dibeli."
            )

        elif recommendation == "HOLD":

            st.info(
                "Fundamental cukup baik namun belum ideal untuk entry agresif."
            )

        else:

            st.warning(
                "Belum menarik berdasarkan kombinasi fundamental dan teknikal."
            )

    except Exception as e:

        st.error(
            f"Recommendation Engine Error: {e}"
        )
