import yfinance as yf
import numpy as np
import pandas as pd

import streamlit as st

from utilities.py.styling import streamlit_style

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

        company_name_to_symbol_temp = [symbol_to_name_dict[i] for i in company_data.columns]

        company_name_to_symbol = company_data.columns.to_list()

        ## Log-Return of Company Dataset
        log_return = np.log(1 + company_data.pct_change())

        ## Generate Random Weights
        rand_weig = np.array([100 / len(company_name_to_symbol)] * len(company_name_to_symbol))
        ## Rebalancing Random Weights
        rebal_weig = rand_weig / np.sum(rand_weig)

        ## Calculate the Expected Returns, Annualize it by * 252.0
        exp_ret = np.sum((log_return.mean() * rebal_weig) * 252)

        ## Calculate the Expected Volatility, Annualize it by * 252.0
        exp_vol = np.sqrt(
            np.dot(rebal_weig.T, np.dot(log_return.cov() * 252, rebal_weig))
        )

        ## Calculate the Sharpe Ratio.
        sharpe_ratio = exp_ret / exp_vol

        
