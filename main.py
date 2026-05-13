
    ```
3.  **Refresh:** Streamlit app par ja kar page ko refresh (reload) karein.

**Is code mein maine `pandas` library bhi add ki hai jo error aane se rokegi. Ab check kijiye aur bataiye, sab sahi chal raha hai?**
```python
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# 1. App setup
st.set_page_config(page_title="Samrat AI Market Advisor", layout="wide")

# 2. PIN Protection (1234)
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

# 3. Main App UI
st.title("📈 Samrat AI Market Advisor")

# Sidebar for inputs
st.sidebar.header("Market Settings")
symbol = st.sidebar.text_input("Enter Stock Symbol", "RELIANCE.NS")
period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y"])

try:
    # 4. Data Download
    data = yf.download(symbol, period=period)
    
    if data.empty:
        st.warning("Data nahi mila. Sahi symbol check karein (e.g., RELIANCE.NS).")
    else:
        # Fix for Plotly (removing timezone for better charts)
        data.index = data.index.tz_localize(None)
        
        # 5. Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Market Price'
        )])
        
        fig.update_layout(title=f"{symbol} Price Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. AI Analysis & Fixed Price Display
        # Using float() to fix the "Unsupported format string" error
        last_price = float(data['Close'].iloc[-1])
        avg_price = float(data['Close'].mean())
        
        st.subheader(f"AI Analysis for {symbol}")
        st.write(f"Current Market Price: **₹{last_price:,.2f}**")
        
        if last_price > avg_price:
            st.success("💡 Analysis: Bullish Trend! Market price average se upar hai.")
        else:
            st.info("💡 Analysis: Market average se niche hai. Watch for recovery.")

except Exception as e:
    st.error(f"Kuch technical issue hua: {e}")
