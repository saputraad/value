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

        score = 0
        available = 0
    
        net_margin = (
            self.net_margin()
        )
    
        if net_margin is not None:
    
            available += 50
    
            pct = net_margin * 100
    
            if pct >= 20:
                score += 50
    
            elif pct >= 10:
                score += 40
    
            elif pct >= 5:
                score += 30
    
            elif pct >= 0:
                score += 20
    
        cfo_margin = (
            self.cfo_margin()
        )
    
        if cfo_margin is not None:
    
            available += 50
    
            pct = cfo_margin * 100
    
            if pct >= 20:
                score += 50
    
            elif pct >= 10:
                score += 40
    
            elif pct >= 5:
                score += 30
    
            elif pct >= 0:
                score += 20
    
        if available == 0:
            return 0
    
        return round(
            score /
            available *
            100,
            2
        )

    def summary(self):

        return {
    
            "net_margin":
                self.net_margin(),
    
            "cfo_margin":
                self.cfo_margin(),
    
            "terminal_quality_score":
                self.score()
    
        }

    def latest_revenue(self):
    
        income = self.data[
            "income_statement"
        ]
    
        candidates = [
    
            "Total Revenue",
            "Operating Revenue"
    
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

    def net_margin(self):

        revenue = (
            self.latest_revenue()
        )
    
        income = (
            self.latest_net_income()
        )
    
        if (
            revenue is None
            or revenue <= 0
            or income is None
        ):
            return None
    
        return income / revenue

    def cfo_margin(self):

        revenue = (
            self.latest_revenue()
        )
    
        cfo = (
            self.latest_cfo()
        )
    
        if (
            revenue is None
            or revenue <= 0
            or cfo is None
        ):
            return None
    
        return cfo / revenue
