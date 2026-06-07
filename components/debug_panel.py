import streamlit as st

from core.data_provider import (
    get_fast_info
)


def render_debug_panel(

    data,

    quality=None,

    moat=None,

    predictability=None,

    trajectory=None,

    cashflow=None,

    buffett=None,

    valuation=None,

    decision=None,

    data_health=None,

    consistency=None,

    economic_stability=None

):

    with st.expander(
        "Data Health"
    ):
    
        st.write(
            data_health
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
                cashflow,

            "economic_stability":
                economic_stability

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

    with st.expander(
        "Consistency Engine"
    ):
    
        st.write(
            "CONSISTENCY TYPE"
        )
        
        st.write(
            type(consistency)
        )
        
        st.write(
            consistency
        )

        data["cashflow"].index.tolist()



   


