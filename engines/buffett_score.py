from engines.quality import (
    analyze_quality
)

from engines.predictability import (
    PredictabilityAnalyzer
)

from engines.cashflow_quality import (
    CashflowQualityAnalyzer
)


class BuffettScoreAnalyzer:

    def __init__(
        self,
        data,
        valuation_results
    ):

        self.data = data
        self.valuation = (
            valuation_results
        )

    # =====================
    # SCORE
    # =====================

    def score(self):

        quality = (
            analyze_quality(
                self.data
            )
            .get(
                "quality_score",
                0
            )
        )
    
        predictability = (
            PredictabilityAnalyzer(
                self.data
            )
            .summary()
            .get(
                "predictability_score",
                0
            )
        )
    
        cashflow = (
            CashflowQualityAnalyzer(
                self.data
            )
            .summary()
            .get(
                "cashflow_score",
                0
            )
        )
    
        valuation = (
            self.valuation
            .get(
                "valuation_score",
                50
            )
        )

    # ------------------
    # Predictability Multiplier
    # ------------------

        if predictability >= 90:
    
            multiplier = 1.00
    
        elif predictability >= 80:
    
            multiplier = 0.95
    
        elif predictability >= 70:
    
            multiplier = 0.85
    
        elif predictability >= 60:
    
            multiplier = 0.70
    
        else:
    
            multiplier = 0.50
    
        base_quality = (
    
            quality * 0.70
            +
            cashflow * 0.20
            +
            valuation * 0.10
        )
    
        return round(
            base_quality * multiplier,
            2
        )

    # =====================
    # RATING
    # =====================

    def rating(self):

        score = self.score()

        if score >= 85:
            return "BUFFETT BUY"

        elif score >= 75:
            return "STRONG"

        elif score >= 65:
            return "GOOD"

        elif score >= 50:
            return "FAIR"

        return "SPECULATIVE"

    # =====================
    # SUMMARY
    # =====================

    def summary(self):

        quality = (
            analyze_quality(
                self.data
            )
            .get(
                "quality_score",
                0
            )
        )
    
        predictability = (
            PredictabilityAnalyzer(
                self.data
            )
            .summary()
            .get(
                "predictability_score",
                0
            )
        )
    
        cashflow = (
            CashflowQualityAnalyzer(
                self.data
            )
            .summary()
            .get(
                "cashflow_score",
                0
            )
        )
    
        valuation = (
            self.valuation
            .get(
                "valuation_score",
                50
            )
        )
    
        return {
    
            "quality": quality,
    
            "predictability": predictability,
    
            "cashflow": cashflow,
    
            "valuation": valuation,
    
            "buffett_score":
                self.score(),
    
            "rating":
                self.rating()
        }
