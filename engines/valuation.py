import numpy as np

from core.data_provider import (
    get_company_info,
    get_current_price,
    get_balance_sheet
)


class ValuationAnalyzer:

    def __init__(self, ticker):

        self.ticker = ticker

        self.info = get_company_info(ticker)

        self.price = get_current_price(ticker)

        self.balance = get_balance_sheet(ticker)

    # ==========================================
    # BASIC METRICS
    # ==========================================

    def current_price(self):

        return self.price

    def eps(self):
        try:
            # Cara 1: Ambil dari info utama
            eps_val = self.info.get("trailingEps") or self.info.get("forwardEps")
            if eps_val is not None:
                return eps_val
                
            # Cara 2: Fallback hitung manual dari Net Income / Shares Outstanding
            from core.data_provider import get_income_statement, get_shares_outstanding
            financials = get_income_statement(self.ticker)
            shares = get_shares_outstanding(self.ticker)
            
            if not financials.empty and shares:
                # Mengambil Net Income dari baris teratas laporan keuangan terbaru
                net_income = financials.loc["Net Income"].iloc[0]
                return net_income / shares
            return None
        except:
            return None

    def book_value_per_share(self):
        try:
            # Cara 1: Ambil dari info utama
            bvps_val = self.info.get("bookValue")
            if bvps_val is not None:
                return bvps_val
                
            # Cara 2: Fallback hitung manual dari Total Equity / Shares Outstanding
            from core.data_provider import get_balance_sheet, get_shares_outstanding
            balance_sheet = get_balance_sheet(self.ticker)
            shares = get_shares_outstanding(self.ticker)
            
            if not balance_sheet.empty and shares:
                # Mencari total ekuitas pemegang saham
                equity_keys = ["Stockholders Equity", "Total Stockholders Equity"]
                for key in equity_keys:
                    if key in balance_sheet.index:
                        total_equity = balance_sheet.loc[key].iloc[0]
                        return total_equity / shares
            return None
        except:
            return None

    def pe_ratio(self):

        try:

            eps = self.eps()

            if eps is None or eps <= 0:
                return None

            return self.price / eps

        except:
            return None

    def pbv_ratio(self):

        try:

            bvps = self.book_value_per_share()

            if bvps is None or bvps <= 0:
                return None

            return self.price / bvps

        except:
            return None

    # ==========================================
    # EARNINGS YIELD
    # ==========================================

    def earnings_yield(self):

        try:

            pe = self.pe_ratio()

            if pe is None or pe <= 0:
                return None

            return 1 / pe

        except:
            return None

    # ==========================================
    # GRAHAM VALUE
    # ==========================================

    def graham_value(self):

        try:

            eps = self.eps()

            bvps = self.book_value_per_share()

            if eps is None:
                return None

            if bvps is None:
                return None

            if eps <= 0:
                return None

            if bvps <= 0:
                return None

            return np.sqrt(
                22.5 * eps * bvps
            )

        except:
            return None

    # ==========================================
    # MARGIN OF SAFETY
    # ==========================================

    def margin_of_safety(self):

        try:

            intrinsic = self.graham_value()

            if intrinsic is None:
                return None

            return (
                intrinsic - self.price
            ) / intrinsic

        except:
            return None

    # ==========================================
    # JUSTIFIED PBV
    # ==========================================

    def justified_pbv(self):

        """
        V1 simplified.

        PBV ≈ ROE / Required Return

        Example:

        ROE = 18%
        Required Return = 12%

        PBV = 1.5x
        """

        try:

            roe = self.info.get(
                "returnOnEquity",
                None
            )

            if roe is None:
                return None

            required_return = 0.12

            return roe / required_return

        except:
            return None

    # ==========================================
    # FAIR VALUE PBV
    # ==========================================

    def fair_value_pbv(self):

        try:

            bvps = self.book_value_per_share()

            justified_pbv = self.justified_pbv()

            if bvps is None:
                return None

            if justified_pbv is None:
                return None

            return bvps * justified_pbv

        except:
            return None

    # ==========================================
    # VALUE SCORE
    # ==========================================

    def value_score(self):

        score = []

        mos = self.margin_of_safety()

        if mos is not None:

            mos_pct = mos * 100

            if mos_pct >= 50:
                score.append(100)

            elif mos_pct >= 30:
                score.append(90)

            elif mos_pct >= 20:
                score.append(80)

            elif mos_pct >= 10:
                score.append(70)

            elif mos_pct >= 0:
                score.append(60)

            else:
                score.append(30)

        pe = self.pe_ratio()

        if pe is not None:

            if pe <= 8:
                score.append(100)

            elif pe <= 12:
                score.append(90)

            elif pe <= 18:
                score.append(75)

            elif pe <= 25:
                score.append(60)

            else:
                score.append(40)

        pbv = self.pbv_ratio()

        if pbv is not None:

            if pbv <= 1:
                score.append(100)

            elif pbv <= 1.5:
                score.append(90)

            elif pbv <= 2:
                score.append(75)

            elif pbv <= 3:
                score.append(60)

            else:
                score.append(40)

        if len(score) == 0:
            return None

        return round(
            np.mean(score),
            2
        )

    # ==========================================
    # SUMMARY
    # ==========================================

    def summary(self):

        return {

            "current_price":
                self.current_price(),

            "eps":
                self.eps(),

            "bvps":
                self.book_value_per_share(),

            "pe":
                self.pe_ratio(),

            "pbv":
                self.pbv_ratio(),

            "earnings_yield":
                self.earnings_yield(),

            "graham_value":
                self.graham_value(),

            "margin_of_safety":
                self.margin_of_safety(),

            "justified_pbv":
                self.justified_pbv(),

            "fair_value_pbv":
                self.fair_value_pbv(),

            "value_score":
                self.value_score()
        }
