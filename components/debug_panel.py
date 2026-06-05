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

    with st.expander(
        "Raw Data"
    ):

        st.write(
            data.keys()
        )

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

    with st.expander(
        "Buffett Score"
    ):

        st.json(
            buffett
        )

    with st.expander(
        "Valuation"
    ):

        st.json(
            valuation
        )

    with st.expander(
        "Decision"
    ):

        st.json(
            decision
        )

    with st.expander(
        "Financial Statement Rows"
    ):

        if data.get(
            "income_statement"
        ) is not None:

            st.write(
                data[
                    "income_statement"
                ]
                .index
                .tolist()
            )

        if data.get(
            "cashflow"
        ) is not None:

            st.write(
                data[
                    "cashflow"
                ]
                .index
                .tolist()
            )

    with st.expander(
        "Valuation Debug"
    ):
    
        st.write(
            "market_cap"
        )
    
        st.write(
            data.get(
                "market_cap"
            )
        )
    
        st.write(
            "info.marketCap"
        )
    
        st.write(
            data.get(
                "info",
                {}
            ).get(
                "marketCap"
            )
        )
    
        st.write(
            "financialCurrency"
        )
    
        st.write(
            data.get(
                "info",
                {}
            ).get(
                "financialCurrency"
            )
        )

    with st.expander(
        "Data Provider Audit"
    ):
    
        st.write(
            data.keys()
        )
    
        info = data.get(
            "info",
            {}
        )
    
        st.json({
    
            "marketCap":
                info.get(
                    "marketCap"
                ),
    
            "financialCurrency":
                info.get(
                    "financialCurrency"
                ),
    
            "currency":
                info.get(
                    "currency"
                ),
    
            "longName":
                info.get(
                    "longName"
                )
    
        })

    fast = get_fast_info(
        ticker
    )
    
    st.json({
    
        "market_cap":
            fast.get(
                "market_cap"
            ),
    
        "shares":
            fast.get(
                "shares"
            ),
    
        "last_price":
            fast.get(
                "lastPrice"
            )
    
    })
