import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta

# Function to fetch stock data from yfinance
def get_stock_data(stock_symbol, start=None, end=None):
    data = yf.download(stock_symbol, start=start, end=end, interval="1d")
    return data

# Function to implement the moving average crossover strategy
def moving_average_strategy(data, short_window=50, long_window=200):
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    
    # Generate buy/sell signals
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()
    
    return data

def set_full_width():
    st.markdown(
        """
        <style>
        .main {
            max-width: 100%;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        .st-emotion-cache-13ln4jf {
            max-width: 60%;
        }
        .stDataFrame {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def dashboard():
    set_full_width()  # Apply the full-width layout
    st.title("Stock Market Dashboard")

    # Set up the sidebar for user inputs
    with st.sidebar:
        st.header("Parameters")
        
        # List of stock symbols in the dropdown
        stock_symbols = {
            "Adani Enterprises": "ADANIENT.NS",
            "Adani Ports and SEZ": "ADANIPORTS.NS",
            "Asian Paints": "ASIANPAINT.NS",
            "Axis Bank": "AXISBANK.NS",
            "Bajaj Finance": "BAJFINANCE.NS",
            "Bajaj Finserv": "BAJFINVOL.NS",
            "Bharti Airtel": "BHARTIARTL.NS",
            "BPCL": "BPCL.NS",
            "Britannia Industries": "BRITANNIA.NS",
            "Cipla": "CIPLA.NS",
            "Coal India": "COALINDIA.NS",
            "Dr. Reddy's Laboratories": "DRREDDY.NS",
            "Eicher Motors": "EICHERMOT.NS",
            "GAIL": "GAIL.NS",
            "Grasim Industries": "GRASIM.NS",
            "HCL Technologies": "HCLTECH.NS",
            "HDFC Bank": "HDFCBANK.NS",
            "HDFC Life Insurance": "HDFCLIFE.NS",
            "Hindalco Industries": "HINDALCO.NS",
            "Hindustan Unilever": "HINDUNILVR.NS",
            "ICICI Bank": "ICICIBANK.NS",
            "Indian Oil Corporation": "IOC.NS",
            "IndusInd Bank": "INDUSINDBK.NS",
            "Infosys": "INFY.NS",
            "ITC": "ITC.NS",
            "JSW Steel": "JSWSTEEL.NS",
            "Kotak Mahindra Bank": "KOTAKBANK.NS",
            "L&T": "LT.NS",
            "Mahindra & Mahindra": "M&M.NS",
            "Maruti Suzuki": "MARUTI.NS",
            "Nestle India": "NESTLEIND.NS",
            "NTPC": "NTPC.NS",
            "Oil and Natural Gas Corporation": "ONGC.NS",
            "Power Grid Corporation": "POWERGRID.NS",
            "Reliance Industries": "RELIANCE.NS",
            "SBI": "SBIN.NS",
            "SBI Life Insurance": "SBILIFE.NS",
            "Shree Cement": "SHREECEM.NS",
            "State Bank of India": "SBIN.NS",
            "Sun Pharmaceutical Industries": "SUNPHARMA.NS",
            "Tata Consultancy Services": "TCS.NS",
            "Tata Motors": "TATAMOTORS.NS",
            "Tata Steel": "TATASTEEL.NS",
            "Tech Mahindra": "TECHM.NS",
            "Titan Company": "TITAN.NS",
            "ULTRATECH CEMENT": "ULTRACEMCO.NS",
            "UPL": "UPL.NS",
            "Wipro": "WIPRO.NS",
        }

        selected_stock = st.selectbox("Select a Stock", list(stock_symbols.keys()))
        stock_symbol = stock_symbols[selected_stock]
        
        short_window = st.number_input("Short Moving Average Window", value=20, min_value=1)
        long_window = st.number_input("Long Moving Average Window", value=50, min_value=1)
        
        # Date range selector
        today = date.today()
        start_date = st.date_input("Start Date", value=date(today.year - 1, today.month, today.day))
        end_date = st.date_input("End Date", value=today)

    # Validate the date range
    if (end_date - start_date).days < 60:
        st.error("Error: The date range must be at least 60 days.")
        return

    # Fetch and display stock data based on the selected date range
    data = get_stock_data(stock_symbol, start=start_date, end=end_date)
    st.write(f"Showing data for {selected_stock} from {start_date} to {end_date}")

    # Apply moving average strategy
    data = moving_average_strategy(data, short_window, long_window)

    # Display the main backtest graph as a candlestick chart
    st.subheader(f"Backtest for {selected_stock}")
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                           open=data['Open'],
                                           high=data['High'],
                                           low=data['Low'],
                                           close=data['Close'],
                                           name='Candlestick')])

    # Increase height of the candlestick chart
    fig.update_layout(
        height=600,
        title=f'Candlestick Chart for {selected_stock}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Add moving averages
    fig.add_trace(go.Scatter(x=data.index, y=data['Short_MA'], mode='lines', name=f'Short {short_window}-day MA', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index, y=data['Long_MA'], mode='lines', name=f'Long {long_window}-day MA', line=dict(color='orange')))

    st.plotly_chart(fig)

    # Display the volume chart
    st.subheader("Volume Data")
    volume_fig = go.Figure(data=[go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='lightgreen')])

    volume_fig.update_layout(
        height=300,
        title='Volume Over Time',
        xaxis_title='Date',
        yaxis_title='Volume',
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(volume_fig)

    # Display buy/sell signals
    buy_signals = data[data['Position'] == 1]
    sell_signals = data[data['Position'] == -1]

    # Use st.table to display buy and sell signals
    st.subheader("Buy/Sell Signals")
    st.write("Buy Signals:")
    st.table(buy_signals[['Close', 'Short_MA', 'Long_MA']])

    st.write("Sell Signals:")
    st.table(sell_signals[['Close', 'Short_MA', 'Long_MA']])

    # Logout button at the bottom of the sidebar
    with st.sidebar:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.query_params['logged_in'] = "false"  # Change to st.query_params
            st.rerun()  # Change to st.rerun()

if __name__ == "__main__":
    dashboard()
