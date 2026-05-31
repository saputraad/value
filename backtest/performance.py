import numpy as np


class PerformanceMetrics:

    @staticmethod
    def cagr(

        start_value,

        end_value,

        years
    ):

        return (

            (
                end_value /
                start_value
            )
            **
            (
                1 / years
            )

            - 1

        ) * 100
        
    @staticmethod
    def max_drawdown(
        equity_curve
    ):

        peak = equity_curve[0]

        max_dd = 0

        for value in equity_curve:

            peak = max(
                peak,
                value
            )

            dd = (

                peak - value

            ) / peak

            max_dd = max(
                max_dd,
                dd
            )

        return max_dd * 100
        
    @staticmethod
    def win_rate(
        trades
    ):

        wins = len(

            [
                x
                for x in trades

                if x > 0
            ]

        )

        return (

            wins /

            len(trades)

        ) * 100