import pandas as pd
import numpy as np

from core.data_provider import (
    get_company_info,
    get_income_statement,
    get_balance_sheet,
    get_cashflow
)


class QualityAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.info = get_company_info(ticker)

        self.income = get_income_statement(ticker)

        self.balance = get_balance_sheet(ticker)

        self.cashflow = get_cashflow(ticker)

    # ==========================================
    # SAFE ROW FINDER
    # ==========================================

    def find_row(self, df, possible_names):

        try:

            for name in possible_names:

                if name in df.index:
                    return df.loc[name]

            return None

        except:
            return None

    # ==========================================
    # ROE
    # ==========================================

    def roe(self):

        try:

            return self.info.get("returnOnEquity", None)

        except:
            return None

    # ==========================================
    # ROA
    # ==========================================

    def roa(self):

        try:

            return self.info.get("returnOnAssets", None)

        except:
            return None

    # ==========================================
    # PROFIT MARGIN
    # ==========================================

    def net_margin(self):

        try:

            return self.info.get("profitMargins", None)

        except:
            return None

    # ==========================================
    # OPERATING MARGIN
    # ==========================================

    def operating_margin(self):

        try:

            return self.info.get("operatingMargins", None)

        except:
            return None

    # ==========================================
    # GROSS MARGIN
    # ==========================================

    def gross_margin(self):

        try:

            return self.info.get("grossMargins", None)

        except:
            return None

    # ==========================================
    # ROIC
    # ==========================================

    def roic(self):

        """
        Approximation.
        Yahoo tidak selalu menyediakan ROIC.
        """

        try:

            ebit_series = self.find_row(
                self.income,
                [
                    "EBIT",
                    "Operating Income"
                ]
            )

            debt_series = self.find_row(
                self.balance,
                [
                    "Total Debt"
                ]
            )

            equity_series = self.find_row(
                self.balance,
                [
                    "Stockholders Equity",
                    "Total Equity Gross Minority Interest"
                ]
            )

            if (
                ebit_series is None
                or debt_series is None
                or equity_series is None
            ):
                return None

            ebit = float(ebit_series.iloc[0])

            debt = float(debt_series.iloc[0])

            equity = float(equity_series.iloc[0])

            invested_capital = debt + equity

            if invested_capital <= 0:
                return None

            return ebit / invested_capital

        except:
            return None

    # ==========================================
    # FCF POSITIVE
    # ==========================================

    def positive_fcf(self):

        try:

            ocf = self.find_row(
                self.cashflow,
                [
                    "Operating Cash Flow",
                    "Cash Flow From Continuing Operating Activities"
                ]
            )

            capex = self.find_row(
                self.cashflow,
                [
                    "Capital Expenditure"
                ]
            )

            if ocf is None or capex is None:
                return None

            fcf = float(
                ocf.iloc[0]
            ) - abs(
                float(capex.iloc[0])
            )

            return fcf > 0

        except:
            return None

    # ==========================================
    # QUALITY SCORE
    # ==========================================

    def quality_score(self):

        score = []

        roe = self.roe()

        if roe is not None:

            roe = roe * 100

            if roe >= 20:
                score.append(100)

            elif roe >= 15:
                score.append(90)

            elif roe >= 10:
                score.append(75)

            elif roe >= 5:
                score.append(50)

            else:
                score.append(20)

        roic = self.roic()

        if roic is not None:

            roic = roic * 100

            if roic >= 20:
                score.append(100)

            elif roic >= 15:
                score.append(90)

            elif roic >= 10:
                score.append(75)

            elif roic >= 5:
                score.append(50)

            else:
                score.append(20)

        if self.positive_fcf():
            score.append(90)

        if len(score) == 0:
            return None

        return round(
            np.mean(score),
            2
        )

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self):

        return {

            "roe":
                self.roe(),

            "roa":
                self.roa(),

            "roic":
                self.roic(),

            "gross_margin":
                self.gross_margin(),

            "operating_margin":
                self.operating_margin(),

            "net_margin":
                self.net_margin(),

            "positive_fcf":
                self.positive_fcf(),

            "quality_score":
                self.quality_score()
        }