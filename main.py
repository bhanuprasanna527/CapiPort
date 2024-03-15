import yfinance as yf
import numpy as np
import pandas as pd

import streamlit as st

from utilities.py.styling import streamlit_style
from utilities.py import plots
from utilities.py import summary_tables

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

import plotly.express as px
import plotly.graph_objects as go

streamlit_style()

company_list_df = pd.read_csv("utilities/data/Company List.csv")

company_name = company_list_df["Name"].to_list()
company_symbol = (company_list_df["Ticker"] + ".NS").to_list()

name_to_symbol_dict = dict()
symbol_to_name_dict = dict()

start_date = 0
initial_investment = 0

streamlit_company_list_input = 0
optimization_methods = 0

for CSymbol, CName in zip(company_symbol, company_name):
    name_to_symbol_dict[CName] = CSymbol

for CSymbol, CName in zip(company_symbol, company_name):
    symbol_to_name_dict[CSymbol] = CName

col1, col2 = st.columns([4, 6])

with col1:
    st.write("##")
    st.write("Select Multiple Companies", unsafe_allow_html=True)
with col2:
    streamlit_company_list_input = st.multiselect("", company_name, default=None)

with col1:
    st.write("##")
    st.write("Select an Optimsation Technique", unsafe_allow_html=True)
with col2:
    optimization_methods = st.selectbox(
        "",
        (
            "Maximum Sharpe Ratio",
            "Efficient Risk",
            "Minimum Volatility",
            "Efficient Return",
        ),
    )

company_name_to_symbol = [name_to_symbol_dict[i] for i in streamlit_company_list_input]

number_of_symbols = len(company_name_to_symbol)

with col1:
    st.write("##")
    st.write("Start Date")
with col2:
    start_date = st.date_input(
        "",
        format="YYYY-MM-DD",
        value=pd.Timestamp("1947-08-15"),
        max_value=pd.Timestamp.now(),
    )

with col1:
    st.write("##")
    st.write("How much would you want to invest?")
with col2:
    initial_investment = st.number_input("", value=45000)

if number_of_symbols > 1:
    company_data = pd.DataFrame()

    for cname in company_name_to_symbol:
        stock_data_temp = yf.download(
            cname, start=start_date, end=pd.Timestamp.now().strftime("%Y-%m-%d")
        )["Adj Close"]
        stock_data_temp.name = cname
        company_data = pd.merge(
            company_data,
            stock_data_temp,
            how="outer",
            right_index=True,
            left_index=True,
        )

    for i in company_data.columns:
        company_data.dropna(axis=1, how="all", inplace=True)

    company_data.dropna(inplace=True)

    st.write(
        f"Note: Due to unavailability of full data, this Analysis uses data from the date: {company_data.index[0]}"
    )

    number_of_symbols = len(company_data.columns)

    st.dataframe(company_data, use_container_width=True)

    if number_of_symbols > 1:
        company_stock_returns_data = company_data.pct_change().dropna()

        mu = expected_returns.mean_historical_return(company_data)
        S = risk_models.sample_cov(company_data)

        ef = EfficientFrontier(mu, S)

        if optimization_methods == "Maximum Sharpe Raio":
            ef.max_sharpe()
        elif optimization_methods == "Minimum Volatility":
            ef.min_volatility()
        elif optimization_methods == "Efficient Risk":
            ef.efficient_risk(0.5)
        else:
            ef.efficient_return(0.05)

        company_asset_weights = pd.DataFrame.from_dict(
            ef.clean_weights(), orient="index"
        ).reset_index()

        company_asset_weights.columns = ["Ticker", "Allocation"]

        company_asset_weights_copy = company_asset_weights

        company_asset_weights["Name"] = [
            symbol_to_name_dict[i] for i in company_asset_weights["Ticker"]
        ]

        company_asset_weights = company_asset_weights[["Name", "Ticker", "Allocation"]]

        st.dataframe(company_asset_weights, use_container_width=True)

        ef.portfolio_performance()

        (
            expected_annual_return,
            annual_volatility,
            sharpe_ratio,
        ) = ef.portfolio_performance()

        st_portfolio_performance = pd.DataFrame.from_dict(
            {
                "Expected annual return": (expected_annual_return * 100).round(2),
                "Annual volatility": (annual_volatility * 100).round(2),
                "Sharpe ratio": sharpe_ratio.round(2),
            },
            orient="index",
        ).reset_index()

        st_portfolio_performance.columns = ["Metrics", "Summary"]

        st.write("Optimization Method - ", optimization_methods)

        st.dataframe(st_portfolio_performance, use_container_width=True)

        plots.pie_chart_company_asset_weights(company_asset_weights)

        portfolio_returns = (
            company_stock_returns_data * list(ef.clean_weights().values())
        ).sum(axis=1)

        annual_portfolio_returns = portfolio_returns.resample("Y").apply(
            lambda x: (x + 1).prod() - 1
        )

        cumulative_returns = (portfolio_returns + 1).cumprod() * initial_investment

        tab1, tab2 = st.tabs(["Plots", "Tables"])

        with tab1:
            plots.plot_annual_returns(annual_portfolio_returns)
            plots.plot_cummulative_returns(cumulative_returns)

        with tab2:
            summary_tables.annual_returns_dataframe(annual_portfolio_returns)
            summary_tables.cumulative_returns_dataframe(cumulative_returns)
