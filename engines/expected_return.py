from engines.forecast import ForecastEngine


class ExpectedReturnEngine:

    def __init__(
        self,
        ticker,
        data,
        valuation_results
    ):

        self.ticker = ticker
        self.data = data
        self.valuation = valuation_results

    # ==========================
    # FORECAST GROWTH
    # ==========================

    def forecast_growth(self):

        try:

            return (
                ForecastEngine(
                    self.ticker,
                    self.data
                )
                .summary()
                .get(
                    "forecast_growth"
                )
            )

        except:

            return None

    # ==========================
    # DIVIDEND YIELD
    # ==========================

    def dividend_yield(self):

        try:

            profile = self.data.get(
                "profile",
                {}
            )

            value = profile.get(
                "dividendYield"
            )

            if value is None:

                return 0

            return value

        except:

            return 0

    # ==========================
    # VALUATION REVERSION
    # ==========================

    def valuation_reversion(self):

        try:

            mos = self.valuation.get(
                "margin_of_safety"
            )

            if mos is None:

                return 0

            return mos * 0.10

        except:

            return 0
   
    # ==========================
    # EXPECTED RETURN
    # ==========================

    def expected_return(self):

        growth = (
            self.forecast_growth()
            or 0
        )

        dividend = (
            self.dividend_yield()
            or 0
        )

        reversion = (
            self.valuation_reversion()
            or 0
        )

        return round(

            growth
            +
            dividend
            +
            reversion,

            4
        )

    # ==========================
    # SCORE
    # ==========================

    def score(self):

        expected = (
            self.expected_return()
        )

        pct = expected * 100

        if pct >= 20:
            return 100

        elif pct >= 15:
            return 90

        elif pct >= 12:
            return 80

        elif pct >= 10:
            return 70

        elif pct >= 8:
            return 60

        elif pct >= 5:
            return 40

        return 20

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "forecast_growth":
                self.forecast_growth(),

            "dividend_yield":
                self.dividend_yield(),

            "valuation_reversion":
                self.valuation_reversion(),

            "expected_return":
                self.expected_return(),

            "expected_return_score":
                self.score()
        }
