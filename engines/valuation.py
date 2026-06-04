from engines.roic import (
    ROICAnalyzer
)


class ValuationAnalyzer:

    def __init__(
        self,
        data
    ):

        self.data = data

        self.market_cap = data.get(
            "market_cap"
        )

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

                    return float(

                        income.loc[
                            key
                        ].iloc[0]

                    )

        except:

            pass

        return None

    # ==========================================
    # OPERATING CASH FLOW
    # ==========================================

    def operating_cash_flow(self):

        try:

            cf = self.data.get(
                "cashflow"
            )

            if cf is None:
                return None

            for key in [

                "Operating Cash Flow",

                "Cash Flow From Continuing Operating Activities"

            ]:

                if key in cf.index:

                    return float(

                        cf.loc[
                            key
                        ].iloc[0]

                    )

        except:

            pass

        return None
        st.write(
            data["cashflow"].index.tolist()
        )

    

    # ==========================================
    # CAPEX
    # ==========================================

    def capex(self):

        try:

            cf = self.data.get(
                "cashflow"
            )

            if cf is None:
                return None

            for key in [

                "Capital Expenditure",

                "Capital Expenditures"

            ]:

                if key in cf.index:

                    return abs(

                        float(

                            cf.loc[
                                key
                            ].iloc[0]

                        )

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
    
            if "Free Cash Flow" in cf.index:
    
                return float(
    
                    cf.loc[
                        "Free Cash Flow"
                    ].iloc[0]
    
                )
    
        except:
    
            pass
    
        return None

    # ==========================================
    # EARNINGS YIELD
    # ==========================================

    def earnings_yield(self):

        ni = self.net_income()

        market_cap = (
            self.normalized_market_cap()
        )

        if ni is None:

            return None

        if not self.market_cap:

            return None

        if self.market_cap <= 0:

            return None

        return ni / self.market_cap

    # ==========================================
    # FCF YIELD
    # ==========================================

    def fcf_yield(self):

        fcf = self.free_cash_flow()

         market_cap = (
            self.normalized_market_cap()
        )

        if fcf is None:

            return None

        if not self.market_cap:

            return None

        if self.market_cap <= 0:

            return None

        return fcf / self.market_cap

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

        score = (

            self.earnings_yield_score()
            * 0.6

            +

            self.fcf_yield_score()
            * 0.4

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

        return {

            "market_cap":
                self.market_cap,

            "net_income":
                self.net_income(),

             "financial_currency":
                self.financial_currency(),
        
            "market_cap":
                self.market_cap,

    "normalized_market_cap":
        self.normalized_market_cap(),

            # "operating_cash_flow":
            #     self.operating_cash_flow(),

            # "capex":
            #     self.capex(),
            
            "financial_currency":
                self.financial_currency(),
            
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

        }

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

    def normalized_market_cap(self):

        market_cap = self.market_cap
    
        if market_cap is None:
    
            return None
    
        currency = self.financial_currency()
    
        if currency == "USD":
    
            market_cap = (
                market_cap
                /
                16000
            )
    
        return market_cap
