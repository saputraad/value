import yfinance as yf
import pandas as pd
import streamlit as st


# ==========================================
# TICKER
# ==========================================

def format_ticker(ticker: str) -> str:

    ticker = ticker.upper().strip()

    if not ticker.endswith(".JK"):
        ticker += ".JK"

    return ticker


# ==========================================
# LOAD STOCK
# ==========================================

def load_stock(ticker: str):

    return yf.Ticker(
        format_ticker(ticker)
    )


# ==========================================
# COMPANY INFO
# ==========================================

@st.cache_data(ttl=21600)
def get_company_info(ticker: str):

    try:

        return (
            load_stock(ticker)
            .info
        )

    except:

        return {}


# ==========================================
# FAST INFO
# ==========================================

@st.cache_data(ttl=300)
def get_fast_info(ticker: str):

    try:

        return dict(
            load_stock(ticker)
            .fast_info
        )

    except:

        return {}


# ==========================================
# CURRENT PRICE
# ==========================================

@st.cache_data(ttl=60)
def get_current_price(ticker: str):

    stock = load_stock(
        ticker
    )

    # --------------------------------------
    # PRIORITY 1
    # INTRADAY
    # --------------------------------------

    try:

        intraday = stock.history(

            period="1d",

            interval="1m",

            auto_adjust=False

        )

        if not intraday.empty:

            return float(

                intraday[
                    "Close"
                ]
                .iloc[-1]

            )

    except:

        pass

    # --------------------------------------
    # PRIORITY 2
    # FAST INFO
    # --------------------------------------

    try:

        fast = get_fast_info(
            ticker
        )

        price = (

            fast.get(
                "lastPrice"
            )

            or

            fast.get(
                "regularMarketPrice"
            )

        )

        if price:

            return float(
                price
            )

    except:

        pass

    # --------------------------------------
    # PRIORITY 3
    # DAILY CLOSE
    # --------------------------------------

    try:

        daily = stock.history(
            period="5d"
        )

        if not daily.empty:

            return float(

                daily[
                    "Close"
                ]
                .iloc[-1]

            )

    except:

        pass

    return None


# ==========================================
# SHARES OUTSTANDING
# ==========================================

@st.cache_data(ttl=21600)
def get_shares_outstanding(ticker: str):

    try:

        info = get_company_info(
            ticker
        )

        shares = info.get(
            "sharesOutstanding"
        )

        if shares:

            return float(
                shares
            )

    except:

        pass

    return None


# ==========================================
# MARKET CAP
# ==========================================

@st.cache_data(ttl=300)
    def get_market_cap(ticker):
    
        try:
    
            fast = get_fast_info(
                ticker
            )
    
            market_cap = (
    
                fast.get(
                    "marketCap"
                )
    
                or
    
                fast.get(
                    "market_cap"
                )
    
            )
    
            if market_cap:
    
                return float(
                    market_cap
                )
    
        except:
    
            pass
    
        try:
    
            shares = get_shares_outstanding(
                ticker
            )
    
            price = get_current_price(
                ticker
            )
    
            if shares and price:
    
                return shares * price
    
        except:
    
            pass
    
        return None


# ==========================================
# FINANCIALS
# ==========================================

@st.cache_data(ttl=21600)
    def get_income_statement(ticker: str):
    
        try:
    
            return (
                load_stock(ticker)
                .financials
            )
    
        except:
    
            return pd.DataFrame()


@st.cache_data(ttl=21600)
    def get_balance_sheet(ticker: str):
    
        try:
    
            return (
                load_stock(ticker)
                .balance_sheet
            )
    
        except:
    
            return pd.DataFrame()


@st.cache_data(ttl=21600)
    def get_cashflow(ticker: str):
    
        try:
    
            return (
                load_stock(ticker)
                .cashflow
            )
    
        except:
    
            return pd.DataFrame()


# ==========================================
# PRICE HISTORY
# ==========================================

@st.cache_data(ttl=3600)
def get_price_history(
    ticker,
    period="10y"
):

    try:

        return (

            load_stock(
                ticker
            )

            .history(

                period=period,

                auto_adjust=True

            )

        )

    except:

        return pd.DataFrame()


# ==========================================
# DIVIDENDS
# ==========================================

@st.cache_data(ttl=21600)
def get_dividends(ticker: str):

    try:

        return (
            load_stock(ticker)
            .dividends
        )

    except:

        return pd.Series(
            dtype=float
        )


# ==========================================
# PROFILE
# ==========================================

@st.cache_data(ttl=21600)
def get_profile(ticker: str):

    info = get_company_info(
        ticker
    )

    return {

        "symbol":
            ticker,

        "name":
            info.get(
                "longName"
            ),

        "sector":
            info.get(
                "sector"
            ),

        "industry":
            info.get(
                "industry"
            ),

        "country":
            info.get(
                "country"
            ),

        "website":
            info.get(
                "website"
            )
    }


# ==========================================
# HEALTH
# ==========================================

def get_data_health(
    ticker
):

    income = (
        get_income_statement(
            ticker
        )
    )

    balance = (
        get_balance_sheet(
            ticker
        )
    )

    cashflow = (
        get_cashflow(
            ticker
        )
    )

    return {

        "income_statement":
            not income.empty,

        "balance_sheet":
            not balance.empty,

        "cashflow":
            not cashflow.empty
    }


# ==========================================
# MASTER DATA
# ==========================================

@st.cache_data(ttl=300)
def get_company_data(
    ticker
):

    return {

        "ticker":
            ticker,

        "profile":
            get_profile(
                ticker
            ),

        "info":
            get_company_info(
                ticker
            ),

        "price":
            get_current_price(
                ticker
            ),

        "market_cap":
            get_market_cap(
                ticker
            ),

        "shares_outstanding":
            get_shares_outstanding(
                ticker
            ),

        "income_statement":
            get_income_statement(
                ticker
            ),

        "balance_sheet":
            get_balance_sheet(
                ticker
            ),

        "cashflow":
            get_cashflow(
                ticker
            ),

        "history":
            get_price_history(
                ticker
            ),

        "dividends":
            get_dividends(
                ticker
            ),

        "health":
            get_data_health(
                ticker
            )
    }
