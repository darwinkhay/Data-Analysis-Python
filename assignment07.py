# Assignment 07, STAT 3250

# Two *very* important rules that must be followed in order for your assignment
# to be graded correctly:

# a) The Python file name must be exactly "assignment00.py" with the correct two digit
# assignment number and without the quotes.
# b) The variables names like q1, q2, ... will be used to grade the assignment.
# They are initially set to `None` but you must set them equal to your final answer.
# If you don't know the answer, leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... variables.
# If your code throws an error, then the autograder will not be able to grade it, and
# you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

# The autograder's dataset will be slightly different from the one you are given.
# Make sure none of your answers are hard coded.


# Dataset

# The file Stocks.zip is a zip file containing nearly 100 data sets of price
# records for various stocks. Each file includes daily data for a specific
# stock, with stock ticker symbol given in the file name. Each line of
# a file includes the following:

#  Date = date for recorded information
#  Open = opening stock price
#  High = high stock price
#  Low = low stock price
#  Close = closing stock price
#  Volume = number of shares traded
#  Adj Close = closing price adjusted for stock splits (ignored for this assignment)

#  The time interval covered varies from stock to stock. For many files
#  there are dates when the market was open but the data is not provided, so
#  those records are missing. Note that some dates are not present because the
#  market is closed on weekends and holidays.  Those are not missing records.


# Preprocessing 1
from pathlib import Path
import pandas as pd
# Read in the datasets into a single dataframe using the `pathlib` library
all_stocks_list = []
all_stocks_tickers_list = []
stocks_path = Path.cwd() /"Stocks"

for i in stocks_path.iterdir():
    if i.is_file():
        file_name = i.name.replace('.csv', '')
        all_stocks_tickers_list.append(file_name)

    temp = pd.read_csv(i)
    temp['ticker'] = file_name
    
    all_stocks_list.append(temp)


all_stocks = pd.concat(all_stocks_list)
# The `Stocks` directory must be in the current working directory.
# 1. Set the index to be the dates as datetimes. You can drop the date column afterwards.
all_stocks['datetimes'] = pd.to_datetime(all_stocks['Date'])
all_stocks = all_stocks.set_index('datetimes')
all_stocks.drop('Date', axis=1, inplace=True)
# 2. Change all the column names to lowercase.
all_stocks.columns = all_stocks.columns.str.lower()
# 3. Add a `ticker` column to the dataset. For example, the ticker MSFT is for Microsoft.

# Step 1 will set the index to be a DatetimeIndex.
# This will allow us to use an offset with the rolling window method.
# This also means that we can now extract date information from the index like:
# ```
# df.index.year
# df.index.month
# ```
# The `dt` accessor is required for a DatetimeIndex.


# Question 1

# How many observations does each company have?
# Submit a series of the companies with the top 5 number of observations where the index is the
# ticker and the values are the counts.
# Be sure to include all ties and sort descending.
company_observations_counts = all_stocks.groupby('ticker').size().sort_values(ascending=False)
test = company_observations_counts.head(5)
q1 = company_observations_counts.nlargest(5, keep="all")


# Question 2

# Find the top-10 stocks (including ties) in terms of the average day-to-day volatility of the price,
# which we define to be the mean of the daily differences High - Low for each stock.
# Give your results as a Series with the ticker symbol as index and average day-to-day volatility as value.
# Sort the Series from highest to lowest average volatility.
all_stocks['daily_differences'] = all_stocks['high'] - all_stocks['low']
company_mean_daily_differences = all_stocks.groupby('ticker')['daily_differences'].mean().sort_values(ascending=False)
q2 = company_mean_daily_differences.nlargest(10, keep="all")


# Question 3

# Repeat the previous problem, this time using the relative volatility,
# which we define to be the mean of
# (High − Low)/(0.5(Open + Close))
# for each day. Provide your results as a Series with the same specifications
# as in the previous problem.
all_stocks['open_and_close'] = all_stocks['open'] + all_stocks['close']
all_stocks['relative_volatility'] = all_stocks['daily_differences']/(0.5*all_stocks['open_and_close'])
company_mean_relative_volatility = all_stocks.groupby('ticker')['relative_volatility'].mean().sort_values(ascending=False)
q3 = company_mean_relative_volatility.head(10)


# Question 4

# For each day the market was open in October 2008, find the average
# daily Open, High, Low, Close, and Volume for all stocks that have
# records for October 2008.  (Note: The market is open on a given
# date if there is a record for that date in any of the files.)
# Give your results as a DataFrame with dates as index and columns of
# means Open, High, Low, Close, Volume (in that order).  The dates should
# be sorted from oldest to most recent, with dates formatted (for example)
# 2008-10-01, the same form as in the files.
october_2008_stocks = all_stocks.query('datetimes.dt.year == 2008 and datetimes.dt.month == 10')
average_opens = october_2008_stocks.groupby('datetimes')['open'].mean()
average_highs = october_2008_stocks.groupby('datetimes')['high'].mean()
average_lows = october_2008_stocks.groupby('datetimes')['low'].mean()
average_closes = october_2008_stocks.groupby('datetimes')['close'].mean()
average_volumes = october_2008_stocks.groupby('datetimes')['volume'].mean()
averages_dictionary = {
    'open' : average_opens,
    'high' : average_highs,
    'low' : average_lows,
    'close': average_closes,
    'volume': average_volumes
    }
october_2008_stock_averages = pd.DataFrame(data=averages_dictionary).sort_index(ascending=False)
october_2008_stock_averages.index = october_2008_stock_averages.index.date

q4 = october_2008_stock_averages


# Preprocessing 2

# Now let's add rolling window calculations to the dataset!
# We want the 5 **calendar day** rolling averages for the open, high, low, close, and volume
# columns for each ticker.
# Unfortunately, I couldn't find an easy to add new rolling window columns to the `combined_df`
# using groupby + rolling.
# (If you figure this out, please let me know).

# So instead, let's revisit the preprocessing step and calculate them one ticker at a time.
# You can either edit your preprocessing step from before, or just repeat it with the new steps.
# If you edit you preprocessing step above, make sure your previous solutions don't change.
# Keep in mind that in order to use an offset window (as opposed to an integer window),
# the index must be datetimelike (from Preprocessing 1).

# Calculate the 5-day rolling averages of the open, high, low, close, and volume and add them
# as new columns named `rolling_*_5_days` where `*` is the original column name.
all_stocks.sort_index(axis=0, inplace=True)
all_stocks['rolling_open_5_days'] = all_stocks['open'].rolling('5D').mean()
all_stocks['rolling_high_5_days'] = all_stocks['high'].rolling('5D').mean()
all_stocks['rolling_low_5_days'] = all_stocks['low'].rolling('5D').mean()
all_stocks['rolling_close_5_days'] = all_stocks['close'].rolling('5D').mean()
all_stocks['rolling_volume_5_days'] = all_stocks['volume'].rolling('5D').mean()
# Ideally, your combined dataframe should now have a DatetimeIndex and the columns should look like:
# ```
# open                     float64
# high                     float64
# low                      float64
# close                    float64
# volume                     int64
# adj close                float64
# ticker                    object
# rolling_open_5_days      float64
# rolling_high_5_days      float64
# rolling_low_5_days       float64
# rolling_close_5_days     float64
# rolling_volume_5_days    float64
# ```


# Question 5

# Calculate the **median** of `rolling_open_5_days` for each company.
# Find the companies that have the top 10 **median** values.
# Submit a Series with the ticker as the index and their median `rolling_open_5_days` as the
# values sorted in descending order and include all ties.
rolling_open_5_days_medians = all_stocks.groupby('ticker')['rolling_open_5_days'].median().sort_values(ascending=False)
test = rolling_open_5_days_medians.head(10)
q5 = rolling_open_5_days_medians.nlargest(10, keep="all")


# Question 6

# For each company, how many times do their day's `close` price exceed
# their `rolling_close_5_days` price?
# Submit a Series with the company as the index and the values as the number of occurrences this
# happens submitted in ascending order.
time_exceed_close = all_stocks.query('close > rolling_close_5_days').groupby('ticker').size().sort_values(ascending=True)
time_exceed_close = time_exceed_close.reindex(all_stocks_tickers_list, fill_value=0)
q6 = time_exceed_close


# Question 7

# Find the average of all the stocks relative volatility per day.
# What are the 10 dates with the largest average relative volatility?
# Submit a Series with the date as the index and the values as the average relative
# volatilty sorted descending.
average_relative_volatility_per_day = all_stocks.groupby('datetimes')['relative_volatility'].mean().sort_values(ascending=False)

q7 = average_relative_volatility_per_day.head(10)

# Question 8

# The "STAT3250 Rolling Index" is designed to capture the collective movement of all of
# our stocks with some smoothing.
# It uses the 5-day rolling averages of the prices to calculate a stock index.
# You can think of it as a "super" stock that contains the information of all the stocks.

# For each date, this is defined as the average `rolling_price_5_days` for all stocks for
# which we have data on that day, weighted by the rolling volume of shares traded for each stock.

# That is, for rolling stock values
# `S_1, S_2, ...` with corresponding rolling volumes `V_1, V_2, ...`, the average
# rolling weighted volume is
# ```
# (S_1*V_1 + S_2*V_2 + ...)/(V_1 + V_2 + ...)
# ```

# Find the Open, High, Low, and Close for the "STAT3250 Rolling Index" for
# each date the market was open.
# Submit a DataFrame of the new STAT3250 Rolling Index with columns open, high, low, close
# in that order and sorted by date ascending.
def rolling_index_open(all_stocks):
    return (all_stocks['rolling_open_5_days']*all_stocks['rolling_volume_5_days']).sum()/all_stocks['rolling_volume_5_days'].sum()
def rolling_index_high(all_stocks):
    return (all_stocks['rolling_high_5_days']*all_stocks['rolling_volume_5_days']).sum()/all_stocks['rolling_volume_5_days'].sum()
def rolling_index_low(all_stocks):
    return (all_stocks['rolling_low_5_days']*all_stocks['rolling_volume_5_days']).sum()/all_stocks['rolling_volume_5_days'].sum()
def rolling_index_close(all_stocks):
    return (all_stocks['rolling_close_5_days']*all_stocks['rolling_volume_5_days']).sum()/all_stocks['rolling_volume_5_days'].sum()


rolling_index_open_series = all_stocks.groupby('datetimes').apply(rolling_index_open)
rolling_index_high_series = all_stocks.groupby('datetimes').apply(rolling_index_high)
rolling_index_low_series = all_stocks.groupby('datetimes').apply(rolling_index_low)
rolling_index_close_series = all_stocks.groupby('datetimes').apply(rolling_index_close)

rolling_indices_dictionary = {
    'open' : rolling_index_open_series,
    'high' : rolling_index_high_series,
    'low' : rolling_index_low_series,
    'close' : rolling_index_close_series
    
    }


q8 = pd.DataFrame(data=rolling_indices_dictionary).sort_index(ascending=True)


# Question 9

# Each stock in the data set contains records starting at some date and ending at another date.
# In between the start and end dates there may be dates when the market was open but there is no record.
# These are the missing records for the stock.
# For each stock, determine the proportion of records that are missing out of the total
# records that would be present if no records were missing.

# Assume that if a date appears in at least one file in the data set, then the market is open that day.
# Otherwise, the market is closed that day.
# Do not make any other assumptions about when the market is open or closed, and do not use
# Python libraries (or other libraries) to try to determine when the market was open.

# You can use a for loop to loop through each ticker.

# Submit a Series where the index is the ticker and the values are the proportion of missing days
# sorted in ascending order.
date_counts = len(all_stocks.groupby('datetimes').size()) # There are 4156 dates
number_of_tickers = len(all_stocks.groupby('ticker').size()) # There are 97 tickers/stocks
all_stocks['dates'] = all_stocks.index
stocks_date_counts = all_stocks.groupby('ticker')['dates'].size() # Count how many dates each ticker has
proportion_missing_dates = (date_counts-stocks_date_counts)/date_counts

q9 = proportion_missing_dates.sort_values(ascending=True)


# Question 10

# Assume we were savvy investors.
# Our investing strategy was as follows.
# 1. Whenever a stock first appears in the dataset, we bought 100 shares at the open price.
# 2. We then sold those 100 stocks the last day they were in the dataset at the close price.

# However, we were busy finishing homework on Wednesdays, so if a stock entered the market
# on a Wednesday, we would not buy the 100 shares until the next available day's open price.

# For simplicity, we assume that no dividends/stock splits happened.
# This means that we will always have 100 shares and the only returns are from selling
# those 100 stocks.

# What was the final value of our investment as a proportion of the original investment?
# You can use a for loop to loop through each ticker.
earliest_stock_dates = all_stocks.groupby('ticker')['dates'].min()
second_earliest_stock_dates = all_stocks.groupby('ticker')['dates'].nsmallest(2)[1::2]
latest_stock_dates = all_stocks.groupby('ticker')['dates'].max()
open_stocks_series = pd.Series()
close_stocks_series = pd.Series()
for i in range(len(earliest_stock_dates)):
    ticker = earliest_stock_dates.index[i]
    date = earliest_stock_dates[i]
    if pd.to_datetime(date).dayofweek != 2:    
        # if not wednesday
        close_date = latest_stock_dates[i]
        selected_row = all_stocks.query('ticker == @ticker and dates == @date')
        selected_row2 = all_stocks.query('ticker == @ticker and dates == @close_date')
        open_stocks_series.loc[ticker] = selected_row.iloc[0]['open']
        close_stocks_series.loc[ticker] = selected_row2.iloc[0]['close']
    else:
        # if wednesday
        new_date = second_earliest_stock_dates[i]
        close_date = latest_stock_dates[i]
        new_selected_row = all_stocks.query('ticker == @ticker and dates == @new_date')
        new_selected_row2 = all_stocks.query('ticker == @ticker and dates == @close_date')
        open_stocks_series.loc[ticker] = new_selected_row.iloc[0]['open']
        close_stocks_series.loc[ticker] = new_selected_row2.iloc[0]['close']
    

total_profit = ((close_stocks_series-open_stocks_series)*100).sum()
proportion = (1 + total_profit)/100

q10 = proportion
