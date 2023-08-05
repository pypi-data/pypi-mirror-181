from uuid import uuid4
import pandas as pd


def fill_na_formater_and_checker(func):
    """
    Decorator for fill na functions
    """

    def inner(*args, **kwargs):
        fill_na_dict = func(*args, **kwargs)

        # Unpack arg
        df = fill_na_dict["df_original"]
        df_transformed = fill_na_dict["df_transformed"]
        groupby_cols = fill_na_dict["groupby_cols"]
        measure_col = fill_na_dict["measure_col"]

        # Structure output
        impute_instance = impute_class()
        df_output = impute_instance.merge_with_original_df_and_fill_na(
            _df_original=df,
            _df_transformed=df_transformed,
            groupby_cols=groupby_cols,
            measure_col=measure_col,
        )
        df_output = impute_instance.drop_original_measure_col_and_use_na_filled(
            _df=df_output, measure_col=measure_col
        )

        # Ensure output is of the right size
        if df_output.shape != df.shape:
            raise Exception("Output df is not of the right size")

        # Check if there are any more NA in measure_col
        if df_output[measure_col].isna().sum() > 0:
            print(
                f"There are still NA in {measure_col} - This will happen in cases where there are no non-na entry within a groupby object"
            )

        return df_output

    return inner


class impute_class:
    """
    1. groupby_rolling_mean_and_shift
    2. groupby_expanding_mean_and_shift
    3. groupby_fill
    4. use_summary_stat_of_groupby_to_fill_na
    5. fill_na_in_id_col
    """

    def __init__(self) -> None:
        pass

    def groupby_fill(
        self,
        df: pd.DataFrame,
        date_col: str,
        groupby_cols: list,
        measure_col: str,
        strategy: str = "bfill",
    ):
        df = df.copy()
        if strategy == "bfill":
            shift_pd = -1
        elif strategy == "ffill":
            shift_pd = 1
        else:
            raise ValueError("strategy must be either bfill or ffill")

        # Find the number of na values within each group
        mask = df[measure_col].isna()
        df_na_count_within_groupby = (
            df[mask].groupby(groupby_cols)[measure_col].size().reset_index()
        )
        df_na_count_within_groupby = df_na_count_within_groupby.rename(
            columns={measure_col: "na_count"}
        )
        max_na_count = int(df_na_count_within_groupby["na_count"].max())

        # rolling mean with 1 window
        for _ in range(max_na_count):
            df = self.groupby_rolling_mean_and_shift(
                _df=df,
                date_col=date_col,
                groupby_cols=groupby_cols,
                number_of_periods=1,
                measure_col=measure_col,
                min_pds=1,
                shift_pds=shift_pd,
            )
        return df

    def groupby_expanding_mean_and_shift(
        self,
        _df: pd.DataFrame,
        date_col: str,
        groupby_cols: list,
        measure_col: str,
        min_pds: int = 1,
    ):
        df = _df.copy()

        # Find number of periods - this is the window size
        number_of_periods = df[date_col].nunique() + 1

        return self.groupby_rolling_mean_and_shift(
            _df=df,
            date_col=date_col,
            groupby_cols=groupby_cols,
            number_of_periods=number_of_periods,
            measure_col=measure_col,
            min_pds=min_pds,
        )

    def check_if_groupby_results_in_single_value(self, _df_grouper) -> None:
        df_check = (
            _df_grouper.size()
            .reset_index()
            .rename(columns={0: "number_of_entries_per_groupby"})
        )
        max_count = df_check["number_of_entries_per_groupby"].max()
        if max_count > 1:
            raise Exception(
                "Warning: There are multiple entries per groupby. Check for duplicates or consider aggregating the data"
            )
        return None

    @fill_na_formater_and_checker
    def groupby_rolling_mean_and_shift(
        self,
        _df: pd.DataFrame,
        date_col: str,
        groupby_cols: list,
        number_of_periods: int,
        measure_col: str,
        min_pds: int = 1,
        shift_pds: int = 1,
    ):
        df = _df.copy()
        measure_col_transform_interim = measure_col + "_" + "rolling_mean"
        measure_col_transform_final = "transformed"

        # Make sure the data is in shape to perform the operation
        df_grouper_checker = df.groupby(groupby_cols + [date_col])
        self.check_if_groupby_results_in_single_value(_df_grouper=df_grouper_checker)

        # Rolling mean and shift
        df_grouper = df.set_index([date_col]).groupby(groupby_cols)
        df_rolling_mean = (
            df_grouper.rolling(window=number_of_periods, min_periods=min_pds)[
                measure_col
            ]
            .mean()
            .reset_index()
        )
        df_rolling_mean = df_rolling_mean.rename(
            columns={measure_col: measure_col_transform_interim}
        )
        df_rolling_mean[measure_col_transform_final] = df_rolling_mean.groupby(
            groupby_cols
        )[measure_col_transform_interim].shift(periods=shift_pds)

        # Structure dict and return dict
        fill_na_dict = {}
        fill_na_dict["df_original"] = df
        fill_na_dict["df_transformed"] = df_rolling_mean
        fill_na_dict["groupby_cols"] = groupby_cols + [date_col]
        fill_na_dict["measure_col"] = measure_col
        return fill_na_dict

    def merge_with_original_df_and_fill_na(
        self,
        _df_original: pd.DataFrame,
        _df_transformed: pd.DataFrame,
        groupby_cols: list,
        measure_col: str,
    ):
        df = _df_original.copy()
        df_transformed = _df_transformed.copy()
        measure_col_transform_final = "transformed"
        measure_col_na_filled = measure_col + "_na_filled"

        # Merge with original df
        df = df.merge(
            df_transformed[groupby_cols + [measure_col_transform_final]],
            on=groupby_cols,
            how="left",
        )
        df[measure_col_na_filled] = df[measure_col]

        # Fill na with rolling mean shifted value
        mask = df[measure_col].isna()
        df.loc[mask, measure_col_na_filled] = df.loc[mask, measure_col_transform_final]

        return df

    def drop_original_measure_col_and_use_na_filled(
        self, _df: pd.DataFrame, measure_col: str
    ):
        df = _df.copy()
        measure_col_na_filled = measure_col + "_na_filled"
        measure_col_transform_final = "transformed"

        df = df.drop(columns=[measure_col, measure_col_transform_final])
        df = df.rename(columns={measure_col_na_filled: measure_col})
        return df

    @fill_na_formater_and_checker
    def use_summary_stat_of_groupby_to_fill_na(
        self,
        _df: pd.DataFrame,
        groupby_cols: list,
        measure_col: str,
        summary_stat: str = "mean",
    ):
        df = _df.copy()

        # Perform groupby operation
        df_grouper = df.groupby(groupby_cols)

        # calculate summary stat
        # Note: Skip NA is True by default
        measure_col_transform_final = "transformed"
        df_summary = df_grouper[measure_col].agg(summary_stat).reset_index()
        df_summary = df_summary.rename(
            columns={measure_col: measure_col_transform_final}
        )

        # Structure dict and return dict
        fill_na_dict = {}
        fill_na_dict["df_original"] = df
        fill_na_dict["df_transformed"] = df_summary
        fill_na_dict["groupby_cols"] = groupby_cols
        fill_na_dict["measure_col"] = measure_col

        return fill_na_dict

    def fill_na_in_id_col(self, _df: pd.DataFrame, id_col: str):
        df = _df.copy()
        uuid_col = "uuid"

        # Generate a uid column
        df[uuid_col] = df.index.map(lambda _: uuid4().hex)

        # Fill na in id_col with values in uuid_col
        mask = df[id_col].isna()
        df.loc[mask, id_col] = df.loc[mask, uuid_col]

        # Make sure the filled values are unique and are not already a part of id_col
        uid_entered_values = list(df.loc[mask, id_col].values)
        if len(uid_entered_values) != len(set(uid_entered_values)):
            raise Exception(
                "Warning: There are duplicate values in the uid_entered_values"
            )
        unique_id_values = list(df.loc[~mask, id_col].unique().tolist())
        common_ids = list(set(unique_id_values).intersection(set(uid_entered_values)))
        if len(common_ids) > 0:
            raise Exception(
                f"Warning: There are common values between uid entered values and {id_col}"
            )

        # Drop uid column before returning df
        df = df.drop(columns=[uuid_col])

        return df
