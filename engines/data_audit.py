class DataAudit:

    def __init__(self, data):

        self.data = data or {}

    def check_price(self):

        return self.data.get(
            "price"
        ) is not None

    def check_shares(self):

        return self.data.get(
            "shares_outstanding"
        ) is not None

    def check_income_statement(self):

        income = self.data.get(
            "income_statement"
        )

        return (
            income is not None
            and
            not income.empty
        )

    def check_balance_sheet(self):

        balance = self.data.get(
            "balance_sheet"
        )

        return (
            balance is not None
            and
            not balance.empty
        )

    def check_cashflow(self):

        cashflow = self.data.get(
            "cashflow"
        )

        return (
            cashflow is not None
            and
            not cashflow.empty
        )

    def score(self):

        checks = [

            self.check_price(),

            self.check_shares(),

            self.check_income_statement(),

            self.check_balance_sheet(),

            self.check_cashflow()

        ]

        return round(
            (
                sum(checks)
                /
                len(checks)
            )
            *
            100,
            2
        )

    def summary(self):

        return {

            "price":
                self.check_price(),

            "shares":
                self.check_shares(),

            "income_statement":
                self.check_income_statement(),

            "balance_sheet":
                self.check_balance_sheet(),

            "cashflow":
                self.check_cashflow(),

            "data_quality":
                self.score()
        }
