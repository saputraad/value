import numpy as np


class ConsistencyAnalyzer:

    def __init__(self, data):

        self.data = data

    def _series_score(self, values):

        clean_values = []

        for v in values:

            try:

                if v is not None and not np.isnan(v):

                    clean_values.append(
                        float(v)
                    )

            except:

                pass

        values = clean_values

        if len(values) < 3:

            return 0

        values = values[::-1]

        growth = []

        for i in range(1, len(values)):

            prev = values[i - 1]

            curr = values[i]

            if prev == 0:

                continue

            growth.append(
                (curr - prev) / abs(prev)
            )

        if len(growth) < 2:

            return 0

        volatility = np.std(
            growth
        )

        score = max(
            0,
            100 - volatility * 300
        )

        return round(
            min(score, 100),
            2
        )

    def revenue_consistency(self):

        return 0

    def earnings_consistency(self):

        return 0

    def fcf_consistency(self):

        return 0

    def summary(self):

        return {

            "revenue_consistency": 0,

            "earnings_consistency": 0,

            "fcf_consistency": 0,

            "consistency_score": 0

        }
