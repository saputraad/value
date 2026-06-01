import numpy as np
from engines.forecast import ForecastEngine

class BankValuationAnalyzer:

    def __init__(
        self,
        ticker,
        data
    ):

        self.ticker = ticker

        self.data = data

        self.info = data.get(
            "info",
            {}
        )

        self.price = data.get(
            "price"
        )

    # ====================================
    # BASIC DATA
    # ====================================

    def roe(self):

        try:

            roe = self.info.get(
                "returnOnEquity",
                None
            )

            if roe is None:
                return None

            return roe * 100

        except:

            return None

    def book_value_per_share(self):

        try:

            return self.info.get(
                "bookValue",
                None
            )

        except:

            return None

    def pbv(self):

        try:

            bvps = self.book_value_per_share()

            if bvps is None:
                return None

            return self.price / bvps

        except:

            return None

    # ====================================
    # JUSTIFIED PBV
    # ====================================

    def justified_pbv(self):

        """
        Simplified Gordon Model

        PBV = (ROE - g)/(r-g)
        """

        try:

            roe = self.roe()
        
            if roe is None:
                return None
        
            forecast = ForecastEngine(
                self.ticker,
                get_company_data(
                    self.ticker
                )
            ).summary()
        
            growth = (
                forecast.get(
                    "forecast_growth"
                )
                * 100
            )
        
            r = forecast.get(
                "required_return"
            )
        
            if growth is None:
                return None
        
            if r is None:
                return None
        
            if r <= growth:
                return None
        
            justified = (
                (roe - growth)
                /
                (r - growth)
            )
        
            return round(
                justified,
                2
            )
        
        except:
        
            return None

    # ====================================
    # FAIR VALUE
    # ====================================

    def fair_value(self):

        try:

            bvps = self.book_value_per_share()

            fair_pbv = self.justified_pbv()

            if bvps is None:
                return None

            if fair_pbv is None:
                return None

            return round(
                bvps * fair_pbv,
                2
            )

        except:

            return None

    # ====================================
    # MARGIN OF SAFETY
    # ====================================

    def margin_of_safety(self):

        try:

            fair = self.fair_value()

            if fair is None:
                return None

            return (
                (
                    fair -
                    self.price
                )
                /
                fair
            ) * 100

        except:

            return None

    # ====================================
    # BANK SCORE
    # ====================================

    def bank_score(self):

        score = []

        roe = self.roe()

        if roe is not None:

            if roe >= 20:
                score.append(100)

            elif roe >= 15:
                score.append(90)

            elif roe >= 12:
                score.append(80)

            elif roe >= 10:
                score.append(70)

            else:
                score.append(40)

        pbv = self.pbv()

        if pbv is not None:

            if pbv <= 1:
                score.append(100)

            elif pbv <= 1.5:
                score.append(90)

            elif pbv <= 2:
                score.append(80)

            elif pbv <= 3:
                score.append(60)

            else:
                score.append(40)

        mos = self.margin_of_safety()

        if mos is not None:

            if mos >= 40:
                score.append(100)

            elif mos >= 25:
                score.append(90)

            elif mos >= 10:
                score.append(75)

            elif mos >= 0:
                score.append(60)

            else:
                score.append(30)

        if len(score) == 0:
            return None

        return round(
            np.mean(score),
            2
        )

    # ====================================
    # SUMMARY
    # ====================================
    
    def summary(self):
    
        mos = self.margin_of_safety()
    
        return {
    
            "current_price":
                self.price,
    
            "roe":
                self.roe(),
    
            "pbv":
                self.pbv(),
    
            "justified_pbv":
                self.justified_pbv(),
    
            "graham_value":
                self.fair_value(),
    
            "margin_of_safety":
                (mos / 100)
                if mos is not None
                else None,
    
            "value_score":
                self.bank_score(),
    
            "model":
                "BANK"
        }
