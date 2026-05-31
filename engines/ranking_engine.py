import pandas as pd
import numpy as np

from engines.scoring import (
    InvestmentScoringEngine
)

from engines.sector_classifier import (
    SectorClassifier
)

class RankingEngine:

    def __init__(self, tickers):

        self.tickers = tickers
		
		
    def analyze_stock(self, ticker):

        try:

            scoring = (
                InvestmentScoringEngine(
                    ticker
                )
            )

            sector = (
                SectorClassifier(
                    ticker
                )
            )

            result = scoring.summary()

            result["sector"] = (
                sector.classify()
            )

            return result

        except Exception:

            return None
			
	def rank(self):

        results = []

        for ticker in self.tickers:

            data = self.analyze_stock(
                ticker
            )

            if data:

                results.append(data)

        if len(results) == 0:

            return pd.DataFrame()

        df = pd.DataFrame(results)

        df = df.sort_values(
            "overall_score",
            ascending=False
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        df.index += 1

        return df
		
	def top_value(
        self,
        top_n=20
    ):

        rows = []

        for ticker in self.tickers:

            try:

                score = (
                    InvestmentScoringEngine(
                        ticker
                    )
                )

                rows.append({

                    "ticker":
                        ticker,

                    "value_score":
                        score.value_score()
                })

            except:

                pass

        df = pd.DataFrame(rows)

        return (
            df.sort_values(
                "value_score",
                ascending=False
            )
            .head(top_n)
        )
		
	def top_growth(
        self,
        top_n=20
    ):

        rows = []

        for ticker in self.tickers:

            try:

                score = (
                    InvestmentScoringEngine(
                        ticker
                    )
                )

                rows.append({

                    "ticker":
                        ticker,

                    "growth_score":
                        score.growth_score()
                })

            except:

                pass

        df = pd.DataFrame(rows)

        return (
            df.sort_values(
                "growth_score",
                ascending=False
            )
            .head(top_n)
        )
		
	def top_compounders(
        self,
        top_n=20
    ):

        rows = []

        for ticker in self.tickers:

            try:

                score = (
                    InvestmentScoringEngine(
                        ticker
                    )
                )

                overall = (
                    score.overall_score()
                )

                quality = (
                    score.quality_score()
                )

                growth = (
                    score.growth_score()
                )

                if (
                    overall is not None
                    and quality is not None
                    and growth is not None
                ):

                    compounder = (
                        quality * 0.5
                        +
                        growth * 0.5
                    )

                    rows.append({

                        "ticker":
                            ticker,

                        "compounder":
                            compounder
                    })

            except:

                pass

        df = pd.DataFrame(rows)

        return (
            df.sort_values(
                "compounder",
                ascending=False
            )
            .head(top_n)
        )