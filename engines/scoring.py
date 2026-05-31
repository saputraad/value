import numpy as np

from engines.growth import GrowthAnalyzer
from engines.quality import QualityAnalyzer
from engines.valuation import ValuationAnalyzer
from engines.risk_v2 import RiskAnalyzerV2
from engines.technical import TechnicalAnalyzer


class InvestmentScoringEngine:

    def __init__(self, ticker):

        self.ticker = ticker

        self.growth = GrowthAnalyzer(ticker)
        self.quality = QualityAnalyzer(ticker)
        self.value = ValuationAnalyzer(ticker)
        self.risk = RiskAnalyzerV2(ticker)
        self.technical = TechnicalAnalyzer(ticker)

    # =====================================
    # COMPONENT SCORES
    # =====================================

    def growth_score(self):

        return self.growth.summary().get(
            "growth_score"
        )

    def quality_score(self):

        return self.quality.summary().get(
            "quality_score"
        )

    def value_score(self):

        return self.value.summary().get(
            "value_score"
        )

    def risk_score(self):

        return self.risk.summary().get(
            "risk_score"
        )

    def technical_score(self):

        return self.technical.summary().get(
            "entry_score"
        )

    # =====================================
    # OVERALL SCORE
    # =====================================

    def overall_score(self):

        weights = {

            "value": 0.25,
            "growth": 0.25,
            "quality": 0.25,
            "risk": 0.15,
            "technical": 0.10
        }

        scores = {

            "value":
                self.value_score(),

            "growth":
                self.growth_score(),

            "quality":
                self.quality_score(),

            "risk":
                self.risk_score(),

            "technical":
                self.technical_score()
        }

        total = 0
        total_weight = 0

        for key, score in scores.items():

            if score is not None:

                total += (
                    score *
                    weights[key]
                )

                total_weight += (
                    weights[key]
                )

        if total_weight == 0:
            return None

        return round(
            total / total_weight,
            2
        )

    # =====================================
    # RECOMMENDATION
    # =====================================

    def recommendation(self):

        score = self.overall_score()

        if score is None:
            return "NO DATA"

        if score >= 90:
            return "STRONG BUY"

        elif score >= 80:
            return "BUY"

        elif score >= 70:
            return "ACCUMULATE"

        elif score >= 60:
            return "HOLD"

        elif score >= 50:
            return "WATCHLIST"

        return "AVOID"

    # =====================================
    # CONFIDENCE LEVEL
    # =====================================

    def confidence(self):

        count = 0

        if self.value_score() is not None:
            count += 1

        if self.growth_score() is not None:
            count += 1

        if self.quality_score() is not None:
            count += 1

        if self.risk_score() is not None:
            count += 1

        if self.technical_score() is not None:
            count += 1

        return round(
            count / 5 * 100,
            2
        )

    # =====================================
    # SUMMARY
    # =====================================

    def summary(self):

        return {

            "ticker":
                self.ticker,

            "value_score":
                self.value_score(),

            "growth_score":
                self.growth_score(),

            "quality_score":
                self.quality_score(),

            "risk_score":
                self.risk_score(),

            "technical_score":
                self.technical_score(),

            "overall_score":
                self.overall_score(),

            "recommendation":
                self.recommendation(),

            "confidence":
                self.confidence()
        }