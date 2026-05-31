import yfinance as yf
import pandas as pd
import streamlit as st


# ==========================================
# HELPERS
# ==========================================

def format_ticker(ticker: str) -> str:
    """
    Convert BBCA -> BBCA.JK
    """
    ticker = ticker.upper().strip()
    if not ticker.endswith(".JK"):
        ticker += ".JK"
    return ticker


# ==========================================
# MAIN DATA LOADER
# ==========================================

@st.cache_data(ttl=3600)
def load_stock(ticker: str):
    symbol = format_ticker(ticker)
    
    # Membuat session agar yfinance mengirimkan data seperti browser manusia asli (mencegah blokir)
    import requests
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    stock = yf.Ticker(symbol, session=session)
    return stock


# ==========================================
# COMPANY INFO
# ==========================================

@st.cache_data(ttl=3600)
def get_company_info(ticker: str):
    try:
        stock = load_stock(ticker)
        info = stock.info
        if not info:
            return {}
        return info
    except Exception as e:
        print(f"Error get_company_info: {e}")
        return {}


# ==========================================
# PRICE HISTORY
# ==========================================

@st.cache_data(ttl=3600)
def get_price_history(ticker: str, period: str = "10y"):
    try:
        stock = load_stock(ticker)
        df = stock.history(period=period, auto_adjust=True)
        return df
    except Exception as e:
        print(f"Error get_price_history: {e}")
        return pd.DataFrame()


# ==========================================
# INCOME STATEMENT
# ==========================================

@st.cache_data(ttl=3600)
def get_income_statement(ticker: str):
    try:
        stock = load_stock(ticker)
        return stock.financials
    except Exception as e:
        print(f"Error get_income_statement: {e}")
        return pd.DataFrame()


# ==========================================
# BALANCE SHEET
# ==========================================

@st.cache_data(ttl=3600)
def get_balance_sheet(ticker: str):
    try:
        stock = load_stock(ticker)
        return stock.balance_sheet
    except Exception as e:
        print(f"Error get_balance_sheet: {e}")
        return pd.DataFrame()


# ==========================================
# CASH FLOW
# ==========================================

@st.cache_data(ttl=3600)
def get_cashflow(ticker: str):
    try:
        stock = load_stock(ticker)
        return stock.cashflow
    except Exception as e:
        print(f"Error get_cashflow: {e}")
        return pd.DataFrame()


# ==========================================
# DIVIDEND HISTORY
# ==========================================

@st.cache_data(ttl=3600)
def get_dividends(ticker: str):
    try:
        stock = load_stock(ticker)
        return stock.dividends
    except Exception as e:
        print(f"Error get_dividends: {e}")
        return pd.Series(dtype=float)


# ==========================================
# SHARES OUTSTANDING & MARKET CAP (Optimized)
# ==========================================

@st.cache_data(ttl=3600)
def get_shares_outstanding(ticker: str, info_dict: dict = None):
    try:
        info = info_dict if info_dict is not None else get_company_info(ticker)
        return info.get("sharesOutstanding", None)
    except:
        return None


@st.cache_data(ttl=3600)
def get_market_cap(ticker: str, info_dict: dict = None):
    try:
        info = info_dict if info_dict is not None else get_company_info(ticker)
        return info.get("marketCap", None)
    except:
        return None


# ==========================================
# CURRENT PRICE (Bypass / Anti-Gagal)
# ==========================================

@st.cache_data(ttl=300)
def get_current_price(ticker: str, info_dict: dict = None):
    try:
        stock = load_stock(ticker)
        
        # Cara 1: Ambil dari fast_info (Paling cepat & stabil di versi yfinance baru)
        if hasattr(stock, 'fast_info') and 'last_price' in stock.fast_info:
            price = stock.fast_info['last_price']
            if price and price > 0:
                return float(price)
                
        # Cara 2: Ambil dari kamus info jika disediakan
        if info_dict:
            price = info_dict.get("currentPrice") or info_dict.get("regularMarketPrice")
            if price:
                return float(price)
                
        # Cara 3: Fallback terakhir menggunakan history
        df = stock.history(period="1d")
        if not df.empty:
            # Mencari kolom close tanpa memedulikan sensitivitas huruf besar/kecil
            close_col = [col for col in df.columns if col.lower() == 'close']
            if close_col:
                return float(df[close_col[0]].iloc[-1])
                
        return None
    except Exception as e:
        print(f"Error get_current_price: {e}")
        return None


# ==========================================
# MASTER FUNCTION (Optimized to Avoid Rate Limits)
# ==========================================

@st.cache_data(ttl=3600)
def get_company_data(ticker: str):
    # Mengambil info sekali saja untuk dipakai bersama demi menghemat kuota request API
    info = get_company_info(ticker)
    price = get_current_price(ticker, info_dict=info)
    market_cap = get_market_cap(ticker, info_dict=info)
    shares = get_shares_outstanding(ticker, info_dict=info)

    return {
        "info": info,
        "price": price,
        "market_cap": market_cap,
        "shares": shares,
        "income_statement": get_income_statement(ticker),
        "balance_sheet": get_balance_sheet(ticker),
        "cashflow": get_cashflow(ticker),
        "history": get_price_history(ticker),
        "dividends": get_dividends(ticker)
    }