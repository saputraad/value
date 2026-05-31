import pandas as pd
import numpy as np

from core.data_provider import (
    get_price_history
)


class TechnicalAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.df = get_price_history(
            ticker,
            period="5y"
        ).copy()

    # =====================================
    # MOVING AVERAGE
    # =====================================

    def add_ma(self):

        self.df["MA20"] = (
            self.df["Close"]
            .rolling(20)
            .mean()
        )

        self.df["MA50"] = (
            self.df["Close"]
            .rolling(50)
            .mean()
        )

        self.df["MA200"] = (
            self.df["Close"]
            .rolling(200)
            .mean()
        )

    # =====================================
    # RSI
    # =====================================

    def add_rsi(self, period=14):

        delta = self.df["Close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()

        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        self.df["RSI"] = (
            100 -
            (
                100 / (1 + rs)
            )
        )

    # =====================================
    # MACD
    # =====================================

    def add_macd(self):

        ema12 = self.df["Close"].ewm(
            span=12,
            adjust=False
        ).mean()

        ema26 = self.df["Close"].ewm(
            span=26,
            adjust=False
        ).mean()

        self.df["MACD"] = ema12 - ema26

        self.df["MACD_SIGNAL"] = (
            self.df["MACD"]
            .ewm(
                span=9,
                adjust=False
            )
            .mean()
        )

    # =====================================
    # PREPARE
    # =====================================

    def prepare(self):

        self.add_ma()
        self.add_rsi()
        self.add_macd()

        return self.df

    # =====================================
    # LAST ROW
    # =====================================

    def latest(self):

        self.prepare()

        return self.df.iloc[-1]

    # =====================================
    # TREND
    # =====================================

    def trend_signal(self):

        row = self.latest()

        if (
            row["MA20"] >
            row["MA50"] >
            row["MA200"]
        ):
            return "STRONG_BULLISH"

        if (
            row["MA50"] >
            row["MA200"]
        ):
            return "BULLISH"

        if (
            row["MA20"] <
            row["MA50"] <
            row["MA200"]
        ):
            return "STRONG_BEARISH"

        return "NEUTRAL"

    # =====================================
    # GOLDEN CROSS
    # =====================================

    def golden_cross(self):

        self.prepare()

        if len(self.df) < 3:
            return False

        prev = self.df.iloc[-2]
        now = self.df.iloc[-1]

        return (
            prev["MA50"] <= prev["MA200"]
            and
            now["MA50"] > now["MA200"]
        )

    # =====================================
    # DEATH CROSS
    # =====================================

    def death_cross(self):

        self.prepare()

        if len(self.df) < 3:
            return False

        prev = self.df.iloc[-2]
        now = self.df.iloc[-1]

        return (
            prev["MA50"] >= prev["MA200"]
            and
            now["MA50"] < now["MA200"]
        )

    # =====================================
    # ENTRY SCORE
    # =====================================

    def entry_score(self):

        score = []

        row = self.latest()

        trend = self.trend_signal()

        if trend == "STRONG_BULLISH":
            score.append(100)

        elif trend == "BULLISH":
            score.append(80)

        elif trend == "NEUTRAL":
            score.append(50)

        else:
            score.append(20)

        rsi = row["RSI"]

        if 45 <= rsi <= 65:
            score.append(100)

        elif 35 <= rsi <= 75:
            score.append(80)

        else:
            score.append(40)

        if row["MACD"] > row["MACD_SIGNAL"]:
            score.append(90)

        else:
            score.append(40)

        return round(
            np.mean(score),
            2
        )

    # =====================================
    # SUMMARY
    # =====================================

    def summary(self):

        row = self.latest()

        return {

            "price":
                float(row["Close"]),

            "ma20": (
                float(row["MA20"])
                if pd.notna(row["MA20"])
                else None
            ),

            "ma50": (
                float(row["MA50"])
                if pd.notna(row["MA50"])
                else None
            ),

            "ma200": (
                float(row["MA200"])
                if pd.notna(row["MA200"])
                else None
            ),

            "rsi": (
                float(row["RSI"])
                if pd.notna(row["RSI"])
                else None
            ),

            "macd": (
                float(row["MACD"])
                if pd.notna(row["MACD"])
                else None
            ),

            "macd_signal": (
                float(row["MACD_SIGNAL"])
                if pd.notna(row["MACD_SIGNAL"])
                else None
            ),

            "trend":
                self.trend_signal(),

            "golden_cross":
                self.golden_cross(),

            "death_cross":
                self.death_cross(),

            "entry_score":
                self.entry_score()
        }
