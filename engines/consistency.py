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
    
            return {
    
                "score": 0,
    
                "growth_rates": [],
    
                "values": values
    
            }
    
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
    
            return {
    
                "score": 0,
    
                "growth_rates": growth,
    
                "values": values
    
            }
    
        volatility = np.std(
            growth
        )
    
        score = max(
            0,
            100 - volatility * 300
        )
    
        return {
    
            "score": round(
                min(score, 100),
                2
            ),
    
            "growth_rates":
                growth,
    
            "values":
                values
    
        }

    def revenue_consistency(self):

        try:
    
            income = self.data.get(
                "income_statement"
            )
    
            if income is None or income.empty:
    
                return 0
    
            row = None
    
            for candidate in [
    
                "Total Revenue",
                "Revenue",
                "Operating Revenue"
    
            ]:
    
                if candidate in income.index:
    
                    row = income.loc[
                        candidate
                    ]
    
                    break
    
            if row is None:
    
                return 0
    
            return self._series_score(
                row.tolist()
            )
    
        except:
    
            return 0

    def earnings_consistency(self):

        try:
    
            income = self.data.get(
                "income_statement"
            )
    
            if income is None or income.empty:
    
                return 0
    
            for candidate in [
    
                "Net Income",
                "NetIncome",
                "Net Income Common Stockholders"
    
            ]:
    
                if candidate in income.index:
    
                    return self._series_score(
    
                        income.loc[
                            candidate
                        ].tolist()
    
                    )
    
            return 0
    
        except:
    
            return 0

    def fcf_consistency(self):

        return 0

    def summary(self):

        revenue = self.revenue_consistency()
    
        earnings = self.earnings_consistency()
    
        score = round(
    
            (
                revenue +
                earnings
            ) / 2,
    
            2
    
        )
    
        return {
    
            "revenue_consistency":
                revenue,
    
            "earnings_consistency":
                earnings,
    
            "fcf_consistency":
                0,
    
            "consistency_score":
                score
    
        }
