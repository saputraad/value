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

    # =====================
    # SCORE
    # =====================

    def score(self):

        return round(
    
            self.quality * 0.30 +
    
            self.moat * 0.25 +
    
            self.predictability * 0.15 +
    
            self.trajectory * 0.15 +
    
            self.cashflow * 0.15,
    
            2
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
            return "BUFFETT FAVORITE"
    
        elif score >= 70:
            return "HIGH QUALITY"
    
        elif score >= 55:
            return "AVERAGE"
    
        elif score >= 40:
            return "SPECULATIVE"
    
        return "AVOID"

    # =====================
    # SUMMARY
    # =====================

    def summary(self):

        return {
    
            "buffett_score":
                self.score(),
    
            "buffett_rating":
                self.rating()
        }
