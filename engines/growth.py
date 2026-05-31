import pandas as pd
import numpy as np
from core.utils import get_metric

from core.data_provider import (
    get_income_statement,
    get_balance_sheet,
)


class GrowthAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.income = get_income_statement(ticker)

        self.balance = get_balance_sheet(ticker)

    # ==========================================
    # CAGR
    # ==========================================

    @staticmethod
    def calculate_cagr(
        start_value,
        end_value,
        years
    ):

        try:

            if start_value <= 0:
                return None

            if end_value <= 0:
                return None

            return (
                (
                    end_value / start_value
                ) ** (1 / years) - 1
            ) * 100

        except:
            return None

    # ==========================================
    # REVENUE SERIES
    # ==========================================

    def get_revenue_series(self):

        try:

            revenue = get_metric(
    self.income,
    "revenue"
)

            revenue = revenue.sort_index()

            return revenue

        except:

            return pd.Series(dtype=float)

    # ==========================================
    # REVENUE CAGR
    # ==========================================

    def revenue_cagr(self, years=5):

        revenue = self.get_revenue_series()

        if len(revenue) < years:
            return None

        start = revenue.iloc[-years]
        end = revenue.iloc[-1]

        return self.calculate_cagr(
            start,
            end,
            years - 1
        )

    # ==========================================
    # BOOK VALUE SERIES
    # ==========================================

    def get_book_value_series(self):

        try:

            equity = self.balance.loc[
                "Stockholders Equity"
            ]

            equity = equity.sort_index()

            return equity

        except:

            return pd.Series(dtype=float)

    # ==========================================
    # BV CAGR
    # ==========================================

    def bv_cagr(self, years=5):

        bv = self.get_book_value_series()

        if len(bv) < years:
            return None

        start = bv.iloc[-years]
        end = bv.iloc[-1]

        return self.calculate_cagr(
            start,
            end,
            years - 1
        )

    # ==========================================
    # GROWTH SCORE
    # ==========================================

    def growth_score(self):

        scores = []

        rev5 = self.revenue_cagr(5)

        if rev5 is not None:

            if rev5 >= 20:
                scores.append(100)

            elif rev5 >= 15:
                scores.append(90)

            elif rev5 >= 10:
                scores.append(80)

            elif rev5 >= 5:
                scores.append(60)

            else:
                scores.append(30)

        if len(scores) == 0:
            return None

        return round(np.mean(scores), 2)

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self):

        return {

            "revenue_cagr_5y":
                self.revenue_cagr(5),

            "revenue_cagr_10y":
                self.revenue_cagr(10),

            "book_value_cagr_5y":
                self.bv_cagr(5),

            "book_value_cagr_10y":
                self.bv_cagr(10),

            "growth_score":
                self.growth_score()
        }