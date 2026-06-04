import streamlit as st


def render_debug_panel(

    data,

    quality=None,

    moat=None,

    predictability=None,

    trajectory=None,

    cashflow=None,

    buffett=None,

    valuation=None,

    decision=None

):

    st.subheader(
        "Debug Center"
    )

    # =====================
    # RAW DATA
    # =====================

    with st.expander(
        "Raw Data"
    ):

        st.write(
            data.keys()
        )

    # =====================
    # BUSINESS COMPONENTS
    # =====================

    with st.expander(
        "Business Components"
    ):

        st.json({

            "quality":
                quality,

            "moat":
                moat,

            "predictability":
                predictability,

            "trajectory":
                trajectory,

            "cashflow":
                cashflow

        })

    # =====================
    # BUFFETT
    # =====================

    with st.expander(
        "Buffett Score"
    ):

        st.json(
            buffett
        )

    # =====================
    # VALUATION
    # =====================

    with st.expander(
        "Valuation"
    ):

        st.json(
            valuation
        )

    # =====================
    # DECISION
    # =====================

    with st.expander(
        "Decision"
    ):

        st.json(
            decision
        )
