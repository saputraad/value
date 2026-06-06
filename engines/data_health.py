class DataHealthAnalyzer:

    def __init__(self, data):

        self.data = data

    def summary(self):

        checks = {

            "price":
                self.data.get("price") is not None,

            "market_cap":
                self.data.get("market_cap") is not None,

            "income_statement":
                self.data.get("income_statement") is not None
                and
                not self.data.get("income_statement").empty,

            "balance_sheet":
                self.data.get("balance_sheet") is not None
                and
                not self.data.get("balance_sheet").empty,

            "cashflow":
                self.data.get("cashflow") is not None
                and
                not self.data.get("cashflow").empty

        }

        score = round(

            sum(checks.values())
            /
            len(checks)
            *
            100,

            2

        )

        if score >= 100:

            rating = "HEALTHY"

        elif score >= 80:

            rating = "PARTIAL"

        else:

            rating = "BROKEN"

        return {

            "checks":
                checks,

            "data_health_score":
                score,

            "data_health_rating":
                rating

        }
