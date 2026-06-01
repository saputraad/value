import pandas as pd
import numpy as np
from engines.roic import (
    ROICAnalyzer
)
from engines.sector_classifier import (
    SectorClassifier
)


# ==========================================
# SAFE GETTER
# ==========================================

def safe_get(df, row_names):

    if df is None or df.empty:
        return None

    for row in row_names:

        if row in df.index:
            return df.loc[row]

    return None


# ==========================================
# ROE
# ==========================================

def calculate_roe(data):

    try:

        income = data["income_statement"]
        balance = data["balance_sheet"]

        net_income = safe_get(
            income,
            [
                "Net Income",
                "NetIncome"
            ]
        )

        equity = safe_get(
            balance,
            [
                "Stockholders Equity",
                "Common Stock Equity",
                "Total Equity Gross Minority Interest"
            ]
        )

        if net_income is None or equity is None:
            return None

        ni = float(net_income.iloc[0])
        eq = float(equity.iloc[0])

        if eq <= 0:
            return None

        return ni / eq

    except:
        return None


# ==========================================
# ROA
# ==========================================

def calculate_roa(data):

    try:

        income = data["income_statement"]
        balance = data["balance_sheet"]

        net_income = safe_get(
            income,
            [
                "Net Income",
                "NetIncome"
            ]
        )

        assets = safe_get(
            balance,
            [
                "Total Assets"
            ]
        )

        if net_income is None or assets is None:
            return None

        ni = float(net_income.iloc[0])
        ta = float(assets.iloc[0])

        if ta <= 0:
            return None

        return ni / ta

    except:
        return None


# ==========================================
# DEBT TO EQUITY
# ==========================================

def calculate_debt_to_equity(data):

    try:

        balance = data["balance_sheet"]

        debt = safe_get(
            balance,
            [
                "Total Debt",
                "Long Term Debt"
            ]
        )

        equity = safe_get(
            balance,
            [
                "Stockholders Equity",
                "Common Stock Equity",
                "Total Equity Gross Minority Interest"
            ]
        )

        if debt is None or equity is None:
            return None

        debt_value = float(debt.iloc[0])
        equity_value = float(equity.iloc[0])

        if equity_value <= 0:
            return None

        return debt_value / equity_value

    except:
        return None

# ==========================================
# ROIC SCORE
# ==========================================

def calculate_roic_score(roic):

    if roic is None:
        return 0

    roic_pct = roic * 100

    if roic_pct >= 20:
        return 30

    elif roic_pct >= 15:
        return 25

    elif roic_pct >= 10:
        return 20

    elif roic_pct >= 5:
        return 10

    return 0
# ==========================================
# QUALITY SCORE
# ==========================================

def calculate_quality_score(
    roe,
    roa,
    debt_to_equity,
    roic
):

    score = 0

    # ROE

    if roe is not None:

        roe_pct = roe * 100

        if roe_pct >= 20:
            score += 30
        
        elif roe_pct >= 15:
            score += 25
        
        elif roe_pct >= 10:
            score += 20
        
        elif roe_pct >= 5:
            score += 10

    # ROA

    if roa is not None:

        roa_pct = roa * 100

        if roa_pct >= 10:
            score += 20
        
        elif roa_pct >= 5:
            score += 15
        
        elif roa_pct >= 2:
            score += 10

    # Debt

    if debt_to_equity is not None:

        if debt_to_equity <= 0.5:
            score += 20
        
        elif debt_to_equity <= 1:
            score += 15
        
        elif debt_to_equity <= 2:
            score += 10

    score += calculate_roic_score(
    roic
    )    

    return min(score, 100)


# ==========================================
# MASTER ANALYZER
# ==========================================

def analyze_quality(data):

    roe = calculate_roe(data)

    roa = calculate_roa(data)

    debt_to_equity = calculate_debt_to_equity(data)

    roic = (
        ROICAnalyzer(
            data
        )
        .summary()
        .get(
            "roic"
        )
    )    

    score = calculate_quality_score(
        roe,
        roa,
        debt_to_equity,
        roic
    )

    return {

        "roe": roe,
    
        "roa": roa,
    
        "debt_to_equity": debt_to_equity,
    
        "roic": roic,
    
        "quality_score": score
    }
