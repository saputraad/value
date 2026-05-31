from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def get_company_info(
        self,
        ticker
    ):
        pass

    @abstractmethod
    def get_income_statement(
        self,
        ticker
    ):
        pass

    @abstractmethod
    def get_balance_sheet(
        self,
        ticker
    ):
        pass

    @abstractmethod
    def get_cashflow(
        self,
        ticker
    ):
        pass

    @abstractmethod
    def get_price_history(
        self,
        ticker
    ):
        pass