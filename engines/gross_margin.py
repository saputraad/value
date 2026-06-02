def safe_get(df, names):

    if df is None or df.empty:
        return None

    for name in names:

        if name in df.index:
            return df.loc[name]

    return None


class GrossMarginAnalyzer:

    def __init__(self, data):

        self.data = data

    # ==========================
    # GROSS MARGIN
    # ==========================

    def gross_margin(self):

        try:

            income = self.data[
                "income_statement"
            ]

            gross_profit = safe_get(
                income,
                [
                    "Gross Profit"
                ]
            )

            revenue = safe_get(
                income,
                [
                    "Total Revenue",
                    "Revenue"
                ]
            )

            if gross_profit is None:
                return None

            if revenue is None:
                return None

            gp = float(
                gross_profit.iloc[0]
            )

            rev = float(
                revenue.iloc[0]
            )

            if rev <= 0:
                return None

            return gp / rev

        except:

            return None

    # ==========================
    # SCORE
    # ==========================

    def score(self):

        margin = self.gross_margin()

        if margin is None:
            return None

        pct = margin * 100

        if pct >= 60:
            return 100

        elif pct >= 50:
            return 90

        elif pct >= 40:
            return 80

        elif pct >= 30:
            return 70

        elif pct >= 20:
            return 50

        return 20

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "gross_margin":
                self.gross_margin(),

            "gross_margin_score":
                self.score()
        }
