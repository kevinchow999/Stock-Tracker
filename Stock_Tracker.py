import yfinance as yf
import streamlit as st
import pandas as pd
import cufflinks as cf
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Application Text
st.markdown('''
# Stock Option Application
- Project created by Kevin Chow and Rex Ocampo

  Libraries used:
  - **streamlit**: Used for creating the interactive web application.
  - **yfinance**: Used for fetching stock data from Yahoo Finance.
  - **datetime**: Used for working with dates and times.
  - **pandas**: Used for data manipulation and analysis.
  - **plotly**: Used for creating interactive plots.
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Select Stock Ticker')

# Retrieving tickers data
ticker_import = pd.read_csv('https://raw.githubusercontent.com/kevinchow999/Stock-Tracker/main/StockTickers.txt')
ticker_symbol = st.sidebar.selectbox('Stock ticker', ticker_import)  
ticker_data = yf.Ticker(ticker_symbol)  
start_date = st.sidebar.date_input("Start date", datetime.date(2023, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2023, 12, 2))
ticker_df = ticker_data.history(period='1h', start=start_date, end=end_date)  # get the historical prices for this ticker

# Ticker information (additional exception handling)
try:
    ticker_name = ticker_data.info['longName']
    ticker_summary = ticker_data.info['longBusinessSummary']
except KeyError as e:
    st.warning(f"An error occurred while fetching ticker information: {e}")
else:
    st.header(f'**{ticker_name}**')
    st.info(ticker_summary)

# Stock Data
st.header('**Stock Data**')
if ticker_df.empty:
    st.warning("No historical data available for the selected period.")
else:
    ticker_df_reset = ticker_df.reset_index()
    ticker_df_reset['Date'] = ticker_df_reset['Date'].dt.strftime('%Y/%m/%d')
    ticker_df_reset['Average Price'] = ticker_df_reset[['Open', 'High', 'Low', 'Close']].mean(axis=1)
    display_columns = ['Date', 'Close', 'Average Price', 'Open', 'High', 'Low', 'Volume']
    formatted_ticker_df = ticker_df_reset[display_columns].rename(columns={'Close': 'Current Price'})

    # Display the formatted DataFrame
    st.dataframe(formatted_ticker_df)
    
# Stock Price Chart
st.header('**Stock Price Chart**')

if not ticker_df.empty:
    fig = go.Figure(data=go.Scatter(x=ticker_df.index, y=ticker_df['Close'], mode='lines'))
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Closing Price (USD)',
    )

    # Display the graph
    st.plotly_chart(fig)
else:
    st.warning("No stock data available for the selected period.")