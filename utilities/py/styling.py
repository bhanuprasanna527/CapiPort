import streamlit as st


def streamlit_style():
    with open(r"utilities/style/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align: center;'><u>CapiPort</u></h1>", unsafe_allow_html=True
    )

    st.markdown(
        "<h5 style='text-align: center; color: gray;'>Your Portfolio Optimisation Tool</h5>",
        unsafe_allow_html=True,
    )
    st.header(
        "",
        divider="rainbow",
    )

    color = "Quest"
    st.markdown(
        "<h1 style='text-align: center;'>🔍 Quest for financial excellence begins with meticulous portfolio optimization</u></h1>",
        unsafe_allow_html=True,
    )

    st.header(
        "",
        divider="rainbow",
    )

    st.markdown(
        """ 
        <style>
            .big-font {
            font-size:20px;
            }
        </style>""",
        unsafe_allow_html=True,
    )
