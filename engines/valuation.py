print(
    "VALUATION FILE LOADED"
)
from engines.roic import (
    ROICAnalyzer
)
from config.banks import INDONESIAN_BANKS

USD_IDR_RATE = 16000

class ValuationAnalyzer:

    def __init__(
        self,
        data
    ):
    
        self.data = data
    
        self.ticker = (
            data.get(
                "ticker",
                ""
            ).upper()
        )
    
        self.market_cap = (
    
            data.get(
                "market_cap"
            )
    
            or
    
            data.get(
                "info",
                {}
            ).get(
                "marketCap"
            )
    
        )
# class ValuationAnalyzer:

#     def __init__(
#         self,
#         ticker,
#         data
#     ):
#         raise Exception(
#             f"VALUATION INIT: {ticker}"
#         )

#         self.ticker = ticker.upper()
#         self.data = data

#         self.ticker = ticker.upper()
#         self.data = data

#         self.market_cap = (

#             data.get(
#                 "market_cap"
#             )

#             or

#             data.get(
#                 "info",
#                 {}
#             ).get(
#                 "marketCap"
#             )

#         )
#         print(
#             "MARKET CAP:",
#             self.market_cap
#         )
        
    def is_bank(self):

        info = self.data.get(
            "info",
            {}
        )
    
        industry = str(
            info.get(
                "industry",
                ""
            )
        ).lower()
    
        if "bank" in industry:
    
            return True
    
        return (
            self.ticker
            in
            INDONESIAN_BANKS
        )

    # ==========================================
    # FINANCIAL CURRENCY
    # ==========================================

    def financial_currency(self):

        try:

            return (

                self.data
                .get(
                    "info",
                    {}
                )
                .get(
                    "financialCurrency"
                )

            )

        except:

            return None

    # ==========================================
    # NORMALIZE CURRENCY
    # ==========================================

    def normalize_currency(
        self,
        value
    ):

        if value is None:

            return None

        currency = (
            self.financial_currency()
        )

        if currency == "USD":

            return (
                value
                *
                USD_IDR_RATE
            )

        return value

    # ==========================================
    # NET INCOME
    # ==========================================

    def net_income(self):

        try:

            income = self.data.get(
                "income_statement"
            )

            if income is None:
                return None

            for key in [

                "Net Income",

                "Net Income Common Stockholders"

            ]:

                if key in income.index:

                    value = float(

                        income.loc[
                            key
                        ].iloc[0]

                    )

                    return self.normalize_currency(
                        value
                    )

        except:

            pass

        return None

    # ==========================================
    # FREE CASH FLOW
    # ==========================================

    def free_cash_flow(self):

        try:

            cf = self.data.get(
                "cashflow"
            )

            if cf is None:
                return None

            if (
                "Free Cash Flow"
                in cf.index
            ):

                value = float(

                    cf.loc[
                        "Free Cash Flow"
                    ].iloc[0]

                )

                return self.normalize_currency(
                    value
                )

        except:

            pass

        return None

    # ==========================================
    # EARNINGS YIELD
    # ==========================================

    def earnings_yield(self):

        ni = self.net_income()

        if ni is None:
            return None

        if self.market_cap is None:
            return None

        if self.market_cap <= 0:
            return None

        return (
            ni
            /
            self.market_cap
        )

    # ==========================================
    # FCF YIELD
    # ==========================================

    def fcf_yield(self):

        fcf = self.free_cash_flow()

        if fcf is None:
            return None

        if self.market_cap is None:
            return None

        if self.market_cap <= 0:
            return None

        return (
            fcf
            /
            self.market_cap
        )

    # ==========================================
    # EARNINGS YIELD SCORE
    # ==========================================

    def earnings_yield_score(self):

        ey = self.earnings_yield()

        if ey is None:

            return 0

        if ey >= 0.15:
            return 100

        elif ey >= 0.12:
            return 90

        elif ey >= 0.10:
            return 80

        elif ey >= 0.08:
            return 70

        elif ey >= 0.06:
            return 60

        return 40

    # ==========================================
    # FCF YIELD SCORE
    # ==========================================

    def fcf_yield_score(self):

        fy = self.fcf_yield()

        if fy is None:

            return 0

        if fy >= 0.12:
            return 100

        elif fy >= 0.10:
            return 90

        elif fy >= 0.08:
            return 80

        elif fy >= 0.06:
            return 70

        elif fy >= 0.04:
            return 60

        return 40

    # ==========================================
    # VALUATION SCORE
    # ==========================================

    def valuation_score(self):

        earnings_score = (
            self.earnings_yield_score()
        )
    
        fcf_score = (
            self.fcf_yield_score()
        )
    
        if self.is_bank():

            score = earnings_score
        
        else:
        
            score = (
                earnings_score * 0.6
                +
                fcf_score * 0.4
            )
    
        try:
    
            roic = (
    
                ROICAnalyzer(
                    self.data
                )
                .summary()
                .get(
                    "roic"
                )
    
            )
    
            if roic is not None:
    
                if roic > 0.20:
    
                    score += 10
    
                elif roic > 0.15:
    
                    score += 5
    
                elif roic < 0:
    
                    score -= 20
    
                elif roic < 0.05:
    
                    score -= 10
    
        except:
    
            pass
    
        return round(
    
            max(
                0,
                min(
                    score,
                    100
                )
            ),
    
            2
        )

    # ==========================================
    # SUMMARY
    # ==========================================
    def summary(self):

        info = self.data.get(
            "info",
            {}
        )
    
        return {
    
            "valuation_debug": {

                "is_bank":
                    self.is_bank(),
    
                "sector":
                    info.get(
                        "sector"
                    ),
    
                "industry":
                    info.get(
                        "industry"
                    ),
    
                "earnings_yield_score":
                    self.earnings_yield_score(),
    
                "fcf_yield_score":
                    self.fcf_yield_score()
    
            },
    
            "financial_currency":
                self.financial_currency(),
    
            "market_cap":
                self.market_cap,
    
            "net_income":
                self.net_income(),
    
            "free_cash_flow":
                self.free_cash_flow(),
    
            "earnings_yield":
                self.earnings_yield(),
    
            "fcf_yield":
                self.fcf_yield(),
    
            "earnings_yield_score":
                self.earnings_yield_score(),
    
            "fcf_yield_score":
                self.fcf_yield_score(),
    
            "valuation_score":
                self.valuation_score()
            
    def sector(self):

        info = self.data.get(
            "info",
            {}
        )
    
        sector = info.get(
            "sector"
        )
    
        if sector:
    
            return sector
    
        if self.is_bank():
    
            return "Financial Services"
    
        return None

    def industry(self):

        info = self.data.get(
            "info",
            {}
        )
    
        industry = info.get(
            "industry"
        )
    
        if industry:
    
            return industry
    
        if self.is_bank():
    
            return "Banks"
    
        return None
    
        }
