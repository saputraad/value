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
                
                    result = self._series_score(
                        row.tolist()
                    )
    
                    break
    
            if row is None:
    
                return 0
    
            result = self._series_score(
                row.tolist()
            )
            
            self.revenue_debug = result
            
            return result["score"]
    
        except:
    
            return 0
    def revenue_stability(self):
        return 0
    
    def earnings_stability(self):
        return 0
    
    def fcf_stability(self):
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

                    row = income.loc[
                        candidate
                    ]
                
                    result = self._series_score(
                        row.tolist()
                    )
                    
                    self.earnings_debug = result
                    
                    return result["score"]
    
        except:
    
            return 0

    def summary(self):

        revenue_predictability = (
            self.revenue_predictability()
        )
        
        earnings_predictability = (
            self.earnings_predictability()
        )

        fcf_consistency = (
            self.fcf_consistency()
        )
        
        fcf_predictability = (
            self.fcf_predictability()
        )

        fcf_stability = (
            self.fcf_stability()
        )

        revenue_stability = (
            self.revenue_stability()
        )

        earnings_stability = (
            self.earnings_stability()
        )
    
        revenue = self.revenue_consistency()

        earnings = self.earnings_consistency()
    
        score = round(
            (
                revenue +
                earnings
            ) / 2,
            2
        )

        business_predictability = round(

            (
                revenue_predictability * 0.3
                +
                earnings_predictability * 0.4
                +
                fcf_predictability * 0.3
            ),
        
            2
        
        )
    
        return {

            "revenue_debug":
                getattr(
                    self,
                    "revenue_debug",
                    {}
                ),
        
            "earnings_debug":
                getattr(
                    self,
                    "earnings_debug",
                    {}
                ),

            "fcf_debug":
                getattr(
                    self,
                    "fcf_debug",
                    {}
                ),
            
            "fcf_consistency":
                fcf_consistency,
            
            "fcf_predictability":
                fcf_predictability,
            
            "revenue_consistency":
                revenue,
        
            "earnings_consistency":
                earnings,
        
            "revenue_predictability":
                revenue_predictability,
        
            "earnings_predictability":
                earnings_predictability,
            
            "business_predictability":
                business_predictability,
            
            "revenue_stability":
                revenue_stability,
            
            "earnings_stability":
                earnings_stability,
            
            "fcf_stability":
                fcf_stability,
        
            "consistency_score":
                score
        
        }

    def _predictability_score(self, values):

        values = [
    
            float(v)
    
            for v in values
    
            if v is not None
    
        ]
    
        if len(values) < 3:
    
            return 0
    
        values = values[::-1]
    
        declines = 0
    
        for i in range(1, len(values)):
    
            if values[i] < values[i - 1]:
    
                declines += 1
    
        score = max(
    
            0,
    
            100 - (declines * 30)
    
        )
    
        return score

    def revenue_predictability(self):

        try:
    
            income = self.data.get(
                "income_statement"
            )
    
            if income is None or income.empty:
    
                return 0
    
            for candidate in [
    
                "Total Revenue",
                "Revenue",
                "Operating Revenue"
    
            ]:
    
                if candidate in income.index:
    
                    return self._predictability_score(
    
                        income.loc[
                            candidate
                        ].tolist()
    
                    )
    
            return 0
    
        except:
    
            return 0

    def earnings_predictability(self):

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
    
                    return self._predictability_score(
    
                        income.loc[
                            candidate
                        ].tolist()
    
                    )
    
            return 0
    
        except:
    
            return 0

    def fcf_predictability(self):

        try:
    
            cashflow = self.data.get(
                "cashflow"
            )
    
            if cashflow is None or cashflow.empty:
    
                return 0
    
            for candidate in [
    
                "Free Cash Flow",
                "FreeCashFlow"
    
            ]:
    
                if candidate in cashflow.index:
    
                    return self._predictability_score(
    
                        cashflow.loc[
                            candidate
                        ].tolist()
    
                    )
    
            return 0
    
        except:
    
            return 0

    def fcf_consistency(self):
    
        try:
    
            cashflow = self.data.get(
                "cashflow"
            )
    
            if cashflow is None or cashflow.empty:
    
                return 0
    
            for candidate in [
    
                "Free Cash Flow",
                "FreeCashFlow"
    
            ]:
    
                if candidate in cashflow.index:
    
                    row = cashflow.loc[
                        candidate
                    ]
    
                    result = self._series_score(
                        row.tolist()
                    )
    
                    self.fcf_debug = result
    
                    return result[
                        "score"
                    ]
    
            return 0
    
        except:

            return 0

    def _max_drawdown_score(self, values):

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
    
        if len(values) < 2:
    
            return 0
    
        peak = max(values)
    
        trough = min(values)
    
        if peak <= 0:
    
            return 0
    
        drawdown = (
            peak - trough
        ) / peak
    
        score = max(
            0,
            100 - drawdown * 100
        )
    
        return round(
            score,
            2
        )
