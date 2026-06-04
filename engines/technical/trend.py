import numpy as np


class TrendAnalyzer:

    def __init__(self, history):

        self.history = history

    # ==========================
    # MOVING AVERAGES
    # ==========================

    def ma20(self):

        try:

            return float(
                self.history[
                    "Close"
                ]
                .rolling(20)
                .mean()
                .iloc[-1]
            )

        except:

            return None

    def ma50(self):

        try:

            return float(
                self.history[
                    "Close"
                ]
                .rolling(50)
                .mean()
                .iloc[-1]
            )

        except:

            return None

    def ma200(self):

        try:

            return float(
                self.history[
                    "Close"
                ]
                .rolling(200)
                .mean()
                .iloc[-1]
            )

        except:

            return None

    # ==========================
    # CURRENT PRICE
    # ==========================

    def current_price(self):

        try:

            return float(
                self.history[
                    "Close"
                ]
                .iloc[-1]
            )

        except:

            return None

    # ==========================
    # SCORE
    # ==========================

    def score(self):

        price = self.current_price()

        ma20 = self.ma20()
        ma50 = self.ma50()
        ma200 = self.ma200()

        if None in [
            price,
            ma20,
            ma50,
            ma200
        ]:

            return 0

        score = 0

        if price > ma20:
            score += 25

        if price > ma50:
            score += 25

        if price > ma200:
            score += 25

        if ma20 > ma50 > ma200:
            score += 25

        return score

    # ==========================
    # SIGNAL
    # ==========================

    def signal(self):

        score = self.score()

        if score >= 100:
            return "STRONG UPTREND"

        elif score >= 75:
            return "UPTREND"

        elif score >= 50:
            return "NEUTRAL"

        return "DOWNTREND"

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "price":
                self.current_price(),

            "ma20":
                self.ma20(),

            "ma50":
                self.ma50(),

            "ma200":
                self.ma200(),

            "trend_score":
                self.score(),

            "trend_signal":
                self.signal()

        }
