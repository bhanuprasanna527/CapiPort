import yfinance as yf

from scipy.optimize import minimize

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_historical_returns(tickers, start_date, end_date):
    """
    Fetch historical returns data for the given tickers.

    Args:
    - tickers: list of strings, tickers of assets
    - start_date: string, start date in the format 'YYYY-MM-DD'
    - end_date: string, end date in the format 'YYYY-MM-DD'

    Returns:
    - pandas DataFrame, historical returns data
    """
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()
    return returns

def get_risk_free_rate_india():
    """
    Get the risk-free rate for the Indian market using the yield of the 10-year Indian Government Bond.

    Returns:
    - float, risk-free rate
    """
    # Ticker symbol for the 10-year Indian Government Bond yield
    bond_ticker = 'INR=X'  # You can replace this with the actual ticker symbol for the bond

    # Fetch the bond data
    bond_data = yf.Ticker(bond_ticker)

    # Get the latest yield
    risk_free_rate_india = bond_data.history(period='1d')['Close'][-1] / 100
    return risk_free_rate_india

def sharpe_ratio(weights, returns, risk_free_rate):
    """
    Calculate the Sharpe Ratio of a portfolio.

    Args:
    - weights: array-like, weights of assets in the portfolio
    - returns: pandas DataFrame, historical returns of assets
    - risk_free_rate: float, risk-free rate of return

    Returns:
    - float, Sharpe Ratio of the portfolio
    """
    portfolio_return = np.sum(weights * returns.mean() * 252)  # 252 trading days in a year
    portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return -sharpe_ratio  # Minimize negative Sharpe Ratio for maximization



def optimize_portfolio(returns, risk_free_rate):
    """
    Optimize portfolio to maximize the Sharpe Ratio.

    Args:
    - returns: pandas DataFrame, historical returns of assets
    - risk_free_rate: float, risk-free rate of return

    Returns:
    - array, optimal weights of assets in the portfolio
    """
    num_assets = len(returns.columns)
    initial_weights = np.array([1 / num_assets] * num_assets)
    bounds = [(0, 1)] * num_assets  # Bounds for asset weights (0 <= weight <= 1)
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})  # Sum of weights equals 1 constraint

    optimized_result = minimize(sharpe_ratio, initial_weights, args=(returns, risk_free_rate),
                                method='SLSQP', bounds=bounds, constraints=constraints)

    return optimized_result.x