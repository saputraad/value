import numpy as np

from core.data_provider import (
    get_income_statement,
    get_balance_sheet,
    get_cashflow,
    get_company_info,
    get_market_cap
)

from core.utils import (
    find_row,
    safe_value
)


class RiskAnalyzerV2:

    def __init__(self, ticker):

        self.ticker = ticker

        self.income = get_income_statement(ticker)

        self.balance = get_balance_sheet(ticker)

        self.cashflow = get_cashflow(ticker)

        self.info = get_company_info(ticker)

        self.market_cap = get_market_cap(ticker)

    # ==========================================
    # PIOTROSKI
    # ==========================================

    def piotroski_score(self):

        score = 0

        try:

            net_income = find_row(
                self.income,
                [
                    "Net Income",
                    "Net Income Common Stockholders"
                ]
            )

            ocf = find_row(
                self.cashflow,
                [
                    "Operating Cash Flow",
                    "Cash Flow From Continuing Operating Activities"
                ]
            )

            total_assets = find_row(
                self.balance,
                [
                    "Total Assets"
                ]
            )

            debt = find_row(
                self.balance,
                [
                    "Total Debt"
                ]
            )

            current_assets = find_row(
                self.balance,
                [
                    "Current Assets"
                ]
            )

            current_liabilities = find_row(
                self.balance,
                [
                    "Current Liabilities"
                ]
            )

            revenue = find_row(
                self.income,
                [
                    "Total Revenue"
                ]
            )

            gross_profit = find_row(
                self.income,
                [
                    "Gross Profit"
                ]
            )

            # -----------------------------
            # ROA Positive
            # -----------------------------

            if (
                net_income is not None and
                total_assets is not None
            ):

                roa = (
                    safe_value(net_income, 0)
                    /
                    safe_value(total_assets, 0)
                )

                if roa > 0:
                    score += 1

            # -----------------------------
            # CFO Positive
            # -----------------------------

            if ocf is not None:

                if safe_value(ocf, 0) > 0:
                    score += 1

            # -----------------------------
            # Delta ROA
            # -----------------------------

            if (
                net_income is not None and
                total_assets is not None
                and len(net_income) > 1
            ):

                roa_now = (
                    safe_value(net_income, 0)
                    /
                    safe_value(total_assets, 0)
                )

                roa_prev = (
                    safe_value(net_income, 1)
                    /
                    safe_value(total_assets, 1)
                )

                if roa_now > roa_prev:
                    score += 1

            # -----------------------------
            # CFO > NI
            # -----------------------------

            if (
                ocf is not None and
                net_income is not None
            ):

                if safe_value(ocf, 0) > safe_value(net_income, 0):
                    score += 1

            # -----------------------------
            # Lower Leverage
            # -----------------------------

            if debt is not None and len(debt) > 1:

                if safe_value(debt, 0) < safe_value(debt, 1):
                    score += 1

            # -----------------------------
            # Better Liquidity
            # -----------------------------

            if (
                current_assets is not None and
                current_liabilities is not None and
                len(current_assets) > 1
            ):

                cr_now = (
                    safe_value(current_assets, 0)
                    /
                    safe_value(current_liabilities, 0)
                )

                cr_prev = (
                    safe_value(current_assets, 1)
                    /
                    safe_value(current_liabilities, 1)
                )

                if cr_now > cr_prev:
                    score += 1

            # -----------------------------
            # No Dilution
            # -----------------------------

            shares = self.info.get(
                "sharesOutstanding",
                None
            )

            if shares is not None:
                score += 1

            # -----------------------------
            # Gross Margin Improvement
            # -----------------------------

            if (
                gross_profit is not None and
                revenue is not None and
                len(gross_profit) > 1
            ):

                gm_now = (
                    safe_value(gross_profit, 0)
                    /
                    safe_value(revenue, 0)
                )

                gm_prev = (
                    safe_value(gross_profit, 1)
                    /
                    safe_value(revenue, 1)
                )

                if gm_now > gm_prev:
                    score += 1

            # -----------------------------
            # Asset Turnover Improvement
            # -----------------------------

            if (
                revenue is not None and
                total_assets is not None and
                len(revenue) > 1
            ):

                at_now = (
                    safe_value(revenue, 0)
                    /
                    safe_value(total_assets, 0)
                )

                at_prev = (
                    safe_value(revenue, 1)
                    /
                    safe_value(total_assets, 1)
                )

                if at_now > at_prev:
                    score += 1

            return min(score, 9)

        except:

            return None

    # ==========================================
    # ALTMAN Z
    # ==========================================

    def altman_z_score(self):

        try:

            total_assets = find_row(
                self.balance,
                ["Total Assets"]
            )

            current_assets = find_row(
                self.balance,
                ["Current Assets"]
            )

            current_liabilities = find_row(
                self.balance,
                ["Current Liabilities"]
            )

            retained_earnings = find_row(
                self.balance,
                ["Retained Earnings"]
            )

            ebit = find_row(
                self.income,
                [
                    "EBIT",
                    "Operating Income"
                ]
            )

            total_liabilities = find_row(
                self.balance,
                [
                    "Total Liabilities Net Minority Interest"
                ]
            )

            revenue = find_row(
                self.income,
                ["Total Revenue"]
            )

            TA = safe_value(total_assets)

            WC = (
                safe_value(current_assets)
                -
                safe_value(current_liabilities)
            )

            RE = safe_value(retained_earnings)

            EBIT = safe_value(ebit)

            TL = safe_value(total_liabilities)

            SALES = safe_value(revenue)

            MVE = self.market_cap

            if None in [TA, WC, RE, EBIT, TL, SALES, MVE]:
                return None

            A = WC / TA
            B = RE / TA
            C = EBIT / TA
            D = MVE / TL
            E = SALES / TA

            z = (
                1.2 * A +
                1.4 * B +
                3.3 * C +
                0.6 * D +
                1.0 * E
            )

            return round(z, 2)

        except:

            return None

    # ==========================================
    # BENEISH
    # ==========================================

    def beneish_score(self):

        """
        Full Beneish membutuhkan
        banyak field yang sering
        tidak tersedia di Yahoo.

        V2:
        Return None jika tidak cukup data.
        """

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

            if altman > 3:
                scores.append(100)

            elif altman > 2:
                scores.append(80)

            elif altman > 1.8:
                scores.append(60)

            else:
                scores.append(20)

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

            "piotroski":
                self.piotroski_score(),

            "altman_z":
                self.altman_z_score(),

            "beneish":
                self.beneish_score(),

            "risk_score":
                self.risk_score()
        }
        
    def get_market_cap(ticker):

    info = get_company_info(
        ticker
    )

    return info.get(
        "marketCap"
    )