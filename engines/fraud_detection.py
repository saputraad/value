import numpy as np

from core.data_provider import (
    get_income_statement,
    get_balance_sheet,
    get_cashflow
)

from core.utils import (
    get_metric,
    safe_value
)


class FraudDetectionAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.income = get_income_statement(
            ticker
        )

        self.balance = get_balance_sheet(
            ticker
        )

        self.cashflow = get_cashflow(
            ticker
        )

    # =====================================
    # NET INCOME
    # =====================================

    def net_income(self):

        ni = get_metric(
            self.income,
            "net_income"
        )

        if ni is None:
            return None

        return safe_value(ni)

    # =====================================
    # OPERATING CASHFLOW
    # =====================================

    def operating_cashflow(self):

        ocf = get_metric(
            self.cashflow,
            "operating_cashflow"
        )

        if ocf is None:
            return None

        return safe_value(ocf)

    # =====================================
    # CASH CONVERSION
    # =====================================

    def cash_conversion_ratio(self):

        try:

            ni = self.net_income()
            ocf = self.operating_cashflow()

            if ni is None:
                return None

            if ni <= 0:
                return None

            return ocf / ni

        except:

            return None

    # =====================================
    # ACCRUAL RATIO
    # =====================================

    def accrual_ratio(self):

        try:

            ni = self.net_income()

            ocf = self.operating_cashflow()

            assets = get_metric(
                self.balance,
                "total_assets"
            )

            total_assets = safe_value(
                assets
            )

            if None in [
                ni,
                ocf,
                total_assets
            ]:
                return None

            return (
                (ni - ocf)
                /
                total_assets
            )

        except:

            return None

    # =====================================
    # RECEIVABLE ANALYSIS
    # =====================================

    def receivable_growth_risk(self):

        receivable = get_metric(
            self.balance,
            "receivables"
        )

        revenue = get_metric(
            self.income,
            "revenue"
        )

        if (
            receivable is None
            or revenue is None
        ):
            return None

        try:

            rec_growth = (
                (
                    safe_value(receivable, 0)
                    -
                    safe_value(receivable, 1)
                )
                /
                safe_value(receivable, 1)
            )

            rev_growth = (
                (
                    safe_value(revenue, 0)
                    -
                    safe_value(revenue, 1)
                )
                /
                safe_value(revenue, 1)
            )

            if rec_growth > rev_growth * 2:

                return "HIGH"

            elif rec_growth > rev_growth:

                return "MEDIUM"

            return "LOW"

        except:

            return None

    # =====================================
    # EARNINGS QUALITY
    # =====================================

    def earnings_quality_score(self):

        score = []

        cash_conversion = (
            self.cash_conversion_ratio()
        )

        if cash_conversion is not None:

            if cash_conversion >= 1.2:
                score.append(100)

            elif cash_conversion >= 1:
                score.append(90)

            elif cash_conversion >= 0.8:
                score.append(70)

            else:
                score.append(30)

        accrual = self.accrual_ratio()

        if accrual is not None:

            if accrual < 0:
                score.append(100)

            elif accrual < 0.05:
                score.append(80)

            elif accrual < 0.1:
                score.append(60)

            else:
                score.append(20)

        risk = self.receivable_growth_risk()

        if risk == "LOW":
            score.append(100)

        elif risk == "MEDIUM":
            score.append(60)

        elif risk == "HIGH":
            score.append(20)

        if len(score) == 0:
            return None

        return round(
            np.mean(score),
            2
        )

    # =====================================
    # FRAUD SCORE
    # =====================================

    def fraud_score(self):

        quality = self.earnings_quality_score()

        if quality is None:
            return None

        return round(
            100 - quality,
            2
        )

    # =====================================
    # FRAUD RATING
    # =====================================

    def fraud_rating(self):

        score = self.fraud_score()

        if score is None:
            return "UNKNOWN"

        if score < 20:
            return "LOW"

        elif score < 40:
            return "MEDIUM"

        elif score < 60:
            return "HIGH"

        return "VERY_HIGH"

    # =====================================
    # SUMMARY
    # =====================================

    def summary(self):

        return {

            "cash_conversion":
                self.cash_conversion_ratio(),

            "accrual_ratio":
                self.accrual_ratio(),

            "receivable_risk":
                self.receivable_growth_risk(),

            "earnings_quality":
                self.earnings_quality_score(),

            "fraud_score":
                self.fraud_score(),

            "fraud_rating":
                self.fraud_rating()
        }