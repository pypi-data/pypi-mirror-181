from eda_and_clean.eda import eda_class
from .fixtures.case_1.input import input_1_fixture
from .fixtures.case_1.output_eda import (
    output_1_dtypes_fixture,
    output_1_missing_values_fixture,
    output_1_downcasting_fixture,
    output_1_duplicates_fixture,
    output_1_data_analysis_fixture,
    output_1_summary_fixture,
    output_1_df_cdf,
)
from .utils import assert_dict, assert_dataframe

df = input_1_fixture()
eda_instance_1 = eda_class(_df=df)


def test_cdf():
    df_cdf_actual = eda_instance_1.calculate_empirical_cdf(_df=df, col="value")
    df_cdf_expected = output_1_df_cdf()
    assert_dataframe(actual=df_cdf_actual, expected=df_cdf_expected)


def test_summary():
    output, not_tested_keys = output_1_summary_fixture()
    assert_dict(
        actual=eda_instance_1.SUMMARY, expected=output, not_tested_keys=not_tested_keys
    )


def test_dtypes():
    output, not_tested_keys = output_1_dtypes_fixture()
    assert_dict(
        actual=eda_instance_1.DTYPES, expected=output, not_tested_keys=not_tested_keys
    )


def test_downcasting():
    output, not_tested_keys = output_1_downcasting_fixture()
    assert_dict(
        actual=eda_instance_1.DOWNCASTING,
        expected=output,
        not_tested_keys=not_tested_keys,
    )


def test_duplicates():
    output, not_tested_keys = output_1_duplicates_fixture()
    assert_dict(
        actual=eda_instance_1.DUPLICATES,
        expected=output,
        not_tested_keys=not_tested_keys,
    )


def test_missing_values():
    output, not_tested_keys = output_1_missing_values_fixture()
    assert_dict(
        actual=eda_instance_1.MISSING_VALUES,
        expected=output,
        not_tested_keys=not_tested_keys,
    )


def test_data_analysis():
    output, not_tested_keys = output_1_data_analysis_fixture()
    assert_dict(
        actual=eda_instance_1.DATA_ANALYSIS,
        expected=output,
        not_tested_keys=not_tested_keys,
    )
