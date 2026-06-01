import numpy as np


class PredictabilityAnalyzer:

    def __init__(self, data):

        self.data = data

    # ==========================
    # REVENUE STABILITY
    # ==========================

    def revenue_score(self):

        try:

            revenue = (
                self.data["income_statement"]
                .loc["Total Revenue"]
            )

            values = revenue.dropna().values

            if len(values) < 4:
                return 50

            growth_rates = []

            for i in range(len(values) - 1):

                if values[i + 1] <= 0:
                    continue

                growth = (
                    values[i]
                    /
                    values[i + 1]
                ) - 1

                growth_rates.append(
                    growth
                )

            if len(growth_rates) < 2:
                return 50

            volatility = np.std(
                growth_rates
            )

            if volatility <= 0.05:
                return 100

            elif volatility <= 0.10:
                return 80

            elif volatility <= 0.20:
                return 60

            return 30

        except:

            return 0

    # ==========================
    # EARNINGS STABILITY
    # ==========================

    def earnings_score(self):

        try:

            income = (
                self.data["income_statement"]
                .loc["Net Income"]
            )

            values = income.dropna().values

            if len(values) < 4:
                return 50

            negative_years = sum(
                1
                for x in values
                if x < 0
            )

            if negative_years == 0:
                return 100

            elif negative_years == 1:
                return 70

            return 20

        except:

            return 0

    # ==========================
    # FINAL SCORE
    # ==========================

    def predictability_score(self):

        revenue = self.revenue_score()

        earnings = self.earnings_score()

        return round(
            (
                revenue * 0.5
                +
                earnings * 0.5
            ),
            2
        )

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "revenue_stability":
                self.revenue_score(),

            "earnings_stability":
                self.earnings_score(),

            "predictability_score":
                self.predictability_score()
        }
