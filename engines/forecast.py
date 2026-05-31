import numpy as np

from engines.growth import GrowthAnalyzer
from engines.valuation import ValuationAnalyzer
from core.data_provider import (
    get_current_price,
    get_company_info
)


class ForecastAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.growth = GrowthAnalyzer(ticker)

        self.valuation = ValuationAnalyzer(ticker)

        self.info = get_company_info(ticker)

        self.price = get_current_price(ticker)

    # ==========================================
    # HISTORICAL EPS CAGR
    # ==========================================

    def historical_growth(self):

        growth = self.growth.summary()

        candidates = [

            growth.get("revenue_cagr_5y"),
            growth.get("revenue_cagr_10y"),
            growth.get("book_value_cagr_5y")
        ]

        candidates = [
            x for x in candidates
            if x is not None
        ]

        if len(candidates) == 0:
            return None

        return np.mean(candidates)

    # ==========================================
    # GROWTH SCENARIOS
    # ==========================================

    def growth_scenarios(self):

        historical = self.historical_growth()

        if historical is None:

            return {

                "bear": 5,
                "base": 10,
                "bull": 15
            }

        return {

            "bear":
                max(
                    historical * 0.5,
                    3
                ),

            "base":
                historical,

            "bull":
                historical * 1.3
        }

    # ==========================================
    # FUTURE EPS
    # ==========================================

    def future_eps(
        self,
        years=5,
        scenario="base"
    ):

        eps = self.info.get(
            "trailingEps",
            None
        )

        if eps is None:
            return None

        growth = self.growth_scenarios()[
            scenario
        ]

        return eps * (
            (1 + growth / 100)
            ** years
        )

    # ==========================================
    # FUTURE PE
    # ==========================================

    def future_pe(self):

        pe = self.valuation.pe_ratio()

        if pe is None:
            return 12

        return pe

    # ==========================================
    # FUTURE PRICE
    # ==========================================

    def future_price(
        self,
        years=5,
        scenario="base"
    ):

        eps = self.future_eps(
            years,
            scenario
        )

        if eps is None:
            return None

        return eps * self.future_pe()

    # ==========================================
    # EXPECTED CAGR
    # ==========================================

    def expected_return_cagr(
        self,
        years=5,
        scenario="base"
    ):

        future_price = self.future_price(
            years,
            scenario
        )

        if future_price is None:
            return None

        return (
            (
                future_price /
                self.price
            ) ** (1 / years)
            - 1
        ) * 100

    # ==========================================
    # UPSIDE
    # ==========================================

    def upside(
        self,
        years=5,
        scenario="base"
    ):

        future_price = self.future_price(
            years,
            scenario
        )

        if future_price is None:
            return None

        return (
            (
                future_price -
                self.price
            )
            /
            self.price
        ) * 100

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self):

        return {

            "current_price":
                self.price,

            "growth_scenarios":
                self.growth_scenarios(),

            "bear_price_5y":
                self.future_price(
                    5,
                    "bear"
                ),

            "base_price_5y":
                self.future_price(
                    5,
                    "base"
                ),

            "bull_price_5y":
                self.future_price(
                    5,
                    "bull"
                ),

            "expected_cagr":
                self.expected_return_cagr(
                    5,
                    "base"
                ),

            "upside":
                self.upside(
                    5,
                    "base"
                )
        }