import yfinance as yf
import numpy as np
import pandas as pd

import streamlit as st

from utilities.py.styling import streamlit_style

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

import plotly.express as px
import plotly.graph_objects as go

streamlit_style()

company_list_df = pd.read_csv('utilities/data/Company List.csv')

company_name = company_list_df["Name"].to_list()
company_symbol = (company_list_df["Ticker"] + ".NS").to_list()

name_to_symbol_dict = dict()
symbol_to_name_dict = dict()

for CSymbol, CName in zip(company_symbol, company_name):
    name_to_symbol_dict[CName] = CSymbol

for CSymbol, CName in zip(company_symbol, company_name):
    symbol_to_name_dict[CSymbol] = CName

streamlit_company_list_input = st.multiselect("", company_name, default=None)

company_name_to_symbol = [name_to_symbol_dict[i] for i in streamlit_company_list_input]

number_of_symbols = len(company_name_to_symbol)

initial_investment = st.number_input('How much would you want to invest?', value = 100000)

if number_of_symbols > 1:

    company_data = pd.DataFrame()

    for cname in company_name_to_symbol:
        stock_data_temp = yf.download(
            cname, start="1900-01-01", end=pd.Timestamp.now().strftime("%Y-%m-%d")
        )["Adj Close"]
        stock_data_temp.name = cname
        company_data = pd.merge(
            company_data, stock_data_temp, how="outer", right_index=True, left_index=True
        )
    
    for i in company_data.columns:
        company_data.dropna(axis=1, how="all", inplace=True)
    
    company_data.dropna(inplace=True)

    st.write(f"Note: Due to unavailability of full data, this Analysis uses data from the date: {company_data.index[0]}")

    number_of_symbols = len(company_data.columns)

    st.dataframe(company_data, use_container_width=True)

    if number_of_symbols > 1:

        company_stock_returns_data = company_data.pct_change().dropna()
        # annual_returns = .resample('Y').ffill().pct_change()

        mu = expected_returns.mean_historical_return(company_data)
        S = risk_models.sample_cov(company_data)

        ef = EfficientFrontier(mu, S)
        ef.max_sharpe()

        company_asset_weights = pd.DataFrame.from_dict(ef.clean_weights(), orient = "index").reset_index()

        company_asset_weights.columns = ['Ticker', 'Allocation']

        company_asset_weights_copy = company_asset_weights

        company_asset_weights['Name'] = [symbol_to_name_dict[i] for i in company_asset_weights['Ticker']]

        company_asset_weights = company_asset_weights[['Name', 'Ticker', 'Allocation']]

        st.dataframe(company_asset_weights, use_container_width=True)

        expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance()

        st_portfolio_performance = pd.DataFrame.from_dict({'Expected annual return': (expected_annual_return*100).round(2),
        'Annual volatility':(annual_volatility*100).round(2),
        'Sharpe ratio':sharpe_ratio.round(2)}, orient = "index").reset_index()

        st_portfolio_performance.columns = ['Metrics', 'Summary']

        st.dataframe(st_portfolio_performance, use_container_width = True)

        # Create pie chart
        fig = go.Figure(data=[go.Pie(labels=company_asset_weights['Name'], 
                              values=company_asset_weights['Allocation'],
                              marker=dict(colors=px.colors.qualitative.Light24),
                              textposition='inside',
                              pull=[0.1]*len(company_asset_weights),
                              textinfo='percent+label')])

        fig.update_layout(title='Asset Allocation',
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            autosize=True,
                            width=700,
                            height=600)
        
        fig.update_traces(
            marker=dict(
                colors=[
                    "lightseagreen",
                    "lightcoral",
                    "lightskyblue",
                    "lightgreen",
                    "lightpink",
                    "lightyellow",
                    "lightblue",
                    "lightgrey",
                    "lightgoldenrodyellow",
                    "lightcyan",
                ]
            )
        )
        
        st.plotly_chart(fig)
        
        portfolio_returns = (company_stock_returns_data * list(ef.clean_weights().values())).sum(axis=1)

        annual_portfolio_returns = portfolio_returns.resample('Y').apply(lambda x: (x + 1).prod() - 1)

        cumulative_returns = (portfolio_returns + 1).cumprod() * initial_investment

        # Plot annual returns using Plotly
        annual_returns_fig = go.Figure(data=[go.Bar(x=annual_portfolio_returns.index.year,
                                                    y=annual_portfolio_returns.values,
                                                    marker_color='skyblue',opacity=0.7)])
        annual_returns_fig.update_layout(title='Annual Returns of Portfolio',
                                        xaxis_title='Year',
                                        yaxis_title='Return',
                                        xaxis=dict(tickmode='linear'),
                                        yaxis=dict(tickformat=".2%"))

        # Plot cumulative returns using Plotly
        cumulative_returns_fig = go.Figure(data=go.Scatter(x=cumulative_returns.index,
                                                            y=cumulative_returns.values,
                                                            mode='lines',
                                                            marker=dict(color='skyblue')))
        cumulative_returns_fig.update_layout(title='Cumulative Returns of Portfolio',
                                            xaxis_title='Date',
                                            yaxis_title='Value (Rupees)',
                                            xaxis=dict(rangeslider=dict(visible=True)),
                                            yaxis=dict(tickformat=".2f"))

        # Display both plots
        st.plotly_chart(annual_returns_fig)
        st.plotly_chart(cumulative_returns_fig)

