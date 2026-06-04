import streamlit as st


def render_ranking_table(ranking):

    st.subheader(
        "🏆 Buffett Ranking"
    )

    st.dataframe(
        ranking,
        use_container_width=True
    )
