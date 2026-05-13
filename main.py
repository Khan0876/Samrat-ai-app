import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

# --- SECURITY ---
REAL_PIN = "1234"
PANIC_PIN = "9999"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ SAMRAT AI LOCK")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Unlock"):
        if pin == REAL_PIN:
            st.session_state.auth = True
            st.session_state.mode = "REAL"
            st.rerun()
        elif pin == PANIC_PIN:
            st.session_state.auth = True
            st.session_state.mode = "GHOST"
            st.rerun()
        else: st.error("Wrong PIN!")
else:
    if st.session_state.mode == "GHOST":
        st.title("⚠️ System Error")
        st.error("Balance: ₹0.00 | No Data Found")
    else:
        st.sidebar.title("💎 SAMRAT PRO")
        st.title("🤖 AI Market Advisor")
        ticker = st.text_input("Stock Name (e.g. RELIANCE.NS)", "RELIANCE.NS")
        if st.button("Analyze"):
            df = yf.download(ticker, period="6mo")
            if not df.empty:
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
                st.plotly_chart(fig)
                st.success(f"{ticker} Analysis Complete!")

if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()
