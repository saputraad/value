import pandas as pd
from core.financial_mapper import FINANCIAL_FIELDS


def get_metric(df, metric):

    try:

        aliases = FINANCIAL_FIELDS[metric]

        for alias in aliases:

            if alias in df.index:
                return df.loc[alias]

        return None

    except:

        return None


def safe_value(series, index=0):

    try:

        return float(series.iloc[index])

    except:
        return None
        
def find_row(df, possible_names):

    try:

        for name in possible_names:

            if name in df.index:

                return df.loc[name]

        return None

    except:

        return None