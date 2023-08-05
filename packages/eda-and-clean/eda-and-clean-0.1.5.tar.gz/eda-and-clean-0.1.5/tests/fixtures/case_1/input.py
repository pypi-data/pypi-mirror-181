import pandas as pd
import numpy as np


def input_1_fixture():
    historical_df = [
        (1, "12-31-2019", "A", "this is A", 5, 1, 1),
        (1, "12-31-2019", "A", "this is A", 5, 1, 1),
        (2, "03-31-2020", "A", "this is A", 10, 2, 1),
        (3, "03-31-2020", "B", "this is B", 20, 4, 1),
        (4, "03-31-2020", "C", "this is C", 30, 6, 1),
        (5, "03-31-2020", "na", "", 40, 8, 1),
        (6, "06-30-2020", "A", "this is A", np.nan, np.nan, np.nan),
        (7, "06-30-2020", "E", "this is E", 17, 3, 1),
        (8, "06-30-2020", "B", "this is B", 20, 4, 1),
        (9, "09-30-2020", "A", "this is A", 10, 2, 1),
        (10, "09-30-2020", "F", "this is F", 20, 4, 1),
        (11, "09-30-2020", "B", "this is B", 20000000, np.nan, np.nan),
        (12, "09-30-2020", "C", "this is C", 30, 6, 1),
        (13, "12-31-2020", "A", "this is A", 10, 2, 1),
        (14, "12-31-2020", "B", "this is B", 20, 4, 1),
        (15, "12-31-2020", "C", "this is C", 30, 6, 1),
        (16, "12-31-2020", "G", "this is G", 100, 10, 1),
    ]

    df = pd.DataFrame(
        data=[
            {
                "uid": uid,
                "date": date,
                "id": id,
                "desc": desc,
                "value": value,
                "volume": volume,
                "random": random,
            }
            for uid, date, id, desc, value, volume, random in historical_df
        ]
    )

    # set data type
    cols = df.columns.tolist()
    dtypes = ["int", "datetime64[ns]", "str", "str", "float", "int", "int"]
    for col, dtype in zip(cols, dtypes):
        df[col] = df[col].astype(dtype, errors="ignore")

    return df
