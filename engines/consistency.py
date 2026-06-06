import numpy as np


class ConsistencyAnalyzer:

    def __init__(self, data):

        self.data = data

    def _series_score(self, values):
  
      values = [
          float(v)
          for v in values
          if v is not None
      ]
  
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

        try:
    
            income = self.data[
                "income_statement"
            ]
    
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
    
            income = self.data[
                "income_statement"
            ]
    
            for candidate in [
    
                "Net Income",
                "NetIncome"
    
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

      def earnings_consistency(self):

        try:
    
            income = self.data[
                "income_statement"
            ]
    
            for candidate in [
    
                "Net Income",
                "NetIncome"
    
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

        try:
    
            cashflow = self.data[
                "cashflow"
            ]
    
            for candidate in [
    
                "Free Cash Flow",
                "FreeCashFlow"
    
            ]:
    
                if candidate in cashflow.index:
    
                    return self._series_score(
    
                        cashflow.loc[
                            candidate
                        ].tolist()
    
                    )
    
            return 0
    
        except:
    
            return 0

    def summary(self):

        revenue = self.revenue_consistency()
    
        earnings = self.earnings_consistency()
    
        fcf = self.fcf_consistency()
    
        score = round(
    
            (
                revenue
                +
                earnings
                +
                fcf
            )
            / 3,
    
            2
    
        )
    
        return {
    
            "revenue_consistency":
                revenue,
    
            "earnings_consistency":
                earnings,
    
            "fcf_consistency":
                fcf,
    
            "consistency_score":                                    
            score

    }
