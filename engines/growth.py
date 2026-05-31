import pandas as pd
import numpy as np


# ==========================================
# CAGR HELPER
# ==========================================

def calculate_cagr(start_value, end_value, years):

    try:

        if (
            start_value is None
            or end_value is None
            or start_value <= 0
            or end_value <= 0
            or years <= 0
        ):
            return None

        return (
            (end_value / start_value)
            ** (1 / years)
            - 1
        )

    except:
        return None


# ==========================================
# GET ROW SAFE
# ==========================================

def get_row(df, possible_names):

    if df.empty:
        return None

    for row in possible_names:

        if row in df.index:

            return df.loc[row]

    return None


# ==========================================
# REVENUE CAGR
# ==========================================

def revenue_cagr(income_statement):

    revenue = get_row(
        income_statement,
        [
            "Total Revenue",
            "Revenue"
        ]
    )

    if revenue is None:
        return {}

    values = revenue.dropna().values

    if len(values) < 2:
        return {}

    newest = float(values[0])
    oldest = float(values[-1])

    years = len(values) - 1

    cagr = calculate_cagr(
        oldest,
        newest,
        years
    )

    return {
        "revenue_cagr": cagr,
        "years": years
    }


# ==========================================
# NET INCOME CAGR
# ==========================================

def earnings_cagr(income_statement):

    earnings = get_row(
        income_statement,
        [
            "Net Income",
            "NetIncome"
        ]
    )

    if earnings is None:
        return {}

    values = earnings.dropna().values

    if len(values) < 2:
        return {}

    newest = float(values[0])
    oldest = float(values[-1])

    years = len(values) - 1

    cagr = calculate_cagr(
        oldest,
        newest,
        years
    )

    return {
        "earnings_cagr": cagr,
        "years": years
    }


# ==========================================
# EQUITY CAGR
# ==========================================

def equity_cagr(balance_sheet):

    equity = get_row(
        balance_sheet,
        [
            "Stockholders Equity",
            "Total Equity Gross Minority Interest",
            "Common Stock Equity"
        ]
    )

    if equity is None:
        return {}

    values = equity.dropna().values

    if len(values) < 2:
        return {}

    newest = float(values[0])
    oldest = float(values[-1])

    years = len(values) - 1

    cagr = calculate_cagr(
        oldest,
        newest,
        years
    )

    return {
        "equity_cagr": cagr,
        "years": years
    }

# ==========================================
# GROWTH COMMENTARY
# ==========================================

def growth_commentary(results):

    comments = []

    rev = (
        results["revenue"]
        .get("revenue_cagr")
    )

    earn = (
        results["earnings"]
        .get("earnings_cagr")
    )

    eq = (
        results["equity"]
        .get("equity_cagr")
    )

    if rev is not None:

        comments.append(
            f"Revenue tumbuh {rev*100:.2f}% per tahun."
        )

    if earn is not None:

        comments.append(
            f"Laba bersih tumbuh {earn*100:.2f}% per tahun."
        )

    if eq is not None:

        comments.append(
            f"Ekuitas tumbuh {eq*100:.2f}% per tahun."
        )

    if (
        rev is not None
        and earn is not None
    ):

        if earn > rev:

            comments.append(
                "Laba tumbuh lebih cepat daripada pendapatan."
            )

        elif earn < rev:

            comments.append(
                "Pertumbuhan laba tertinggal dari pendapatan."
            )

    return comments
# ==========================================
# MASTER GROWTH ENGINE
# ==========================================

def analyze_growth(data):

    income = data["income_statement"]

    balance = data["balance_sheet"]

    revenue = revenue_cagr(income)

    earnings = earnings_cagr(income)

    equity = equity_cagr(balance)

    score = 0

rev = revenue.get("revenue_cagr")
ear = earnings.get("earnings_cagr")
equ = equity.get("equity_cagr")

# Revenue

if rev is not None:

    if rev >= 0.15:
        score += 30

    elif rev >= 0.10:
        score += 25

    elif rev >= 0.05:
        score += 15

# Earnings

if ear is not None:

    if ear >= 0.15:
        score += 40

    elif ear >= 0.10:
        score += 35

    elif ear >= 0.05:
        score += 20

# Equity

if equ is not None:

    if equ >= 0.15:
        score += 30

    elif equ >= 0.10:
        score += 25

    elif equ >= 0.05:
        score += 15

    return {

        "revenue": revenue,

        "earnings": earnings,

        "equity": equity,

        "growth_score": score
    }
results = {

    "revenue": revenue,

    "earnings": earnings,

    "equity": equity,

    "growth_score": score
}

results["commentary"] = (
    growth_commentary(results)
)

return results
