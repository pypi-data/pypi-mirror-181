from eda_and_clean.eda import eda_class
from eda_and_clean.clean import clean_class
from .fixtures.case_1.input import input_1_fixture
from .fixtures.case_1.output_clean import (
    output_1_clean_str_columns,
    output_1_convert_dtype,
    output_1_drop_columns,
    output_1_drop_duplicate_rows,
    output_1_drop_rows,
    output_1_fill_value_in_masked_entries,
    output_1_remove_existing_index_and_make_new_one,
)
import pandas as pd
import numpy as np

df = input_1_fixture()
eda_instance_test_1 = eda_class(_df=df)
clean_instance_test_1 = clean_class()
input = input_1_fixture()

dict_to_convert = {}
dict_to_convert["float32"] = eda_instance_test_1.DOWNCASTING["to_float32"]

df_test_1 = input.pipe(clean_instance_test_1.remove_existing_index_and_make_new_one)
df_test_2 = df_test_1.pipe(clean_instance_test_1.drop_duplicate_rows)
df_test_3 = df_test_2.pipe(clean_instance_test_1.drop_columns, cols_to_drop=["random"])
df_test_4 = df_test_3.pipe(
    clean_instance_test_1.convert_dtype, dict_with_cols_to_convert=dict_to_convert
)
df_test_5 = df_test_4.pipe(
    clean_instance_test_1.clean_str_columns,
    str_cols_to_clean=["desc"],
    operations_to_perform=[
        "make_str_col_lowercase",
        "tokenize_remove_stop_words_and_stem",
        "remove_punctuation",
        "remove_non_alphabets",
    ],
    list_of_stopwords_to_remove=["a"],
)
df_test_6 = clean_instance_test_1.fill_value_in_masked_entries(
    _df=df_test_5,
    dict_with_col_name_as_key_and_mask_as_value_to_make_na={
        "id": df_test_5["id"] == "na",
        "desc": df_test_5["desc"] == "",
    },
    fill_value=np.nan,
)
df_test_7 = clean_instance_test_1.drop_rows(
    _df=df_test_6, row_mask_to_drop=df_test_6["value"].isna()
)


def test_remove_existing_index_and_make_new_one():
    pd.testing.assert_frame_equal(
        df_test_1, output_1_remove_existing_index_and_make_new_one(), check_dtype=False
    )


def test_drop_duplicate_rows():
    pd.testing.assert_frame_equal(
        df_test_2, output_1_drop_duplicate_rows(), check_dtype=False
    )


def test_drop_columns():
    pd.testing.assert_frame_equal(df_test_3, output_1_drop_columns(), check_dtype=False)


def test_convert_dtype():
    pd.testing.assert_frame_equal(
        df_test_4, output_1_convert_dtype(), check_dtype=False
    )


def test_clean_str_columns():
    pd.testing.assert_frame_equal(
        df_test_5, output_1_clean_str_columns(), check_dtype=False
    )


def test_fill_value_in_masked_entries():
    pd.testing.assert_frame_equal(
        df_test_6, output_1_fill_value_in_masked_entries(), check_dtype=False
    )


def test_drop_rows():
    pd.testing.assert_frame_equal(df_test_7, output_1_drop_rows(), check_dtype=False)
