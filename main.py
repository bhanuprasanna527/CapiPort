import CapiPort
import streamlit as st
import pandas as pd

df = pd.read_csv("EQUITY_L.csv")

CompanySymbol = (df["SYMBOL"] + '.NS').to_list()
CompanyName = df["NAME OF COMPANY"].to_list()

CompanyDict = dict()

for CSymbol, CName in zip(CompanySymbol, CompanyName):
    CompanyDict[CName] = CSymbol

EquitiesInvested = st.multiselect('Select Multiple Companies', CompanyName, default = None)

st.write("Need at Least two Companies to provide the Optimal Portfolio.")

if len(EquitiesInvested) > 1:
    EquitiesInvested = [CompanyDict[i] for i in EquitiesInvested]

    st.write(EquitiesInvested)

    equity_data = CapiPort.get_historical_returns(EquitiesInvested, "1900-01-01", "2024-03-04")

    risk_free_rate = CapiPort.get_risk_free_rate_india()

    optimal_weights = CapiPort.optimize_portfolio(equity_data, risk_free_rate)

    for i,j in zip(EquitiesInvested, optimal_weights):
        st.write(i, " : ", j)
