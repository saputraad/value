import streamlit as st

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="Value Investing Workstation",
    page_icon="📈",
    layout="wide"
)

# =====================================
# IMPORTS
# =====================================

from core.data_provider import (
    get_company_data
)

from engines.buffett_score import (
    BuffettScoreAnalyzer
)

from engines.valuation import (
    ValuationAnalyzer
)

from engines.buffett_decision import (
    BuffettDecisionAnalyzer
)

from engines.ranking import (
    BuffettRankingEngine
)

from components.debug_panel import (
    render_debug_panel
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title(
    "Value Investing Workstation"
)

ticker = st.sidebar.text_input(
    "Ticker",
    value="BBCA"
).upper()

DEBUG_MODE = st.sidebar.checkbox(
    "Developer Mode",
    value=False
)

# =====================================
# LOAD DATA
# =====================================

try:

    data = get_company_data(
        ticker
    )

except Exception as e:

    st.error(
        f"Failed loading data: {e}"
    )

    st.stop()

# =====================================
# ENGINE
# =====================================

try:

    buffett = (
        BuffettScoreAnalyzer(
            data
        )
        .summary()
    )

except:

    buffett = {}

try:

    valuation = (
        ValuationAnalyzer(
            data
        )
        .summary()
    )

except:

    valuation = {}

try:

    decision = (

        BuffettDecisionAnalyzer(

            business_score=
                buffett.get(
                    "buffett_score",
                    0
                ),

            valuation_score=
                valuation.get(
                    "valuation_score",
                    0
                )

        )
        .summary()

    )

except:

    decision = {}

# =====================================
# TABS
# =====================================

tabs = st.tabs([

    "📊 Dashboard",

    "🏢 Fundamental",

    "💰 Valuation",

    "🎯 Decision",

    "🏆 Ranking",

    "📈 Technical",

    "🐋 Bandarmology",

    "🛠 Debug"

])

# =====================================
# DASHBOARD
# =====================================

with tabs[0]:

    st.subheader(
        ticker
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Business Score",

            round(
                buffett.get(
                    "buffett_score",
                    0
                ),
                2
            )

        )

    with c2:

        st.metric(

            "Valuation Score",

            round(
                valuation.get(
                    "valuation_score",
                    0
                ),
                2
            )

        )

    with c3:

        st.metric(

            "Decision Score",

            round(
                decision.get(
                    "decision_score",
                    0
                ),
                2
            )

        )

    st.success(

        decision.get(
            "decision_rating",
            "-"
        )

    )

# =====================================
# FUNDAMENTAL
# =====================================

with tabs[1]:

    st.subheader(
        "Fundamental Analysis"
    )

    st.json(
        buffett
    )

# =====================================
# VALUATION
# =====================================

with tabs[2]:

    st.subheader(
        "Valuation Analysis"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Valuation Score",

            valuation.get(
                "valuation_score",
                0
            )

        )

    with c2:

        ey = valuation.get(
            "earnings_yield"
        )

        st.metric(

            "Earnings Yield",

            f"{ey*100:.2f}%"
            if ey is not None
            else "-"

        )

    with c3:

        fy = valuation.get(
            "fcf_yield"
        )

        st.metric(

            "FCF Yield",

            f"{fy*100:.2f}%"
            if fy is not None
            else "-"

        )

    st.divider()

    score = valuation.get(
        "valuation_score",
        0
    )

    st.progress(
        score / 100
    )

    st.caption(
        f"Valuation Strength : {score}/100"
    )

# =====================================
# DECISION
# =====================================

with tabs[3]:

    st.subheader(
        "Decision"
    )

    st.json(
        decision
    )

# =====================================
# RANKING
# =====================================

with tabs[4]:

    st.subheader(
        "Top Buffett Stocks"
    )

    st.info(
        "Ranking engine coming next."
    )

# =====================================
# TECHNICAL
# =====================================

with tabs[5]:

    st.subheader(
        "Technical Analysis"
    )

    st.info(
        "Technical engine coming next."
    )

# =====================================
# BANDARMOLOGY
# =====================================

with tabs[6]:

    st.subheader(
        "Bandarmology"
    )

    st.info(
        "Bandarmology engine coming next."
    )

# =====================================
# DEBUG
# =====================================

with tabs[7]:

    if DEBUG_MODE:

        render_debug_panel(
            data
        )

    else:

        st.info(
            "Enable Developer Mode"
        )
