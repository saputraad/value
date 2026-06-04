from engines.predictability import (
    PredictabilityAnalyzer
)

from engines.roic import (
    ROICAnalyzer
)

from engines.gross_margin import (
    GrossMarginAnalyzer
)

from engines.quality import (
    analyze_quality
)

from engines.sector_classifier import (
    SectorClassifier
)


class MoatAnalyzer:

    def __init__(
        self,
        ticker,
        data
    ):

        self.ticker = ticker
        self.data = data

    # ==========================
    # SCORE
    # ==========================

    def score(self):

        sector = SectorClassifier(
            self.ticker
        ).classify()

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

        # =====================
        # BANK
        # =====================

        if sector == "BANK":

            quality = (
                analyze_quality(
                    self.data
                )
                .get(
                    "quality_score",
                    0
                )
            )

            moat = (

                quality * 0.5
                +
                predictability * 0.5

            )

            return round(
                moat,
                2
            )

        # =====================
        # NON BANK
        # =====================

        roic_score = (
            ROICAnalyzer(
                self.data
            )
            .summary()
            .get(
                "roic_score",
                0
            )
        )

        gross_margin_score = (
            GrossMarginAnalyzer(
                self.data
            )
            .summary()
            .get(
                "gross_margin_score",
                0
            )
        )

        print(
            "gross_margin_score:",
            gross_margin_score,
            type(gross_margin_score)
            )
        
        print(
            "roic_score:",
            roic_score,
            type(roic_score)
        )
        
        print(
            "predictability:",
            predictability,
            type(predictability)
        )

        # Buffett Gate

        roic_score = roic_score or 0
        gross_margin_score = gross_margin_score or 0
        predictability = predictability or 0
        
        if roic_score == 0:
        
            return min(
                20,
                predictability
            )

        moat = (

            roic_score * 0.6
            +
            predictability * 0.3
            +
            gross_margin_score * 0.1
        
        )


        return round(
            moat,
            2
        )

    # ==========================
    # RATING
    # ==========================

    def rating(self):

        score = self.score()

        if score >= 85:

            return "WIDE MOAT"

        elif score >= 70:

            return "STRONG MOAT"

        elif score >= 50:

            return "MODERATE MOAT"

        elif score >= 30:

            return "WEAK MOAT"

        return "NO MOAT"

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "moat_score":
                self.score(),

            "moat_rating":
                self.rating()
        }
