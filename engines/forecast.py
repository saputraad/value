from engines.growth import analyze_growth
from engines.risk import RiskAnalyzer
from engines.data_audit import DataAudit


class ForecastEngine:

    def __init__(
        self,
        ticker,
        data
    ):

        self.ticker = ticker
        self.data = data

    # ==========================
    # HISTORICAL GROWTH
    # ==========================

    def historical_growth(self):

        try:

            growth = analyze_growth(
                self.data
            )

            revenue = growth[
                "revenue"
            ].get(
                "revenue_cagr",
                0
            )

            earnings = growth[
                "earnings"
            ].get(
                "earnings_cagr",
                0
            )

            equity = growth[
                "equity"
            ].get(
                "equity_cagr",
                0
            )

            return (
                revenue * 0.2
                +
                earnings * 0.6
                +
                equity * 0.2
            )

        except:

            return None

    # ==========================
    # FORECAST GROWTH
    # ==========================

    def forecast_growth(self):

        historical = (
            self.historical_growth()
        )

        if historical is None:
            return None

        return historical * 0.8

    # ==========================
    # REQUIRED RETURN
    # ==========================

    def required_return(self):

        try:

            risk = RiskAnalyzer(
                self.ticker
            )

            score = risk.summary().get(
                "risk_score"
            )

            if score is None:
                return 15

            return round(
                10 +
                (
                    (100 - score)
                    / 10
                ),
                2
            )

        except:

            return 15

    # ==========================
    # CONFIDENCE
    # ==========================

    def confidence(self):

        audit = DataAudit(
            self.data
        )
    
        score = audit.score()
    
        historical = (
            self.historical_growth()
        )
    
        if historical is None:
    
            score *= 0.7
    
        if historical is not None:
    
            if historical > 0.25:
    
                score *= 0.8
    
        return round(
            min(
                score,
                95
            ),
            2
        )

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "historical_growth":
                self.historical_growth(),

            "forecast_growth":
                self.forecast_growth(),

            "required_return":
                self.required_return(),

            "confidence":
                self.confidence()
        }
