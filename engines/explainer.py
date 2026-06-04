class BuffettExplainer:

    def __init__(
        self,
        quality,
        moat,
        predictability,
        trajectory,
        cashflow,
        valuation
    ):

        self.quality = quality
        self.moat = moat
        self.predictability = predictability
        self.trajectory = trajectory
        self.cashflow = cashflow
        self.valuation = valuation

    def strengths(self):

        items = []

        if self.moat >= 80:
            items.append(
                "Wide moat"
            )

        if self.predictability >= 90:
            items.append(
                "Excellent predictability"
            )

        if self.cashflow >= 80:
            items.append(
                "Strong cashflow"
            )

        if self.quality >= 80:
            items.append(
                "High quality business"
            )

        if self.trajectory >= 80:
            items.append(
                "Strong business momentum"
            )

        if self.valuation >= 80:
            items.append(
                "Attractive valuation"
            )

        return items

    def weaknesses(self):

        items = []

        if self.moat < 60:
            items.append(
                "Weak competitive advantage"
            )

        if self.predictability < 70:
            items.append(
                "Unpredictable earnings"
            )

        if self.cashflow < 60:
            items.append(
                "Weak cash generation"
            )

        if self.quality < 60:
            items.append(
                "Business quality below average"
            )

        if self.trajectory < 60:
            items.append(
                "Weak growth trajectory"
            )

        if self.valuation < 60:
            items.append(
                "Not attractively valued"
            )

        return items

    def summary(self):

        return {

            "strengths":
                self.strengths(),

            "weaknesses":
                self.weaknesses()
        }
