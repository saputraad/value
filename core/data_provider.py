import yfinance as yf
import pandas as pd
import streamlit as st


# ==================================================
# TICKER FORMATTER
# ==================================================

def format_ticker(ticker: str) -> str:

    ticker = ticker.upper().strip()

    if not ticker.endswith(".JK"):
        ticker += ".JK"

    return ticker


# ==================================================
# LOAD STOCK
# ==================================================

@st.cache_resource
def load_stock(ticker: str):

    symbol = format_ticker(ticker)

    return yf.Ticker(symbol)


# ==================================================
# COMPANY INFO
# ==================================================

@st.cache_data(ttl=3600)
def get_company_info(ticker: str):

    try:

        stock = load_stock(ticker)

        info = stock.info

        if not isinstance(info, dict):
            return {}

        return info

    except Exception:

        return {}


# ==================================================
# FAST INFO
# ==================================================

@st.cache_data(ttl=1800)
def get_fast_info(ticker: str):

    try:

        stock = load_stock(ticker)

        return dict(stock.fast_info)

    except Exception:

        return {}


# ==================================================
# PRICE HISTORY
# ==================================================

@st.cache_data(ttl=1800)
def get_price_history(
    ticker: str,
    period: str = "10y"
):

    try:

        stock = load_stock(ticker)

        df = stock.history(
            period=period,
            auto_adjust=True
        )

        if df is None:
            return pd.DataFrame()

        return df

    except Exception:

        return pd.DataFrame()


# ==================================================
# CURRENT PRICE
# ==================================================

@st.cache_data(ttl=300)
def get_current_price(ticker: str):

    try:

        fast = get_fast_info(ticker)

        if fast:

            last_price = (
                fast.get("lastPrice")
                or fast.get("regularMarketPrice")
            )

            if last_price:
                return float(last_price)

    except Exception:
        pass

    try:

        history = get_price_history(
            ticker,
            period="1mo"
        )

        if not history.empty:

            return float(
                history["Close"].dropna().iloc[-1]
            )

    except Exception:
        pass

    return None


# ==================================================
# MARKET CAP
# ==================================================

@st.cache_data(ttl=1800)
def get_market_cap(ticker: str):

    try:

        fast = get_fast_info(ticker)

        market_cap = fast.get("marketCap")

        if market_cap:
            return float(market_cap)

    except Exception:
        pass

    try:

        info = get_company_info(ticker)

        market_cap = info.get("marketCap")

        if market_cap:
            return float(market_cap)

    except Exception:
        pass

    return None


# ==================================================
# SHARES OUTSTANDING
# ==================================================

@st.cache_data(ttl=1800)
def get_shares_outstanding(ticker: str):

    try:

        fast = get_fast_info(ticker)

        shares = fast.get("shares")

        if shares:
            return float(shares)

    except Exception:
        pass

    try:

        info = get_company_info(ticker)

        shares = info.get("sharesOutstanding")

        if shares:
            return float(shares)

    except Exception:
        pass

    return None


# ==================================================
# INCOME STATEMENT
# ==================================================

@st.cache_data(ttl=3600)
def get_income_statement(ticker: str):

    try:

        stock = load_stock(ticker)

        return stock.financials

    except Exception:

        return pd.DataFrame()


# ==================================================
# BALANCE SHEET
# ==================================================

@st.cache_data(ttl=3600)
def get_balance_sheet(ticker: str):

    try:

        stock = load_stock(ticker)

        return stock.balance_sheet

    except Exception:

        return pd.DataFrame()


# ==================================================
# CASHFLOW
# ==================================================

@st.cache_data(ttl=3600)
def get_cashflow(ticker: str):

    try:

        stock = load_stock(ticker)

        return stock.cashflow

    except Exception:

        return pd.DataFrame()


# ==================================================
# DIVIDENDS
# ==================================================

@st.cache_data(ttl=3600)
def get_dividends(ticker: str):

    try:

        stock = load_stock(ticker)

        return stock.dividends

    except Exception:

        return pd.Series(dtype=float)


# ==================================================
# PROFILE
# ==================================================

@st.cache_data(ttl=1800)
def get_profile(ticker: str):

    info = get_company_info(ticker)

    return {

        "name":
            info.get("longName"),

        "sector":
            info.get("sector"),

        "industry":
            info.get("industry"),

        "country":
            info.get("country"),

        "website":
            info.get("website"),
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@st.cache_data(ttl=1800)
def get_data_health(ticker: str):

    income = get_income_statement(ticker)
    balance = get_balance_sheet(ticker)
    cashflow = get_cashflow(ticker)

    return {

        "income_statement":
            not income.empty,

        "balance_sheet":
            not balance.empty,

        "cashflow":
            not cashflow.empty,
    }


# ==================================================
# MASTER DATA OBJECT
# ==================================================

@st.cache_data(ttl=1800)
def get_company_data(ticker: str):

    return {

        "ticker":
            ticker,

        "profile":
            get_profile(ticker),

        "price":
            get_current_price(ticker),

        "market_cap":
            get_market_cap(ticker),

        "shares_outstanding":
            get_shares_outstanding(ticker),

        "income_statement":
            get_income_statement(ticker),

        "balance_sheet":
            get_balance_sheet(ticker),

        "cashflow":
            get_cashflow(ticker),

        "history":
            get_price_history(ticker),

        "dividends":
            get_dividends(ticker),

        "health":
            get_data_health(ticker),
    }
