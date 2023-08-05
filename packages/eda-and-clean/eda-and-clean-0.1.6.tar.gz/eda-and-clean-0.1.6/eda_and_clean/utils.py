import pandas as pd
import numpy as np


def generate_outlier_mask_based_on_iqr(df, col_name, iqr_multiplier=1.5):
    """
    Generates a mask for a given column in a dataframe based on the interquartile range.
    :param df: Pandas dataframe
    :param col_name: Column name
    :param iqr_multiplier: Multiplier for the interquartile range
    :return: Mask
    """
    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)
    iqr = q3 - q1
    outlier_mask = (df[col_name] < (q1 - iqr_multiplier * iqr)) & (
        df[col_name] > (q3 + iqr_multiplier * iqr)
    )
    return outlier_mask


def generate_outlier_mask_based_on_z_score(df, col_name, z_score_threshold=3):
    """
    Generates a mask for a given column in a dataframe based on the z-score.
    :param df: Pandas dataframe
    :param col_name: Column name
    :param z_score_threshold: Z-score threshold
    :return: Mask
    """
    z_score = (df[col_name] - df[col_name].mean()) / df[col_name].std()
    outlier_mask = (z_score > z_score_threshold) | (z_score < -z_score_threshold)
    return outlier_mask


def filter_non_capitalized_words_from_list(_list: list) -> list:
    return [word for word in _list if word.isupper()]


def print_dataframe_as_dataframe_definition(df: pd.DataFrame) -> None:
    """
    Prints a dataframe as a dataframe definition.
    :param df: Pandas dataframe
    :param df_name: Name of the dataframe
    :return: None
    """
    df_text = f"pd.DataFrame({df.to_dict()})"
    # replace "TimeStamp" with "pd.to_datetime"
    df_text = df_text.replace("Timestamp", "pd.to_datetime")
    # replace "nan" with "np.nan"
    df_text = df_text.replace("nan", "np.nan")
    return df_text


def structure_concated_dataframe(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Structures a dataframe that has been concated.
    :param df: Pandas dataframe
    :return: Pandas dataframe
    """
    df = _df.copy()
    df = df.reset_index(drop=True)
    for col in ["level_0", "index"]:
        if col in df.columns:
            df = df.drop(columns=col)
    return df


def make_diagonals_na(_df: pd.DataFrame) -> pd.DataFrame:
    df = _df.copy()
    # fluctuating diagonals
    df.values[[np.arange(df.shape[0])] * 2] = np.nan
    return df


def check_df_equal(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:

    # Make sure both are of the same shape
    if df_1.shape != df_2.shape:
        print("There is a difference in the shape of the dataframes")
        return False

    col_order = df_1.columns.tolist()
    df_2 = df_2[col_order]

    index_order = df_1.index.tolist()
    df_2 = df_2.reindex(index_order)

    return df_1.equals(df_2)
