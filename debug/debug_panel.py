import streamlit as st


def render_debug_panel(data):

    st.header(
        "Debug Panel"
    )

    st.subheader(
        "Profile"
    )

    st.json(
        data["profile"]
    )

    st.subheader(
        "Income Statement Rows"
    )

    st.write(
        data["income_statement"].index.tolist()
    )

    st.subheader(
        "Balance Sheet Rows"
    )

    st.write(
        data["balance_sheet"].index.tolist()
    )

    st.subheader(
        "Cashflow Rows"
    )

    st.write(
        data["cashflow"].index.tolist()
    )
