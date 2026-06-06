class DataHealthAnalyzer:

    def __init__(self, data):

        self.data = data

    def score(self):

        checks = [

            self.data.get(
                "income_statement"
            ) is not None,

            self.data.get(
                "balance_sheet"
            ) is not None,

            self.data.get(
                "cashflow"
            ) is not None,

            self.data.get(
                "market_cap"
            ) is not None,

            self.data.get(
                "price"
            ) is not None

        ]

        valid = sum(checks)

        return round(
            valid / len(checks) * 100,
            2
        )

    def rating(self):

        score = self.score()

        if score >= 90:
            return "HEALTHY"

        elif score >= 70:
            return "PARTIAL"

        return "BROKEN"

    def summary(self):

        return {

            "data_health_score":
                self.score(),

            "data_health_rating":
                self.rating()

        }
