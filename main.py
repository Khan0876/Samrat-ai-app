import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# App title and styling
st.set_page_config(page_title="Samrat AI Market Advisor", layout="wide")

# Simple PIN Protection
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Welcome to Samrat AI")
    pin = st.text_input("Enter your 4-digit PIN", type="password")
    if st.button("Unlock"):
        if pin == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Ghalat PIN! Phir se koshish karein.")
    st.stop()

# --- Main App Starts Here ---
st.title("📈 Samrat AI Market Advisor")
st.sidebar.header("Settings")

# User Input for Stock
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, TSLA)", "RELIANCE.NS")
period = st.sidebar.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "5y"])

try:
    # Fetch Data
    data = yf.download(symbol, period=period)
    
    if data.empty:
        st.warning("Data nahi mila. Sahi symbol check karein.")
    else:
        # Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name='Market Data')])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Simple AI Insight
        last_price = data['Close'].iloc[-1]
        st.subheader(f"AI Analysis for {symbol}")
        st.write(f"Current Price: **₹{last_price:,.2f}**")
        
        if last_price > data['Close'].mean():
            st.success("Analysis: Market is currently above average. Bullish trend!")
        else:
            st.info("Analysis: Market is below average. Potential buying opportunity?")

except Exception as e:
    st.error(f"Kuch ghalat hua: {e}")
