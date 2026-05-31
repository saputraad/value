import numpy as np

from engines.growth import GrowthAnalyzer
from engines.quality import QualityAnalyzer
from engines.economic_moat import (
    EconomicMoatAnalyzer
)
from engines.forecast import (
    ForecastAnalyzer
)
from engines.risk_v2 import (
    RiskAnalyzerV2
)


class MultibaggerAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.growth = GrowthAnalyzer(
            ticker
        )

        self.quality = QualityAnalyzer(
            ticker
        )

        self.moat = EconomicMoatAnalyzer(
            ticker
        )

        self.forecast = ForecastAnalyzer(
            ticker
        )

        self.risk = RiskAnalyzerV2(
            ticker
        )

    # =====================================
    # REVENUE GROWTH
    # =====================================

    def revenue_growth_score(self):

        growth = self.growth.summary()

        cagr = growth.get(
            "revenue_cagr_5y"
        )

        if cagr is None:
            return None

        if cagr >= 30:
            return 100

        elif cagr >= 20:
            return 90

        elif cagr >= 15:
            return 80

        elif cagr >= 10:
            return 60

        return 30

    # =====================================
    # QUALITY
    # =====================================

    def quality_score(self):

        return (
            self.quality.summary()
            .get("quality_score")
        )

    # =====================================
    # MOAT
    # =====================================

    def moat_score(self):

        return (
            self.moat.summary()
            .get("moat_score")
        )

    # =====================================
    # FORECAST
    # =====================================

    def forecast_score(self):

        expected = (
            self.forecast.summary()
            .get("expected_cagr")
        )

        if expected is None:
            return None

        if expected >= 25:
            return 100

        elif expected >= 20:
            return 90

        elif expected >= 15:
            return 80

        elif expected >= 10:
            return 60

        return 30

    # =====================================
    # RISK
    # =====================================

    def risk_score(self):

        return (
            self.risk.summary()
            .get("risk_score")
        )

    # =====================================
    # MULTIBAGGER SCORE
    # =====================================

    def multibagger_score(self):

        scores = []

        metrics = [

            self.revenue_growth_score(),

            self.quality_score(),

            self.moat_score(),

            self.forecast_score(),

            self.risk_score()
        ]

        for metric in metrics:

            if metric is not None:

                scores.append(metric)

        if len(scores) == 0:

            return None

        return round(
            np.mean(scores),
            2
        )

    # =====================================
    # PROBABILITY
    # =====================================

    def probability_rating(self):

        score = self.multibagger_score()

        if score is None:

            return "UNKNOWN"

        if score >= 90:

            return "VERY_HIGH"

        elif score >= 80:

            return "HIGH"

        elif score >= 70:

            return "MEDIUM"

        elif score >= 60:

            return "LOW"

        return "VERY_LOW"

    # =====================================
    # SUMMARY
    # =====================================

    def summary(self):

        return {

            "ticker":
                self.ticker,

            "multibagger_score":
                self.multibagger_score(),

            "probability":
                self.probability_rating()
        }