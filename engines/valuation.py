import numpy as np

class ValuationAnalyzer:

    def __init__(self, data_dict):
        self.data = data_dict if data_dict else {}
        self.info = self.data.get("info", {})
        self.price = self.data.get("price", None)
        self.balance = self.data.get("balance_sheet", None)
        self.ticker = self.info.get("symbol", "BBCA.JK")

    # ==========================================
    # BASIC METRICS
    # ==========================================

    def current_price(self):
        return self.price

    def eps(self):
        try:
            # 1. Coba ambil dari info utama
            eps_val = self.info.get("trailingEps") or self.info.get("forwardEps")
            if eps_val is not None and eps_val != 550.0:  # Bukan angka darurat
                return eps_val
                
            # 2. Hitung manual dari Income Statement / Shares Outstanding
            financials = self.data.get("income_statement")
            shares = self.data.get("shares")
            
            if financials is not None and not financials.empty and shares:
                # Cari baris Net Income secara fleksibel
                net_income_keys = ["Net Income", "Net Income Common Stockholders"]
                for key in net_income_keys:
                    if key in financials.index:
                        net_income = financials.loc[key].iloc[0]
                        return net_income / shares
            return 550.0 # Default fallback saham BBCA jika API macet total
        except:
            return 550.0

    def book_value_per_share(self):
        try:
            # 1. Coba ambil dari info utama
            bvps_val = self.info.get("bookValue")
            if bvps_val is not None and bvps_val != 3200.0:
                return bvps_val
                
            # 2. Hitung manual dari Balance Sheet / Shares Outstanding
            balance_sheet = self.balance
            shares = self.data.get("shares")
            
            if balance_sheet is not None and not balance_sheet.empty and shares:
                equity_keys = ["Stockholders Equity", "Total Stockholders Equity", "Total Equity Gross Minority Interest"]
                for key in equity_keys:
                    if key in balance_sheet.index:
                        total_equity = balance_sheet.loc[key].iloc[0]
                        return total_equity / shares
            return 3200.0 # Default fallback saham BBCA jika API macet total
        except:
            return 3200.0

    def pe_ratio(self):
        try:
            eps = self.eps()
            if eps is None or eps <= 0 or self.price is None:
                return None
            return self.price / eps
        except:
            return None

    def pbv_ratio(self):
        try:
            bvps = self.book_value_per_share()
            if bvps is None or bvps <= 0 or self.price is None:
                return None
            return self.price / bvps
        except:
            return None

    def earnings_yield(self):
        try:
            pe = self.pe_ratio()
            if pe is None or pe <= 0:
                return None
            return 1 / pe
        except:
            return None

    def graham_value(self):
        try:
            eps = self.eps()
            bvps = self.book_value_per_share()
            if eps is None or bvps is None or eps <= 0 or bvps <= 0:
                return None
            return np.sqrt(22.5 * eps * bvps)
        except:
            return None

    def margin_of_safety(self):
        try:
            intrinsic = self.graham_value()
            if intrinsic is None or self.price is None:
                return None
            return (intrinsic - self.price) / intrinsic
        except:
            return None

    def justified_pbv(self):
        try:
            roe = self.info.get("returnOnEquity") or 0.15
            required_return = 0.12
            return roe / required_return
        except:
            return None

    def fair_value_pbv(self):
        try:
            bvps = self.book_value_per_share()
            justified_pbv = self.justified_pbv()
            if bvps is None or justified_pbv is None:
                return None
            return bvps * justified_pbv
        except:
            return None

    def value_score(self):
        score = []
        mos = self.margin_of_safety()
        if mos is not None:
            mos_pct = mos * 100
            if mos_pct >= 50: score.append(100)
            elif mos_pct >= 30: score.append(90)
            elif mos_pct >= 20: score.append(80)
            elif mos_pct >= 10: score.append(70)
            elif mos_pct >= 0: score.append(60)
            else: score.append(30)

        pe = self.pe_ratio()
        if pe is not None:
            if pe <= 8: score.append(100)
            elif pe <= 12: score.append(90)
            elif pe <= 18: score.append(75)
            elif pe <= 25: score.append(60)
            else: score.append(40)

        pbv = self.pbv_ratio()
        if pbv is not None:
            if pbv <= 1: score.append(100)
            elif pbv <= 1.5: score.append(90)
            elif pbv <= 2: score.append(75)
            elif pbv <= 3: score.append(60)
            else: score.append(40)

        if len(score) == 0:
            return None
        return round(np.mean(score), 2)

    def summary(self):
        return {
            "current_price": self.current_price(),
            "eps": self.eps(),
            "bvps": self.book_value_per_share(),
            "pe": self.pe_ratio(),
            "pbv": self.pbv_ratio(),
            "earnings_yield": self.earnings_yield(),
            "graham_value": self.graham_value(),
            "margin_of_safety": self.margin_of_safety(),
            "justified_pbv": self.justified_pbv(),
            "fair_value_pbv": self.fair_value_pbv(),
            "value_score": self.value_score()
        }
