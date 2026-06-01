import numpy as np


def safe_get(df, names):

    if df is None or df.empty:
        return None

    for name in names:

        if name in df.index:
            return df.loc[name]

    return None


class CashflowQualityAnalyzer:

    def __init__(self, data):

        self.data = data

    # ==========================
    # FREE CASH FLOW
    # ==========================

    def free_cash_flow_series(self):

        try:

            cashflow = self.data["cashflow"]

            fcf = safe_get(
                cashflow,
                [
                    "Free Cash Flow"
                ]
            )

            if fcf is None:
                return None

            return fcf.dropna()

        except:

            return None

    # ==========================
    # FCF CAGR
    # ==========================

    def fcf_growth(self):

        try:

            fcf = self.free_cash_flow_series()

            if fcf is None:
                return None

            values = list(
                reversed(
                    fcf.values.astype(float)
                )
            )

            if len(values) < 3:
                return None

            first = values[0]
            last = values[-1]

            if first <= 0:
                return None

            years = len(values) - 1

            return (
                (last / first)
                **
                (1 / years)
                - 1
            )

        except:

            return None

    # ==========================
    # POSITIVE YEARS
    # ==========================

    def positive_years(self):

        try:

            fcf = self.free_cash_flow_series()

            if fcf is None:
                return 0

            return int(
                sum(fcf > 0)
            )

        except:

            return 0

    # ==========================
    # SCORE
    # ==========================

    def score(self):

        score = 0

        positive = self.positive_years()

        growth = self.fcf_growth()

        if positive >= 5:
            score += 60

        elif positive >= 4:
            score += 50

        elif positive >= 3:
            score += 40

        elif positive >= 2:
            score += 20

        if growth is not None:

            growth_pct = growth * 100

            if growth_pct >= 15:
                score += 40

            elif growth_pct >= 10:
                score += 30

            elif growth_pct >= 5:
                score += 20

            elif growth_pct >= 0:
                score += 10

        return min(score, 100)

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        growth = self.fcf_growth()

        return {

            "fcf_growth":
                growth,

            "positive_years":
                self.positive_years(),

            "cashflow_score":
                self.score()
        }
