from core.data_provider import (
    get_company_info
)


class SectorClassifier:

    def __init__(self, ticker):

        self.ticker = ticker

        self.info = get_company_info(ticker)

    # ==================================
    # RAW SECTOR
    # ==================================

    def raw_sector(self):

        try:

            return (
                self.info.get(
                    "sector",
                    ""
                )
                .upper()
            )

        except:

            return ""

    # ==================================
    # RAW INDUSTRY
    # ==================================

    def raw_industry(self):

        try:

            return (
                self.info.get(
                    "industry",
                    ""
                )
                .upper()
            )

        except:

            return ""

    # ==================================
    # NORMALIZED SECTOR
    # ==================================

    def classify(self):

        sector = self.raw_sector()

        industry = self.raw_industry()

        text = f"{sector} {industry}"

        # -----------------------------
        # BANK
        # -----------------------------

        if any(
            x in text
            for x in [
                "BANK",
                "BANKS",
                "REGIONAL BANK"
            ]
        ):
            return "BANK"

        # -----------------------------
        # INSURANCE
        # -----------------------------

        if any(
            x in text
            for x in [
                "INSURANCE"
            ]
        ):
            return "INSURANCE"

        # -----------------------------
        # COAL
        # -----------------------------

        if any(
            x in text
            for x in [
                "COAL",
                "THERMAL COAL"
            ]
        ):
            return "COAL"

        # -----------------------------
        # MINING
        # -----------------------------

        if any(
            x in text
            for x in [
                "MINING",
                "METALS",
                "NICKEL",
                "COPPER",
                "GOLD"
            ]
        ):
            return "MINING"

        # -----------------------------
        # OIL & GAS
        # -----------------------------

        if any(
            x in text
            for x in [
                "OIL",
                "GAS",
                "ENERGY"
            ]
        ):
            return "ENERGY"

        # -----------------------------
        # PROPERTY
        # -----------------------------

        if any(
            x in text
            for x in [
                "REAL ESTATE",
                "PROPERTY"
            ]
        ):
            return "PROPERTY"

        # -----------------------------
        # CONSUMER
        # -----------------------------

        if any(
            x in text
            for x in [
                "FOOD",
                "BEVERAGE",
                "CONSUMER",
                "HOUSEHOLD"
            ]
        ):
            return "CONSUMER"

        # -----------------------------
        # TELECOM
        # -----------------------------

        if any(
            x in text
            for x in [
                "TELECOM",
                "COMMUNICATION"
            ]
        ):
            return "TELECOM"

        # -----------------------------
        # HEALTHCARE
        # -----------------------------

        if any(
            x in text
            for x in [
                "HEALTH",
                "PHARMACEUTICAL",
                "HOSPITAL"
            ]
        ):
            return "HEALTHCARE"

        # -----------------------------
        # TECHNOLOGY
        # -----------------------------

        if any(
            x in text
            for x in [
                "SOFTWARE",
                "TECHNOLOGY",
                "INTERNET"
            ]
        ):
            return "TECHNOLOGY"

        return "GENERAL"

    # ==================================
    # SUMMARY
    # ==================================

    def summary(self):

        return {

            "sector":
                self.raw_sector(),

            "industry":
                self.raw_industry(),

            "classification":
                self.classify()
        }