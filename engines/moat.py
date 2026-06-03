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

        # Buffett Gate

        st.write(type(gross_margin_score))
        st.write(gross_margin_score)
        
        st.write(type(predictability_score))
        st.write(predictability_score)
        
        st.write(type(roic_score))
        st.write(roic_score)

        if roic_score == 0:

            return min(
                20,
                predictability
            )

        moat = (

            roic_score * 0.4
            +
            gross_margin_score * 0.4
            +
            predictability * 0.2

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
