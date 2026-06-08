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

            self.quality * 0.25 +
            self.moat * 0.25 +
            self.predictability * 0.20 +
            self.trajectory * 0.20 +
            self.cashflow * 0.10,

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

        quality_contribution = round(
            self.quality * 0.25,
            2
        )
    
        moat_contribution = round(
            self.moat * 0.25,
            2
        )
    
        predictability_contribution = round(
            self.predictability * 0.20,
            2
        )
    
        trajectory_contribution = round(
            self.trajectory * 0.20,
            2
        )
    
        cashflow_contribution = round(
            self.cashflow * 0.10,
            2
        )
    
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
    
            "buffett_debug": {
    
                "quality_contribution":
                    quality_contribution,
    
                "moat_contribution":
                    moat_contribution,
    
                "predictability_contribution":
                    predictability_contribution,
    
                "trajectory_contribution":
                    trajectory_contribution,
    
                "cashflow_contribution":
                    cashflow_contribution
    
            },
    
            "buffett_score":
                self.score(),
    
            "buffett_rating":
                self.rating()
    
        }
