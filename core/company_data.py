from core.data_provider import (
    get_company_info,
    get_income_statement,
    get_balance_sheet,
    get_cashflow,
    get_price_history,
    get_current_price
)

from core.cache_manager import (
    CacheManager
)


class CompanyData:

    def __init__(
        self,
        ticker
    ):

        self.ticker = ticker

        self._load()

    # ==========================
    # LOAD DATA
    # ==========================

    def _load(self):

        cache_key = (
            f"{self.ticker}_company"
        )

        cached = CacheManager.load(
            cache_key,
            max_age_hours=12
        )

        if cached:

            self.info = cached["info"]

            self.income_statement = cached["income"]

            self.balance_sheet = cached["balance"]

            self.cashflow = cached["cashflow"]

            self.price_history = cached["price_history"]

            self.current_price = cached["current_price"]

            return

        self.info = get_company_info(
            self.ticker
        )

        self.income_statement = (
            get_income_statement(
                self.ticker
            )
        )

        self.balance_sheet = (
            get_balance_sheet(
                self.ticker
            )
        )

        self.cashflow = (
            get_cashflow(
                self.ticker
            )
        )

        self.price_history = (
            get_price_history(
                self.ticker
            )
        )

        self.current_price = (
            get_current_price(
                self.ticker
            )
        )

        CacheManager.save(

            cache_key,

            {
                "info":
                    self.info,

                "income":
                    self.income_statement,

                "balance":
                    self.balance_sheet,

                "cashflow":
                    self.cashflow,

                "price_history":
                    self.price_history,

                "current_price":
                    self.current_price
            }
        )