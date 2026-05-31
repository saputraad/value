import streamlit as st

from engines.scoring import (
    InvestmentScoringEngine
)

from engines.sector_classifier import (
    SectorClassifier
)

from engines.multibagger_screener import (
    MultibaggerAnalyzer
)

st.title(
    "Stock Intelligence Platform"
)

ticker = st.session_state.get(
    "ticker",
    "BBCA"
)

score = (
    InvestmentScoringEngine(
        ticker
    )
)

sector = (
    SectorClassifier(
        ticker
    )
)

multi = (
    MultibaggerAnalyzer(
        ticker
    )
)

col1,col2,col3,col4 = st.columns(4)

summary = score.summary()

with col1:

    st.metric(

        "Overall Score",

        summary.get(
            "overall_score"
        )
    )
    
with col2:

    st.metric(

        "Rating",

        summary.get(
            "recommendation"
        )
    )
    
with col3:

    st.metric(

        "Sector",

        sector.classify()
    )
    
with col4:

    st.metric(

        "Multibagger",

        multi.probability_rating()
    )
    
    st.subheader(
    "Score Breakdown"
)

scores = {

    "Value":
        summary.get(
            "value_score"
        ),

    "Growth":
        summary.get(
            "growth_score"
        ),

    "Quality":
        summary.get(
            "quality_score"
        ),

    "Risk":
        summary.get(
            "risk_score"
        ),

    "Technical":
        summary.get(
            "technical_score"
        )
}

st.bar_chart(scores)