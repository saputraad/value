class BuffettScoreAnalyzer:

    def __init__(
        self,
        quality,
        moat,
        predictability,
        trajectory,
        cashflow
    ):

        self.quality = quality
        self.moat = moat
        self.predictability = predictability
        self.trajectory = trajectory
        self.cashflow = cashflow

    def score(self):

        return round(

            self.quality * 0.30 +

            self.moat * 0.25 +

            self.predictability * 0.15 +

            self.trajectory * 0.15 +

            self.cashflow * 0.15,

            2
        )

    def rating(self):

        score = self.score()

        if score >= 85:
            return "BUFFETT FAVORITE"

        elif score >= 70:
            return "HIGH QUALITY"

        elif score >= 55:
            return "AVERAGE"

        elif score >= 40:
            return "SPECULATIVE"

        return "AVOID"

    def summary(self):

    return {

        "quality":
            self.quality,

        "moat":
            self.moat,

        "predictability":
            self.predictability,

        "trajectory":
            self.trajectory,

        "cashflow":
            self.cashflow,

        "buffett_score":
            self.score(),

        "buffett_rating":
            self.rating()
    }
