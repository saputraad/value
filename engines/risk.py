import numpy as np

from core.data_provider import (
    get_income_statement,
    get_balance_sheet,
    get_cashflow,
    get_company_info
)


class RiskAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.income = get_income_statement(ticker)

        self.balance = get_balance_sheet(ticker)

        self.cashflow = get_cashflow(ticker)

        self.info = get_company_info(ticker)

    # ==========================================
    # HELPER
    # ==========================================

    def find_row(self, df, names):

        try:

            for name in names:

                if name in df.index:
                    return df.loc[name]

            return None

        except:
            return None

    # ==========================================
    # PIOTROSKI F SCORE
    # ==========================================

    def piotroski_score(self):

        """
        Simplified V1

        Max = 9
        """

        score = 0

        try:

            net_income = self.find_row(
                self.income,
                [
                    "Net Income",
                    "Net Income Common Stockholders"
                ]
            )

            if net_income is not None:

                current_ni = float(net_income.iloc[0])

                if current_ni > 0:
                    score += 1

            ocf = self.find_row(
                self.cashflow,
                [
                    "Operating Cash Flow",
                    "Cash Flow From Continuing Operating Activities"
                ]
            )

            if ocf is not None:

                current_ocf = float(ocf.iloc[0])

                if current_ocf > 0:
                    score += 1

            if (
                net_income is not None and
                ocf is not None
            ):

                if current_ocf > current_ni:
                    score += 1

            debt = self.find_row(
                self.balance,
                [
                    "Total Debt"
                ]
            )

            if debt is not None and len(debt) >= 2:

                if debt.iloc[0] < debt.iloc[1]:
                    score += 1

            current_assets = self.find_row(
                self.balance,
                [
                    "Current Assets"
                ]
            )

            current_liabilities = self.find_row(
                self.balance,
                [
                    "Current Liabilities"
                ]
            )

            if (
                current_assets is not None and
                current_liabilities is not None and
                len(current_assets) >= 2 and
                len(current_liabilities) >= 2
            ):

                current_ratio_now = (
                    current_assets.iloc[0]
                    /
                    current_liabilities.iloc[0]
                )

                current_ratio_prev = (
                    current_assets.iloc[1]
                    /
                    current_liabilities.iloc[1]
                )

                if current_ratio_now > current_ratio_prev:
                    score += 1

            gross_margin = self.info.get(
                "grossMargins",
                None
            )

            if gross_margin is not None:

                if gross_margin > 0.25:
                    score += 1

            operating_margin = self.info.get(
                "operatingMargins",
                None
            )

            if operating_margin is not None:

                if operating_margin > 0.10:
                    score += 1

            roe = self.info.get(
                "returnOnEquity",
                None
            )

            if roe is not None:

                if roe > 0.10:
                    score += 1

            asset_turnover = self.info.get(
                "revenuePerShare",
                None
            )

            if asset_turnover is not None:

                score += 1

            return min(score, 9)

        except:

            return None

    # ==========================================
    # ALTMAN Z SCORE
    # ==========================================

    def altman_z_score(self):

        """
        Simplified approximation.

        Full version later.
        """

        try:

            debt = self.find_row(
                self.balance,
                [
                    "Total Debt"
                ]
            )

            equity = self.find_row(
                self.balance,
                [
                    "Stockholders Equity",
                    "Total Equity Gross Minority Interest"
                ]
            )

            if debt is None:
                return None

            if equity is None:
                return None

            debt = float(debt.iloc[0])

            equity = float(equity.iloc[0])

            if debt <= 0:
                return 5.0

            return round(
                equity / debt,
                2
            )

        except:

            return None

    # ==========================================
    # BENEISH M SCORE
    # ==========================================

    def beneish_score(self):

        """
        Placeholder V1.

        Full Beneish needs
        2-year detailed statements.
        """

        try:

            margin = self.info.get(
                "profitMargins",
                None
            )

            if margin is None:
                return None

            if margin > 0.20:
                return -2.5

            return -2.0

        except:

            return None

    # ==========================================
    # RISK SCORE
    # ==========================================

    def risk_score(self):

        scores = []

        piotroski = self.piotroski_score()

        if piotroski is not None:

            scores.append(
                (piotroski / 9) * 100
            )

        altman = self.altman_z_score()

        if altman is not None:

            if altman >= 3:
                scores.append(100)

            elif altman >= 2:
                scores.append(80)

            elif altman >= 1:
                scores.append(60)

            else:
                scores.append(20)

        beneish = self.beneish_score()

        if beneish is not None:

            if beneish <= -2.22:
                scores.append(100)

            else:
                scores.append(50)

        if len(scores) == 0:
            return None

        return round(
            np.mean(scores),
            2
        )

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self):

        return {

            "piotroski_score":
                self.piotroski_score(),

            "altman_z":
                self.altman_z_score(),

            "beneish_m":
                self.beneish_score(),

            "risk_score":
                self.risk_score()
        }