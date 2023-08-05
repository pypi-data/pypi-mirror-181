import warnings
import pandas as pd


def assert_dict(actual: dict, expected: dict, not_tested_keys: list = []):
    for key, value in actual.items():
        if key not in not_tested_keys:
            if isinstance(value, list):
                assert expected[key] == value
            elif isinstance(value, pd.DataFrame):
                assert_dataframe(actual=value, expected=expected[key])
            elif isinstance(value, dict):
                assert value == expected[key]
            else:
                warnings.warn(
                    "test coverage not implemented for this {} type".format(type(value))
                )


def assert_dataframe(actual: pd.DataFrame, expected: pd.DataFrame):
    actual = actual.reindex(expected.index)
    actual = actual[expected.columns]
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)
