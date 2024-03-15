import streamlit as st
import pandas as pd
import numpy as np


def annual_returns_dataframe(annual_portfolio_returns):

    annual_portfolio_returns = annual_portfolio_returns * 100

    annual_portfolio_returns = annual_portfolio_returns.to_frame().reset_index()

    annual_portfolio_returns.columns = ["Year", "Return"]

    annual_portfolio_returns["Year"] = annual_portfolio_returns.Year.dt.year.astype(str)

    st.dataframe(annual_portfolio_returns, use_container_width=True)


def cumulative_returns_dataframe(cumulative_returns):

    cumulative_returns = cumulative_returns.to_frame().reset_index()

    cumulative_returns.columns = ["Year", "Balance"]

    cumulative_returns["Year"] = cumulative_returns["Year"].dt.year.astype(str)

    cumulative_returns = (
        cumulative_returns.groupby("Year").tail(1).reset_index().drop("index", axis=1)
    )

    st.dataframe(cumulative_returns, use_container_width=True)
