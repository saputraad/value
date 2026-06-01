class FinancialMetrics:

    def __init__(self, data):

        self.data = data or {}

        self.income = data.get(
            "income_statement"
        )

        self.balance = data.get(
            "balance_sheet"
        )

        self.cashflow = data.get(
            "cashflow"
        )

        self.info = data.get(
            "info",
            {}
        )

    # ======================
    # SHARES
    # ======================

    def shares(self):

        return self.data.get(
            "shares_outstanding"
        )

    # ======================
    # NET INCOME
    # ======================

    def net_income(self):

        if self.income is None:
            return None

        keys = [

            "Net Income",

            "Net Income Common Stockholders"
        ]

        for key in keys:

            if key in self.income.index:

                return self.income.loc[
                    key
                ].iloc[0]

        return None

    # ======================
    # TOTAL EQUITY
    # ======================

    def total_equity(self):

        if self.balance is None:
            return None

        keys = [

            "Stockholders Equity",

            "Total Stockholders Equity",

            "Total Equity Gross Minority Interest"
        ]

        for key in keys:

            if key in self.balance.index:

                return self.balance.loc[
                    key
                ].iloc[0]

        return None
