import numpy as np

from core.data_provider import (
    get_company_info,
    get_income_statement,
    get_current_price
)

from core.utils import (
    get_metric,
    safe_value
)


class CommodityValuationAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.info = get_company_info(ticker)

        self.income = get_income_statement(ticker)

        self.price = get_current_price(ticker)

    # =====================================
    # EPS
    # =====================================

    def current_eps(self):

        try:
            return self.info.get(
                "trailingEps",
                None
            )
        except:
            return None

    # =====================================
    # REVENUE HISTORY
    # =====================================

    def revenue_series(self):

        return get_metric(
            self.income,
            "revenue"
        )

    # =====================================
    # NET INCOME HISTORY
    # =====================================

    def net_income_series(self):

        return get_metric(
            self.income,
            "net_income"
        )

    # =====================================
    # NORMALIZED EARNINGS
    # =====================================

    def normalized_net_income(self):

        try:

            ni = self.net_income_series()

            if ni is None:
                return None

            values = []

            for i in range(min(4, len(ni))):

                v = safe_value(ni, i)

                if v is not None:
                    values.append(v)

            if len(values) == 0:
                return None

            return np.mean(values)

        except:
            return None

    # =====================================
    # NORMALIZED EPS
    # =====================================

    def normalized_eps(self):

        try:

            current_eps = self.current_eps()

            ni = self.net_income_series()

            if (
                current_eps is None or
                ni is None
            ):
                return None

            latest_ni = safe_value(
                ni,
                0
            )

            normalized_ni = (
                self.normalized_net_income()
            )

            if (
                latest_ni is None or
                latest_ni <= 0
            ):
                return None

            ratio = (
                normalized_ni /
                latest_ni
            )

            return (
                current_eps *
                ratio
            )

        except:
            return None

    # =====================================
    # CURRENT PE
    # =====================================

    def current_pe(self):

        try:

            eps = self.current_eps()

            if (
                eps is None or
                eps <= 0
            ):
                return None

            return self.price / eps

        except:
            return None

    # =====================================
    # NORMALIZED PE
    # =====================================

    def normalized_pe(self):

        try:

            eps = self.normalized_eps()

            if (
                eps is None or
                eps <= 0
            ):
                return None

            return self.price / eps

        except:
            return None

    # =====================================
    # PEAK EARNINGS RISK
    # =====================================

    def peak_earnings_risk(self):

        try:

            current_eps = self.current_eps()

            normalized_eps = (
                self.normalized_eps()
            )

            if (
                current_eps is None or
                normalized_eps is None
            ):
                return None

            ratio = (
                current_eps /
                normalized_eps
            )

            if ratio > 2.0:
                return "VERY_HIGH"

            elif ratio > 1.5:
                return "HIGH"

            elif ratio > 1.2:
                return "MODERATE"

            return "LOW"

        except:
            return None

    # =====================================
    # FAIR VALUE
    # =====================================

    def fair_value(self):

        try:

            normalized_eps = (
                self.normalized_eps()
            )

            if normalized_eps is None:
                return None

            target_pe = 10

            return (
                normalized_eps *
                target_pe
            )

        except:
            return None

    # =====================================
    # MOS
    # =====================================

    def margin_of_safety(self):

        try:

            fair = self.fair_value()

            if fair is None:
                return None

            return (
                (
                    fair -
                    self.price
                )
                /
                fair
            ) * 100

        except:
            return None

    # =====================================
    # COMMODITY SCORE
    # =====================================

    def commodity_score(self):

        scores = []

        npe = self.normalized_pe()

        if npe is not None:

            if npe < 6:
                scores.append(100)

            elif npe < 8:
                scores.append(90)

            elif npe < 10:
                scores.append(80)

            elif npe < 15:
                scores.append(60)

            else:
                scores.append(30)

        mos = self.margin_of_safety()

        if mos is not None:

            if mos > 40:
                scores.append(100)

            elif mos > 25:
                scores.append(90)

            elif mos > 10:
                scores.append(75)

            elif mos > 0:
                scores.append(60)

            else:
                scores.append(30)

        risk = self.peak_earnings_risk()

        if risk == "LOW":
            scores.append(100)

        elif risk == "MODERATE":
            scores.append(80)

        elif risk == "HIGH":
            scores.append(50)

        elif risk == "VERY_HIGH":
            scores.append(20)

        if len(scores) == 0:
            return None

        return round(
            np.mean(scores),
            2
        )

    # =====================================
    # SUMMARY
    # =====================================

    def summary(self):

        return {

            "price":
                self.price,

            "current_pe":
                self.current_pe(),

            "normalized_pe":
                self.normalized_pe(),

            "normalized_eps":
                self.normalized_eps(),

            "fair_value":
                self.fair_value(),

            "margin_of_safety":
                self.margin_of_safety(),

            "peak_earnings_risk":
                self.peak_earnings_risk(),

            "commodity_score":
                self.commodity_score()
        }