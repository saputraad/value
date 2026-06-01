def safe_get(df, names):

    if df is None or df.empty:
        return None

    for name in names:

        if name in df.index:
            return df.loc[name]

    return None


class ROICAnalyzer:

    def __init__(self, data):

        self.data = data

    # =================================
    # NOPAT
    # =================================

    def nopat(self):

        try:

            income = self.data["income_statement"]

            operating_income = safe_get(
                income,
                [
                    "Operating Income",
                    "OperatingIncome"
                ]
            )

            if operating_income is None:
                return None

            ebit = float(
                operating_income.iloc[0]
            )

            tax_rate = 0.22

            return ebit * (
                1 - tax_rate
            )

        except:

            return None

    # =================================
    # INVESTED CAPITAL
    # =================================

    def invested_capital(self):

        try:

            balance = self.data[
                "balance_sheet"
            ]

            debt = safe_get(
                balance,
                [
                    "Total Debt",
                    "Long Term Debt"
                ]
            )

            equity = safe_get(
                balance,
                [
                    "Stockholders Equity",
                    "Common Stock Equity",
                    "Total Equity Gross Minority Interest"
                ]
            )

            if debt is None:
                debt_value = 0

            else:
                debt_value = float(
                    debt.iloc[0]
                )

            if equity is None:
                return None

            equity_value = float(
                equity.iloc[0]
            )

            return (
                debt_value +
                equity_value
            )

        except:

            return None

    # =================================
    # ROIC
    # =================================

    def roic(self):

        try:

            nopat = self.nopat()

            capital = self.invested_capital()

            if nopat is None:
                return None

            if capital is None:
                return None

            if capital <= 0:
                return None

            return nopat / capital

        except:

            return None

    # =================================
    # SCORE
    # =================================

    def score(self):

        roic = self.roic()

        if roic is None:
            return 0

        roic_pct = roic * 100

        if roic_pct >= 20:
            return 100

        elif roic_pct >= 15:
            return 90

        elif roic_pct >= 10:
            return 75

        elif roic_pct >= 5:
            return 60

        elif roic_pct >= 0:
            return 40

        return 0

    # =================================
    # SUMMARY
    # =================================

    def summary(self):

        return {

            "roic":
                self.roic(),

            "roic_score":
                self.score()
        }
