class TerminalQualityAnalyzer:

    def __init__(
        self,
        data
    ):
        self.data = data

    def latest_net_income(self):

        income = self.data[
            "income_statement"
        ]

        candidates = [

            "Net Income",
            "Net Income Common Stockholders",
            "Net Income Continuous Operations"

        ]

        for row in candidates:

            if row in income.index:

                values = (
                    income.loc[row]
                    .dropna()
                )

                if len(values) > 0:

                    return float(
                        values.iloc[0]
                    )

        return None

    def latest_cfo(self):

        cashflow = self.data[
            "cashflow"
        ]

        candidates = [

            "Operating Cash Flow",
            "Cash Flow From Continuing Operating Activities",
            "Net Cash Provided By Operating Activities",
            "Cash Flowsfromusedin Operating Activities Direct"

        ]

        for row in candidates:

            if row in cashflow.index:

                values = (
                    cashflow.loc[row]
                    .dropna()
                )

                if len(values) > 0:

                    return float(
                        values.iloc[0]
                    )

        return None

    def score(self):

        score = 100

        net_income = (
            self.latest_net_income()
        )

        cfo = (
            self.latest_cfo()
        )

        if net_income is not None:

            if net_income <= 0:

                score *= 0.7

        if cfo is not None:

            if cfo <= 0:

                score *= 0.8

        return round(
            score,
            2
        )

    def summary(self):

        return {

            "terminal_quality_score":
            self.score()

        }
