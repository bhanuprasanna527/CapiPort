import yfinance as yf

# 1. Check if the company is listed on Yahoo Finance
def check_company(company_dict):
    com_sel = []
    for i in company_dict.keys():
        if yf.Ticker(company_dict[i]).info:
                com_sel.append(i)

    return com_sel

#2. make a function to calculate moving averages from the dataframe com_data, store those moving averages in dictionary for respective company
def moving_average(data, window):
    ma = {}
    for i in data.columns:
        ma[i] = data[i].rolling(window=window).mean().values[2]
    return ma


# calculate percentage return till present date from the moving average price of the stock
def percentage_return(data, moving_avg):
    pr = {}
    for i in data.columns:
        pr[i] = f'{round(((data[i].values[-1] - moving_avg[i]) / moving_avg[i]) * 100,2) }%'
    return pr

