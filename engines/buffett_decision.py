class BuffettDecisionAnalyzer:

    def __init__(
        self,
        business_score,
        valuation_score
    ):

        self.business_score = business_score
        self.valuation_score = valuation_score

    # =====================
    # SCORE
    # =====================

    def score(self):

        # Buffett Gate

        if self.business_score < 50:

            return 0

        return round(

            self.business_score * 0.7
            +
            self.valuation_score * 0.3,

            2
        )

    # =====================
    # RATING
    # =====================

    def rating(self):

        if self.business_score < 50:

            return "PASS"

        score = self.score()

        if score >= 85:

            return "STRONG BUY"

        elif score >= 70:

            return "BUY"

        elif score >= 55:

            return "WATCHLIST"

        return "PASS"

    # =====================
    # SUMMARY
    # =====================

    def summary(self):

        return {

            "business_score":
                self.business_score,

            "valuation_score":
                self.valuation_score,

            "decision_score":
                self.score(),

            "decision_rating":
                self.rating()
        }
