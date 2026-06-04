import streamlit as st


def render_debug_panel(data):

    st.subheader(
        "Debug Panel"
    )

    st.write(
        "Profile"
    )

    st.json(
        data.get(
            "profile",
            {}
        )
    )

    st.write(
        "Market Data"
    )

    st.json({

        "price":
            data.get(
                "price"
            ),

        "market_cap":
            data.get(
                "market_cap"
            ),

        "shares_outstanding":
            data.get(
                "shares_outstanding"
            )

    })

    if data.get(
        "income_statement"
    ) is not None:

        st.write(
            "Income Statement Rows"
        )

        st.write(
            data[
                "income_statement"
            ].index.tolist()
        )

    if data.get(
        "cashflow"
    ) is not None:

        st.write(
            "Cashflow Rows"
        )

        st.write(
            data[
                "cashflow"
            ].index.tolist()
        )
