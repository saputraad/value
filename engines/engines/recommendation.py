import numpy as np

from engines.growth import analyze_growth
from engines.quality import analyze_quality
from engines.risk import RiskAnalyzer
from engines.technical import TechnicalAnalyzer


class RecommendationEngine:

    def __init__(
        self,
        ticker,
        data,
        valuation_results
    ):

        self.ticker = ticker

        self.data = data

        self.valuation = valuation_results

    # ==========================================
    # GET SCORES
    # ==========================================

    def valuation_score(self):

        try:

            score = self.valuation.get(
                "value_score"
            )

            if score is None:
                return None

            return float(score)

        except:

            return None

    def growth_score(self):

        try:

            growth = analyze_growth(
                self.data
            )

            return float(
                growth.get(
                    "growth_score",
                    0
                )
            )

        except:

            return None

    def quality_score(self):

        try:

            quality = analyze_quality(
                self.data
            )

            return float(
                quality.get(
                    "quality_score",
                    0
                )
            )

        except:

            return None

    def risk_score(self):

        try:

            risk = RiskAnalyzer(
                self.ticker
            )

            result = risk.summary()

            return float(
                result.get(
                    "risk_score",
                    0
                )
            )

        except:

            return None

    def technical_score(self):

        try:

            tech = TechnicalAnalyzer(
                self.ticker
            )

            result = tech.summary()

            return float(
                result.get(
                    "entry_score",
                    0
                )
            )

        except:

            return None

    # ==========================================
    # OVERALL SCORE
    # ==========================================

    def overall_score(self):

        scores = []

        val = self.valuation_score()
        gro = self.growth_score()
        qua = self.quality_score()
        ris = self.risk_score()
        tec = self.technical_score()

        for s in [
            val,
            gro,
            qua,
            ris,
            tec
        ]:

            if s is not None:
                scores.append(s)

        if len(scores) == 0:
            return None

        return round(
            np.mean(scores),
            2
        )

    # ==========================================
    # RECOMMENDATION
    # ==========================================

    def recommendation(self):

        score = self.overall_score()

        if score is None:
            return "NO DATA"

        if score >= 85:
            return "STRONG BUY"

        elif score >= 70:
            return "BUY"

        elif score >= 55:
            return "HOLD"

        else:
            return "AVOID"

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self):

        return {

            "valuation_score":
                self.valuation_score(),

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
                self.recommendation()
        }
