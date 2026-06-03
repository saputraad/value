def safe_get(df, names):

    if df is None or df.empty:
        return None

    for name in names:

        if name in df.index:
            return df.loc[name]

    return None


class TrajectoryAnalyzer:

    def __init__(self, data):

        self.data = data

    # ==========================
    # CAGR HELPER
    # ==========================

    def calculate_cagr(self, series):

        try:

            values = list(
                reversed(
                    series.dropna()
                    .astype(float)
                    .values
                )
            )

            if len(values) < 3:
                return None

            first = values[0]
            last = values[-1]

            if first <= 0:
                return None

            years = len(values) - 1

            return (
                (last / first)
                **
                (1 / years)
                - 1
            )

        except:

            return None

    # ==========================
    # REVENUE CAGR
    # ==========================

    def revenue_growth(self):

        income = self.data[
            "income_statement"
        ]

        revenue = safe_get(
            income,
            [
                "Total Revenue",
                "Revenue"
            ]
        )

        if revenue is None:
            return None

        return self.calculate_cagr(
            revenue
        )

    # ==========================
    # NET INCOME CAGR
    # ==========================

    def earnings_growth(self):

        income = self.data[
            "income_statement"
        ]

        earnings = safe_get(
            income,
            [
                "Net Income",
                "Net Income Common Stockholders"
            ]
        )

        if earnings is None:
            return None

        return self.calculate_cagr(
            earnings
        )

    # ==========================
    # CFO CAGR
    # ==========================

    def cfo_growth(self):

        cashflow = self.data[
            "cashflow"
        ]
    
        cfo = safe_get(
            cashflow,
            [
                "Operating Cash Flow",
                "Cash Flow From Continuing Operating Activities",
                "Net Cash Provided By Operating Activities",
                "Cash Flowsfromusedin Operating Activities Direct"
            ]
        )
        
        if cfo is None or cfo.dropna().empty:
        
            fcf = safe_get(
                cashflow,
                [
                    "Free Cash Flow"
                ]
            )
        
            capex = safe_get(
                cashflow,
                [
                    "Capital Expenditure"
                ]
            )
            import streamlit as st

            st.subheader("KRAS DEBUG")
            
            st.write("FCF")
            st.write(fcf)
            
            st.write("CAPEX")
            st.write(capex)
            st.write("FCF", fcf)
            st.write("CAPEX", capex)
        
            if fcf is not None and capex is not None:
        
                cfo = fcf - capex
        
            else:
        
                return None
        
        return self.calculate_cagr(
            cfo
        )

    # ==========================
    # SCORE
    # ==========================

    def score(self):

        revenue = self.revenue_growth()
        earnings = self.earnings_growth()
        cfo = self.cfo_growth()
    
        # =====================
        # RED FLAG
        # =====================
    
        if revenue is not None:
    
            if revenue < -0.10:
    
                return 20
    
        score = 0
        count = 0
    
        metrics = [
            revenue,
            earnings,
            cfo
        ]
    
        for growth in metrics:
    
            if growth is None:
                continue
    
            count += 1
    
            pct = growth * 100
    
            if pct >= 15:
                score += 100
            
            elif pct >= 10:
                score += 90
            
            elif pct >= 5:
                score += 80
            
            elif pct >= 0:
                score += 60
            
            elif pct >= -5:
                score += 40
            
            else:
                score += 20
    
        if count == 0:
            return 0
    
        return round(
            score / count,
            2
        )

    # ==========================
    # RATING
    # ==========================

    def rating(self):

        score = self.score()

        if score >= 80:
            return "IMPROVING"
        
        elif score >= 55:
            return "STABLE"
        
        elif score >= 30:
            return "SLOWING"
        
        return "DETERIORATING"

    # ==========================
    # SUMMARY
    # ==========================

    def summary(self):

        return {

            "revenue_growth":
                self.revenue_growth(),

            "earnings_growth":
                self.earnings_growth(),

            "cfo_growth":
                self.cfo_growth(),

            "trajectory_score":
                self.score(),

            "trajectory_rating":
                self.rating()
        }
