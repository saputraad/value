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

        return round(

            quality * 0.40
            +
            predictability * 0.30
            +
            cashflow * 0.15
            +
            valuation * 0.15,

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
