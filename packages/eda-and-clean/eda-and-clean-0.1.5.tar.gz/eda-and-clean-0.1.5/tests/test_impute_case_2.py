from eda_and_clean.eda import eda_class
from eda_and_clean.clean import clean_class
from eda_and_clean.impute import impute_class
from .fixtures.case_2.input import input_2_fixture
from .fixtures.case_2.output_impute import (
    output_2_fill_na_in_id_col,
    output_2_groupby_bfill,
    output_2_groupby_expanding_mean_and_shift,
    output_2_groupby_ffill,
    output_2_groupby_rolling_mean_and_shift,
    output_2_use_summary_stat_of_groupby_to_fill_na_mean,
)
import pandas as pd
import numpy as np

# Clean the input data before imputing
df_test = input_2_fixture()
eda_instance_test_2 = eda_class(_df=df_test)
clean_instance_test_2 = clean_class()
df_test = clean_instance_test_2.fill_value_in_masked_entries(
    _df=df_test,
    dict_with_col_name_as_key_and_mask_as_value_to_make_na={
        "id": df_test["id"] == "na",
        "desc": df_test["desc"] == "",
    },
    fill_value=np.nan,
)
df_test = clean_instance_test_2.drop_rows(
    _df=df_test, row_mask_to_drop=df_test.index == 1
)

# Instantiate the impute class
impute_instance_test_2 = impute_class()

# Generate the output data
df_groupby_rolling_mean_and_shift = (
    impute_instance_test_2.groupby_rolling_mean_and_shift(
        _df=df_test,
        date_col="date",
        number_of_periods=2,
        groupby_cols=["id"],
        measure_col="value",
        min_pds=1,
    )
)
df_groupby_expanding_mean_and_shift = (
    impute_instance_test_2.groupby_expanding_mean_and_shift(
        _df=df_test,
        date_col="date",
        groupby_cols=["id"],
        measure_col="value",
        min_pds=1,
    )
)
df_groupby_bfill = impute_instance_test_2.groupby_fill(
    df=df_test,
    date_col="date",
    groupby_cols=["id"],
    measure_col="value",
    strategy="bfill",
)
df_groupby_ffill = impute_instance_test_2.groupby_fill(
    df=df_test,
    date_col="date",
    groupby_cols=["id"],
    measure_col="value",
    strategy="ffill",
)
df_fill_na_in_id_col = impute_instance_test_2.fill_na_in_id_col(
    _df=df_test, id_col="id"
)
df_use_summary_stat_of_groupby_to_fill_na_mean = (
    impute_instance_test_2.use_summary_stat_of_groupby_to_fill_na(
        _df=df_test.iloc[1:, :],
        groupby_cols=["id"],
        measure_col="value",
        summary_stat="mean",
    )
)


def test_groupby_rolling_mean_and_shift():
    pd.testing.assert_frame_equal(
        df_groupby_rolling_mean_and_shift,
        output_2_groupby_rolling_mean_and_shift(),
        check_dtype=False,
    )


def test_groupby_expanding_mean_and_shift():
    pd.testing.assert_frame_equal(
        df_groupby_expanding_mean_and_shift,
        output_2_groupby_expanding_mean_and_shift(),
        check_dtype=False,
    )


def test_groupby_bfill():
    pd.testing.assert_frame_equal(
        df_groupby_bfill, output_2_groupby_bfill(), check_dtype=False
    )


def test_groupby_ffill():
    pd.testing.assert_frame_equal(
        df_groupby_ffill, output_2_groupby_ffill(), check_dtype=False
    )


def test_use_summary_stat_of_groupby_to_fill_na_mean():
    pd.testing.assert_frame_equal(
        df_use_summary_stat_of_groupby_to_fill_na_mean,
        output_2_use_summary_stat_of_groupby_to_fill_na_mean(),
        check_dtype=False,
    )


def test_fill_na_in_id_col():
    # Since we are generating uid, it will always be different therefore mocking it
    mask = df_test["id"].isna()
    df_fill_na_in_id_col.loc[mask, "id"] = output_2_fill_na_in_id_col().loc[mask, "id"]
    pd.testing.assert_frame_equal(
        df_fill_na_in_id_col, output_2_fill_na_in_id_col(), check_dtype=False
    )
