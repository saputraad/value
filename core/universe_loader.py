import pandas as pd


class UniverseLoader:

    @staticmethod
    def load():

        df = pd.read_csv(
            "data/idx_universe.csv"
        )

        return (
            df["ticker"]
            .dropna()
            .tolist()
        )