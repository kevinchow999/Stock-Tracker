import yfinance as yf
import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go

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

# Retrieving tickers data using historical data
ticker_import = pd.read_csv('https://raw.githubusercontent.com/kevinchow999/Stock-Tracker/main/StockTickers.txt')
ticker_symbol = st.sidebar.selectbox('Stock ticker', ticker_import)  
ticker_data = yf.Ticker(ticker_symbol)  

# Ticker information (additional exception handling)
try:
    ticker_name = ticker_data.info['longName']
    ticker_summary = ticker_data.info['longBusinessSummary']
except KeyError as e:
    st.warning(f"An error occurred while fetching ticker information: {e}")
else:
    st.header(f'**{ticker_name}**')
    st.info(ticker_summary)

# Time Period Selection
st.sidebar.subheader('Select Time Period')

# Mapping display names to backend values
period_options_mapping = {
    "1 Day": "1d",
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "10 Years": "10y",
    "Year to Date": "ytd",
    "Max": "max"
}

selected_period = st.sidebar.selectbox('Time Period', list(period_options_mapping.keys()))

# Backend value corresponding to the selected display name
selected_backend_value = period_options_mapping[selected_period]

# Fetching Ticker Data
try:
    if selected_backend_value == "1d":
        ticker_df = ticker_data.history(period=selected_backend_value, interval="1m")
    elif selected_backend_value == "5d" :
        ticker_df = ticker_data.history(period=selected_backend_value, interval="1h")
    elif selected_backend_value == "1mo" :
        ticker_df = ticker_data.history(period=selected_backend_value, interval="90m")
    else:
        ticker_df = ticker_data.history(period=selected_backend_value)
except Exception as e:
    st.warning(f"An error occurred while fetching stock data: {e}")
    ticker_df = pd.DataFrame()

# Stock Data
st.header('**Stock Data**')
if ticker_df.empty:
    st.warning("No historical data available for the selected period.")
else:
    ticker_df_filtered = ticker_df[ticker_df['Volume'] != 0]

    ticker_df_reset = ticker_df_filtered.reset_index()
    
    if 'Date' in ticker_df_reset.columns:
        # Format the date consistently
        ticker_df_reset['Date'] = ticker_df_reset['Date'].dt.strftime('%Y/%m/%d %H:%M:%S')
    
    # Displaying The Stock Chart (1d, 5d, use Datetime due to hour/minute period intervals for high graph accuracy)
    if selected_backend_value in ["1d", "5d","1mo"]:
        ticker_df_reset['Average Price'] = ticker_df_reset[['Open', 'Low', 'High', 'Close']].mean(axis=1)
        display_columns = ['Datetime', 'Open', 'Close', 'Average Price', 'Low', 'High', 'Volume']
        formatted_ticker_df = ticker_df_reset[display_columns]
    else:
        ticker_df_reset['Average Price'] = ticker_df_reset[['Open', 'Low', 'High', 'Close']].mean(axis=1)
        display_columns = ['Date', 'Open', 'Close', 'Average Price', 'Low', 'High', 'Volume']
        formatted_ticker_df = ticker_df_reset[display_columns]

    st.dataframe(formatted_ticker_df)
    
# Stock Price Graph
st.header('**Stock Price Graph**')

if not ticker_df.empty:
    fig = go.Figure(data=go.Scatter(x=ticker_df.index, y=ticker_df['Close'], mode='lines'))
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Closing Price (USD)',
    )

    if selected_backend_value == "5d":
        # Set x-axis type to 'category' for better scaling
        fig.update_xaxes(type='category')

    # Display the graph
    st.plotly_chart(fig)
else:
    st.warning("No stock data available for the selected period.")
