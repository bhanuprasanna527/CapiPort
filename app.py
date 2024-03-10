import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import datetime

with open(r"style/style.css") as css:
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

list_df = pd.read_csv("Data/Company List.csv")

company_name = list_df["Name"].to_list()
company_symbol = (list_df["Ticker"] + ".NS").to_list()

company_dict = dict()
company_symbol_dict = dict()

for CSymbol, CName in zip(company_symbol, company_name):
    company_dict[CName] = CSymbol

for CSymbol, CName in zip(company_symbol, company_name):
    company_symbol_dict[CSymbol] = CName

st.markdown(
    """ 
    <style>
        .big-font {
        font-size:20px;
        }
    </style>""",
    unsafe_allow_html=True,
)

st.markdown('<p class="big-font">Select Multiple Companies</p>', unsafe_allow_html=True)

com_sel_name = st.multiselect("", company_name, default=None)
com_sel_date = []

for i in com_sel_name:
    d = st.date_input(
        f"Select your vacation for next year - {i}",
        format="YYYY-MM-DD",
    )
    com_sel_date.append(d)

com_sel = [company_dict[i] for i in com_sel_name]

num_tick = len(com_sel)

if num_tick > 1:

    com_data = pd.DataFrame()
    for cname, cdate in zip(com_sel, com_sel_date):
        stock_data_temp = yf.download(cname, start=cdate, end=pd.Timestamp.now().strftime('%Y-%m-%d'))
        com_data[cname] = stock_data_temp["Adj Close"]



