from core.data_provider import (
    get_company_info
)


class BankQualityAnalyzer:

    def __init__(
        self,
        ticker,
        data
    ):

        self.ticker = ticker
        self.data = data
