import pandas as pd

def column_equal(
        df :pd.DataFrame,
        column_name: str,
        value
) -> pd.DataFrame:
    if column_name in df.columns:
        return df.loc[df[column_name] == value]
    else:
        return pd.DataFrame(columns=df.columns)