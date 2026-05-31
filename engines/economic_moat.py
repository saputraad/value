import numpy as np

from engines.quality import QualityAnalyzer
from engines.growth import GrowthAnalyzer


class EconomicMoatAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.quality = QualityAnalyzer(
            ticker
        )

        self.growth = GrowthAnalyzer(
            ticker
        )

    # =====================================
    # ROE SCORE
    # =====================================

    def roe_score(self):

        roe = self.quality.roe()

        if roe is None:
            return None

        roe *= 100

        if roe >= 25:
            return 100

        elif roe >= 20:
            return 90

        elif roe >= 15:
            return 80

        elif roe >= 10:
            return 60

        return 30

    # =====================================
    # ROIC SCORE
    # =====================================

    def roic_score(self):

        roic = self.quality.roic()

        if roic is None:
            return None

        roic *= 100

        if roic >= 25:
            return 100

        elif roic >= 20:
            return 90

        elif roic >= 15:
            return 80

        elif roic >= 10:
            return 60

        return 30

    # =====================================
    # MARGIN SCORE
    # =====================================

    def margin_score(self):

        margin = self.quality.net_margin()

        if margin is None:
            return None

        margin *= 100

        if margin >= 25:
            return 100

        elif margin >= 20:
            return 90

        elif margin >= 15:
            return 80

        elif margin >= 10:
            return 60

        return 30

    # =====================================
    # GROWTH SCORE
    # =====================================

    def growth_score(self):

        growth = self.growth.summary()

        revenue_growth = growth.get(
            "revenue_cagr_5y"
        )

        if revenue_growth is None:
            return None

        if revenue_growth >= 20:
            return 100

        elif revenue_growth >= 15:
            return 90

        elif revenue_growth >= 10:
            return 80

        elif revenue_growth >= 5:
            return 60

        return 30

    # =====================================
    # FCF SCORE
    # =====================================

    def fcf_score(self):

        if self.quality.positive_fcf():
            return 100

        return 30

    # =====================================
    # MOAT SCORE
    # =====================================

    def moat_score(self):

        scores = []

        metrics = [

            self.roe_score(),
            self.roic_score(),
            self.margin_score(),
            self.growth_score(),
            self.fcf_score()
        ]

        for metric in metrics:

            if metric is not None:

                scores.append(metric)

        if len(scores) == 0:
            return None

        return round(
            np.mean(scores),
            2
        )

    # =====================================
    # MOAT RATING
    # =====================================

    def moat_rating(self):

        score = self.moat_score()

        if score is None:
            return "UNKNOWN"

        if score >= 90:
            return "WIDE MOAT"

        elif score >= 75:
            return "NARROW MOAT"

        elif score >= 60:
            return "AVERAGE"

        return "WEAK"

    # =====================================
    # SUMMARY
    # =====================================

    def summary(self):

        return {

            "roe_score":
                self.roe_score(),

            "roic_score":
                self.roic_score(),

            "margin_score":
                self.margin_score(),

            "growth_score":
                self.growth_score(),

            "fcf_score":
                self.fcf_score(),

            "moat_score":
                self.moat_score(),

            "moat_rating":
                self.moat_rating()
        }