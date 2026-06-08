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

    economic_stability=None,

    legacy_predictability=None

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
                economic_stability,
            
            "legacy_predictability":
                legacy_predictability,

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
        st.write(
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
            "TRAJECTORY TYPE"
        )
    
        st.write(
            type(
                trajectory
            )
        )
    
        st.write(
            trajectory
        )
    
        if isinstance(
            trajectory,
            dict
        ):
    
            st.json(
                trajectory.get(
                    "trajectory_debug",
                    {}
                )
            )

        st.json(

            buffett.get(
                "buffett_debug",
                {}
            )
        
        )

        st.json({

            "ticker": ticker,
        
            "sector":
                data.get(
                    "info",
                    {}
                ).get(
                    "sector"
                ),
        
            "industry":
                data.get(
                    "info",
                    {}
                ).get(
                    "industry"
                )
        
        })

   


