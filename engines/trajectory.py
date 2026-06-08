from engines.terminal_quality import (
    TerminalQualityAnalyzer
)
def safe_get(df, names):

    if df is None or df.empty:
        return None

    for name in names:

        if name in df.index:
            return df.loc[name]

    return None


class TrajectoryAnalyzer:

    def __init__(
        self,
        ticker,
        data
    ):
    
        self.ticker = ticker
        self.data = data

    # ==========================
    # CAGR HELPER
    # ==========================

    def calculate_cagr(
        self,
        series
    ):
    
        values = (
            series
            .dropna()
            .astype(float)
            .values
        )
    
        if len(values) < 2:
            return None
    
        first = values[-1]
        last = values[0]
    
        years = len(values)-1
    
        if years <= 0:
            return None
    
        # turnaround case
        if first <= 0 or last <= 0:
    
            return (
                (
                    last-first
                )
                /
                abs(first)
            )
    
        return (
            (
                last/first
            )
            **
            (
                1/years
            )
        )-1

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

        revenue_growth = self.revenue_growth()
        earnings_growth = self.earnings_growth()
        cfo_growth = self.cfo_growth()
        
        return {
        
            "trajectory_debug": {
        
                "revenue_growth":
                    revenue_growth,
        
                "revenue_score":
                    self.growth_to_score(
                        revenue_growth
                    ),
        
                "earnings_growth":
                    earnings_growth,
        
                "earnings_score":
                    self.growth_to_score(
                        earnings_growth
                    ),
        
                "cfo_growth":
                    cfo_growth,
        
                "cfo_score":
                    self.growth_to_score(
                        cfo_growth
                    )
        
            },
        
            "trajectory_score":
                final_score,
        
            "trajectory_rating":
                rating
        
        }
    
        score = 0
        count = 0
    
        bank_tickers = [

            "BBCA",
            "BBRI",
            "BMRI",
            "BNGA",
            "BNII",
            "BBNI",
            "BDMN",
            "BBTN",
            "ARTO"
        
        ]
        
        if self.ticker in bank_tickers:
        
            metrics = [
                revenue,
                earnings
            ]
        
        else:
        
            metrics = [
                revenue,
                earnings,
                cfo
            ]
        for growth in metrics:
    
            if growth is None:
                continue
    
            count += 1
    
            score += self.growth_to_score(
                growth
            )
    
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

        base_score = self.score()
    
        final_score = round(
            self.score(),
            2
        )
    
        if final_score >= 80:
    
            rating = "IMPROVING"
    
        elif final_score >= 55:
    
            rating = "STABLE"
    
        elif final_score >= 30:
    
            rating = "SLOWING"
    
        else:
    
            rating = "DETERIORATING"
    
        return {
    
            "revenue_growth":
            self.revenue_growth(),
    
            "earnings_growth":
            self.earnings_growth(),
    
            "cfo_growth":
            self.cfo_growth(),
    
            "trajectory_score":
            final_score,
    
            "trajectory_rating":
            rating
    
        }

        return {

            "trajectory_debug": {
        
                "revenue_growth":
                    revenue_growth,
        
                "revenue_score":
                    self.growth_to_score(
                        revenue_growth
                    ),
        
                "earnings_growth":
                    earnings_growth,
        
                "earnings_score":
                    self.growth_to_score(
                        earnings_growth
                    ),
        
                "cfo_growth":
                    cfo_growth,
        
                "cfo_score":
                    self.growth_to_score(
                        cfo_growth
                    )
        
            },
        
            "revenue_growth":
                revenue_growth,
        
            "earnings_growth":
                earnings_growth,
        
            "cfo_growth":
                cfo_growth,
        
            "trajectory_score":
                final_score,
        
            "trajectory_rating":
                rating
        
        }

    def growth_to_score(self, growth):

        if growth is None:
            return None
    
        pct = growth * 100
    
        if pct >= 15:
            return 100
    
        if pct <= -20:
            return 0
    
        return round(
            ((pct + 20) / 35) * 100,
            2
        )
