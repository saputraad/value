import pandas as pd
import yfinance as yf
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

def fetch_ticker_info(
    ticker
):

    try:

        stock = yf.Ticker(
            ticker
        )

        info = stock.info

        return {

            "ticker":
                ticker,

            "name":
                info.get(
                    "longName"
                ),

            "sector":
                info.get(
                    "sector"
                ),

            "industry":
                info.get(
                    "industry"
                ),

            "market_cap":
                info.get(
                    "marketCap"
                ),

            "shares":
                info.get(
                    "sharesOutstanding"
                )
        }

    except:

        return None
        
 class IDXUniverseBuilder:

    def __init__(
        self,
        tickers
    ):

        self.tickers = tickers
        
        
    def build(self):

        results = []

        with ThreadPoolExecutor(
            max_workers=20
        ) as executor:

            futures = {

                executor.submit(
                    fetch_ticker_info,
                    ticker
                ): ticker

                for ticker
                in self.tickers
            }

            for future in as_completed(
                futures
            ):

                data = future.result()

                if data:

                    results.append(
                        data
                    )

        return pd.DataFrame(
            results
        )
        
            def save_csv(

        self,

        path="data/idx_universe.csv"
    ):

        df = self.build()

        df.to_csv(
            path,
            index=False
        )

        return df