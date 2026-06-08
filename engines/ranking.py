import pandas as pd

from engines.buffett_score import (
    BuffettScoreAnalyzer
)

from engines.valuation import (
    ValuationAnalyzer
)

from engines.buffett_decision import (
    BuffettDecisionAnalyzer
)

from engines.moat import (
    MoatAnalyzer
)

from engines.predictability import (
    PredictabilityAnalyzer
)

from engines.trajectory import (
    TrajectoryAnalyzer
)

from engines.cashflow_quality import (
    CashflowQualityAnalyzer
)

from engines.quality import (
    analyze_quality
)


class BuffettRankingEngine:

    def __init__(
        self,
        stocks_data
    ):

        self.stocks_data = stocks_data

    def run(self):

        rows = []

        for ticker, data in self.stocks_data.items():

            try:

                quality = (
                    analyze_quality(
                        data
                    )
                )

                moat = (
                    MoatAnalyzer(
                        ticker,
                        data
                    )
                    .summary()
                )

                predictability = (
                    PredictabilityAnalyzer(
                        data
                    )
                    .summary()
                )

                trajectory = (
                    TrajectoryAnalyzer(
                        data
                    )
                    .summary()
                )

                cashflow = (
                    CashflowQualityAnalyzer(
                        data
                    )
                    .summary()
                )

                business = (

                    BuffettScoreAnalyzer(

                        quality=
                            quality[
                                "quality_score"
                            ],

                        moat=
                            moat[
                                "moat_score"
                            ],

                        predictability=
                            predictability[
                                "predictability_score"
                            ],

                        trajectory=
                            trajectory[
                                "trajectory_score"
                            ],

                        cashflow=
                            cashflow[
                                "cashflow_score"
                            ]

                    )
                    .summary()

                )

                valuation = (

                    ValuationAnalyzer(
                        ticker,
                        data
                    )
                    .summary()

                )

                decision = (

                    BuffettDecisionAnalyzer(

                        business_score=
                            business[
                                "buffett_score"
                            ],

                        valuation_score=
                            valuation[
                                "valuation_score"
                            ]

                    )
                    .summary()

                )

                rows.append({

                    "ticker":
                        ticker,

                    "business_score":
                        business[
                            "buffett_score"
                        ],

                    "valuation_score":
                        valuation[
                            "valuation_score"
                        ],

                    "decision_score":
                        decision[
                            "decision_score"
                        ],

                    "rating":
                        decision[
                            "decision_rating"
                        ]

                })

            except Exception:

                pass

        return (

            pd.DataFrame(
                rows
            )
            .sort_values(
                "decision_score",
                ascending=False
            )

        )
