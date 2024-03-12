import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import time
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
        f"On which date did you invested in - {i}",
        value= pd.Timestamp('2021-01-01'),
        format="YYYY-MM-DD",
    )
    d = d - datetime.timedelta(days=3)
    com_sel_date.append(d)

com_sel = [company_dict[i] for i in com_sel_name]

num_tick = len(com_sel)

if num_tick > 1:
    com_data = pd.DataFrame()
    for cname, cdate in zip(com_sel, com_sel_date):
        stock_data_temp = yf.download(cname, start=cdate, end=pd.Timestamp.now().strftime('%Y-%m-%d'))['Low']
        stock_data_temp.name = cname
        com_data = pd.merge(com_data, stock_data_temp, how="outer", right_index=True, left_index=True)
    for i in com_data.columns:
        com_data.dropna(axis=1, how='all', inplace=True)
    # com_data.dropna(inplace=True)
    num_tick = len(com_data.columns)

    # Dataframe of the selected companies
    st.dataframe(com_data, use_container_width=True)

    # make a function to calculate moving averages from the dataframe com_data, store those moving averages in dictionary for respective company
    def moving_average(data, window):
        ma = {}
        for i in data.columns:
            ma[i] = data[i].rolling(window=window).mean().values[2]
        return ma

    moving_avg = moving_average(com_data, 3)
    MA_df = pd.DataFrame(moving_avg.items(), columns=['Company', 'Purchase Rate (MA)'])

    # calculate percentage return till present date from the moving average price of the stock
    def percentage_return(data, moving_avg):
        pr = {}
        for i in data.columns:
            pr[i] = f'{round(((data[i].values[-1] - moving_avg[i]) / moving_avg[i]) * 100,2) }%'
        return pr
    
    # make percentage return a dataframe from dictionary
    percentage_return = pd.DataFrame(percentage_return(com_data, moving_avg).items(), columns=['Company', 'Percentage Return'])

    #merge MA_df and percentage_return on "Company" columns
    MA_df = pd.merge(MA_df, percentage_return, on='Company')

    st.markdown(
            "<h5 style='text-align: center;'>Percent Returns & MA price</h5>",
            unsafe_allow_html=True,
        )

    st.write("<p style='text-align: center;'>**rate of purchase is moving average(MA) of 3 (t+2) days</p>", unsafe_allow_html=True) 
    st.dataframe(MA_df,use_container_width=True)

    if num_tick > 1:
        com_sel_name_temp = []
        for i in com_data.columns:
            com_sel_name_temp.append(company_symbol_dict[i])

        com_sel = com_data.columns.to_list()

        ## Log-Return of Company Dataset
        log_return = np.log(1 + com_data.pct_change())

        ## Generate Random Weights
        rand_weig = np.array(np.random.random(num_tick))

        ## Rebalancing Random Weights
        rebal_weig = rand_weig / np.sum(rand_weig)

        ## Calculate the Expected Returns, Annualize it by * 252.0
        exp_ret = np.sum((log_return.mean() * rebal_weig) * 252)

        ## Calculate the Expected Volatility, Annualize it by * 252.0
        exp_vol = np.sqrt(np.dot(rebal_weig.T, np.dot(log_return.cov() * 252, rebal_weig)))

        ## Calculate the Sharpe Ratio.
        sharpe_ratio = exp_ret / exp_vol

        # Put the weights into a data frame to see them better.
        weights_df = pd.DataFrame(
            data={
                "company_name": com_sel_name_temp,
                "random_weights": rand_weig,
                "rebalance_weights": rebal_weig,
            }
        )

        st.markdown(
            "<h5 style='text-align: center;'>Random Portfolio Weights</h5>",
            unsafe_allow_html=True,
        )
        st.dataframe(weights_df, use_container_width=True)

        # Do the same with the other metrics.
        metrics_df = pd.DataFrame(
            data={
                "Expected Portfolio Returns": exp_ret,
                "Expected Portfolio Volatility": exp_vol,
                "Portfolio Sharpe Ratio": sharpe_ratio,
            },
            index=[0],
        )

        st.markdown(
            "<h5 style='text-align: center;'>Random Weights Metrics</h5>",
            unsafe_allow_html=True,
        )
        st.dataframe(metrics_df, use_container_width=True)


        ## Let's get started with Monte Carlo Simulations

        ## How many times should we run Monte Carlo
        num_of_port = 8000

        ## Create an Array to store the weights as they are generated
        all_weights = np.zeros((num_of_port, num_tick))

        ## Create an Array to store the returns as they are generated
        ret_arr = np.zeros(num_of_port)

        ## Create an Array to store the volatilities as they are generated
        vol_arr = np.zeros(num_of_port)

        ## Create an Array to store the Sharpe Ratios as they are generated
        sharpe_arr = np.zeros(num_of_port)

        ## Track Progress with a Bar
        progress_text = "Simulations in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        ## Let's start the Monte Carlo Simulation
        for ind in range(num_of_port):  # Corrected the range to iterate from 0 to num_of_port
            time.sleep(0.001)
            ## Let's first Calculate the Weights
            weig = np.array(np.random.random(num_tick))
            weig = weig / np.sum(weig)

            ## Append the Weights to Weigths array
            all_weights[ind, :] = weig

            ## Calculate and Append the Expected Log Returns to Returns Array
            ret_arr[ind] = np.sum((log_return.mean() * weig) * 247)

            ## Calculate and Append the Volatility to the Volatitlity Array
            vol_arr[ind] = np.sqrt(np.dot(weig.T, np.dot(log_return.cov() * 247, weig)))

            ## Calculate and Append the Sharpe Ratio to Sharpe Ratio Array
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]
            if ind % 100 == 0:
                my_bar.progress((ind + 1) / num_of_port, text=progress_text)
        # clear progress bar
        my_bar.empty()

        ## Let's create a Data Frame with Weights, Returns, Volatitlity, and the Sharpe Ratio
        sim_data = [ret_arr, vol_arr, sharpe_arr, all_weights]
        
        ## Create a Data Frame using above, then Transpose it
        sim_df = pd.DataFrame(data=sim_data).T

        ## Give the columns in Simulation Data Proper Names
        sim_df.columns = ["Returns", "Volatility", "Sharpe Ratio", "Portfolio Weights"]

        ## Make sure the Data Types are correct in the Data Frame
        sim_df = sim_df.infer_objects()

        # Print out the results.
        st.write("\n\n")
        st.markdown(
            "<h4 style='text-align: center;'>Simulation Results</h4>",
            unsafe_allow_html=True,
        )
        st.dataframe(sim_df.head(), use_container_width=True)

        # Return the Max Sharpe Ratio from the run.
        max_sharpe_ratio = sim_df.loc[sim_df["Sharpe Ratio"].idxmax()]

        # Return the Min Volatility from the run.
        min_volatility = sim_df.loc[sim_df["Volatility"].idxmin()]

        max_sharpe_weights_df = pd.DataFrame(
            data={
                "company_name": com_sel_name_temp,
                "random_weights": max_sharpe_ratio["Portfolio Weights"],
            }
        )

        st.markdown(
            "<h5 style='text-align: center;'>Portfolio with Max Sharpe Ratio</h5>",
            unsafe_allow_html=True,
        )
        st.dataframe(max_sharpe_ratio, use_container_width=True)
        st.dataframe(max_sharpe_weights_df, use_container_width=True)

        min_volatility_weights_df = pd.DataFrame(
            data={
                "company_name": com_sel_name_temp,
                "random_weights": min_volatility["Portfolio Weights"],
            }
        )

        st.markdown(
            "<h5 style='text-align: center;'>Portfolio with Min Volatility</h5>",
            unsafe_allow_html=True,
        )
        st.dataframe(min_volatility, use_container_width=True)
        st.dataframe(min_volatility_weights_df, use_container_width=True)

        st.divider()

        st.markdown("<h1 style='text-align: center;'>Plotting</h1>", unsafe_allow_html=True)


        # plot a pie chart using plotly for max sharpe ratio
        fig = go.Figure(
            data=go.Pie(
                labels=com_sel_name_temp,
                values=max_sharpe_ratio["Portfolio Weights"],
                hole=0.3,
                textinfo='percent+label', # Information to display on the pie slices
                hoverinfo='label+percent',# Information to display on hover
                marker=dict( line=dict(color='white', width=2)) 
            )
        )

        # update colors
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

        # update layout of the pie chart

        # Add color bar
        fig.update_layout(coloraxis_colorbar=dict(title="Sharpe Ratio"))

        # Add title and axis labels
        fig.update_layout(
            title="Portfolio Composition",
            showlegend=False,
            height=500,
            width=700,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        st.plotly_chart(fig, use_container_width=True)
