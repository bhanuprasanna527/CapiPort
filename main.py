import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

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

for CSymbol, CName in zip(company_symbol, company_name):
    company_dict[CName] = CSymbol

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

com_sel = [company_dict[i] for i in com_sel_name]

num_tick = len(com_sel)

if num_tick > 1:

    com_data = yf.download(com_sel, start="1900-01-01", end="2024-03-08")["Adj Close"]
    com_data.dropna(inplace=True)

    com_sel = com_data.columns.to_list()
    com_sel_name.sort()

    st.dataframe(com_data, use_container_width=True)

    ## Log-Return of Company Dataset
    log_return = np.log(1 + com_data.pct_change())

    ## Generate Random Weights
    rand_weig = np.array(np.random.random(num_tick))

    ## Rebalancing Random Weights
    rebal_weig = rand_weig / np.sum(rand_weig)

    ## Calculate the Expected Returns, Annualize it by * 247.0
    exp_ret = np.sum((log_return.mean() * rebal_weig) * 247)

    ## Calculate the Expected Volatility, Annualize it by * 247.0
    exp_vol = np.sqrt(np.dot(rebal_weig.T, np.dot(log_return.cov() * 247, rebal_weig)))

    ## Calculate the Sharpe Ratio.
    sharpe_ratio = exp_ret / exp_vol

    # Put the weights into a data frame to see them better.
    weights_df = pd.DataFrame(
        data={
            "company_name": com_sel_name,
            "random_weights": rand_weig,
            "rebalance_weights": rebal_weig,
        }
    )

    st.divider()

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

    st.divider()

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

    ## Let's start the Monte Carlo Simulation

    for ind in range(num_of_port):
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
            "company_name": com_sel_name,
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
            "company_name": com_sel_name,
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

    fig = go.Figure(
        data=go.Scatter(
            x=sim_df["Volatility"],
            y=sim_df["Returns"],
            mode="markers",
            marker=dict(color=sim_df["Sharpe Ratio"], colorscale="RdYlBu", size=10),
        )
    )

    # Add color bar
    fig.update_layout(coloraxis_colorbar=dict(title="Sharpe Ratio"))

    # Add title and axis labels
    fig.update_layout(
        title="Portfolio Returns Vs. Risk",
        xaxis=dict(title="Standard Deviation / Volatility"),
        yaxis=dict(title="Returns"),
    )

    # Plot the Max Sharpe Ratio, using a `Red Star`.
    fig.add_trace(
        go.Scatter(
            x=[max_sharpe_ratio[1]],
            y=[max_sharpe_ratio[0]],
            mode="markers",
            marker=dict(color="red", symbol="star", size=20),
            name="Max Sharpe Ratio",
        )
    )

    # Plot the Min Volatility, using a `Blue Star`.
    fig.add_trace(
        go.Scatter(
            x=[min_volatility[1]],
            y=[min_volatility[0]],
            mode="markers",
            marker=dict(color="blue", symbol="star", size=20),
            name="Min Volatility",
        )
    )

    st.plotly_chart(fig, use_container_width=True)
