import pandas as pd
import numpy as np


def output_1_dtypes_fixture():
    # Dtypes
    dtypes_test_1 = {}
    dtypes_test_1["boolean_like_columns"] = ["random"]
    dtypes_test_1["datetime"] = ["date"]
    dtypes_test_1["categorical_like_columns"] = []
    dtypes_test_1["potential_uid_columns"] = pd.DataFrame(
        {
            "column_name": {
                0: "uid",
                1: "date",
                2: "id",
                3: "desc",
                4: "value",
                5: "volume",
                6: "random",
            },
            "unique_identifier_count": {0: 16, 1: 5, 2: 7, 3: 7, 4: 8, 5: 7, 6: 1},
            "number_of_explicit_na": {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 2},
            "number_of_duplicates": {0: 1, 1: 12, 2: 10, 3: 10, 4: 8, 5: 8, 6: 14},
        }
    )

    # Not tested keys
    not_tested_keys = []

    return dtypes_test_1, not_tested_keys


def output_1_summary_fixture():
    summary_test_1 = {}
    summary_test_1["describe"] = pd.DataFrame(
        {
            "uid": {
                "sum": 137.0,
                "count": 17.0,
                "mean": 8.058823529411764,
                "std": 4.955685979701677,
                "mean-2*std": -1.8525484299915895,
                "IQR_lower": -8.0,
                "min": 1.0,
                "5%": 1.0,
                "25%": 4.0,
                "50%": 8.0,
                "75%": 12.0,
                "95%": 15.2,
                "max": 16.0,
                "IQR_upper": 24.0,
                "mean+2*std": 17.97019548881512,
                "IQR": 8.0,
            },
            "value": {
                "sum": 20000367.0,
                "count": 16.0,
                "mean": 1250022.9375,
                "std": 4999993.883383731,
                "mean-2*std": -8749964.829267463,
                "IQR_lower": -20.0,
                "min": 5.0,
                "5%": 5.0,
                "25%": 10.0,
                "50%": 20.0,
                "75%": 30.0,
                "95%": 5000075.0,
                "max": 20000000.0,
                "IQR_upper": 60.0,
                "mean+2*std": 11250010.704267463,
                "IQR": 20.0,
            },
            "volume": {
                "sum": 63.0,
                "count": 15.0,
                "mean": 4.2,
                "std": 2.596701204000403,
                "mean-2*std": -0.9934024080008061,
                "IQR_lower": -4.0,
                "min": 1.0,
                "5%": 1.0,
                "25%": 2.0,
                "50%": 4.0,
                "75%": 6.0,
                "95%": 8.599999999999998,
                "max": 10.0,
                "IQR_upper": 12.0,
                "mean+2*std": 9.393402408000807,
                "IQR": 4.0,
            },
            "random": {
                "sum": 15.0,
                "count": 15.0,
                "mean": 1.0,
                "std": 0.0,
                "mean-2*std": 1.0,
                "IQR_lower": 1.0,
                "min": 1.0,
                "5%": 1.0,
                "25%": 1.0,
                "50%": 1.0,
                "75%": 1.0,
                "95%": 1.0,
                "max": 1.0,
                "IQR_upper": 1.0,
                "mean+2*std": 1.0,
                "IQR": 0.0,
            },
        }
    )

    summary_test_1["info"] = pd.DataFrame(
        {
            "columns": {
                0: "uid",
                1: "date",
                2: "id",
                3: "desc",
                4: "value",
                5: "volume",
                6: "random",
            },
            "non_nulls": {0: 17, 1: 17, 2: 17, 3: 17, 4: 16, 5: 15, 6: 15},
            "nulls": {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 2},
            "type": {
                0: np.dtype("int32"),
                1: np.dtype("<M8[ns]"),
                2: np.dtype("O"),
                3: np.dtype("O"),
                4: np.dtype("float64"),
                5: np.dtype("float64"),
                6: np.dtype("float64"),
            },
            "zeros": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
            "non_nulls_%": {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 0.94, 5: 0.88, 6: 0.88},
            "nulls_%": {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.06, 5: 0.12, 6: 0.12},
            "zero_%": {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0},
        }
    )

    # Not tested keys
    not_tested_keys = []

    return summary_test_1, not_tested_keys


def output_1_missing_values_fixture():
    missing_values_test_1 = {}
    missing_values_test_1["dates_continuity_check"] = pd.DataFrame(
        {
            "col": {0: "date", 1: "date", 2: "date"},
            "freq": {0: "M", 1: "Q", 2: "A"},
            "max_value_of_diff_between_periods": {0: 3, 1: 1, 2: 1},
            "missing_periods": {
                0: pd.PeriodIndex(
                    [
                        "2020-01",
                        "2020-02",
                        "2020-04",
                        "2020-05",
                        "2020-07",
                        "2020-08",
                        "2020-10",
                        "2020-11",
                    ],
                    dtype="period[M]",
                ),
                1: pd.PeriodIndex([], dtype="period[Q-DEC]"),
                2: pd.PeriodIndex([], dtype="period[A-DEC]"),
            },
            "number_of_missing_periods": {0: 8, 1: 0, 2: 0},
        }
    )
    missing_values_test_1["na_like_values_in_str_columns"] = {
        "id": ["na"],
        "desc": [""],
    }
    missing_values_test_1["na_in_datetime_columns"] = {"date": []}
    # Not tested keys
    not_tested_keys = [
        "plotly_missing_values_heatmap",
        "plotly_correlation_missing_values",
    ]

    return missing_values_test_1, not_tested_keys


def output_1_downcasting_fixture():
    downcasting_test_1 = {}
    downcasting_test_1["to_float32"] = ["value", "volume", "random"]

    # Not tested keys
    not_tested_keys = []

    return downcasting_test_1, not_tested_keys


def output_1_duplicates_fixture():
    duplicate_test_1 = {}
    duplicate_test_1["redundant_columns"] = {"random": 2}
    duplicate_test_1["duplicate_rows"] = [1]

    # Not tested keys
    not_tested_keys = []

    return duplicate_test_1, not_tested_keys


def output_1_data_analysis_fixture():
    data_analysis_test_1 = {}
    data_analysis_test_1["top_20_most_frequent_values"] = pd.DataFrame(
        {
            "id": {0: "A", 1: "B", 2: "C", 3: "na", 4: "E", 5: "F", 6: "G"},
            "desc": {
                0: "this is A",
                1: "this is B",
                2: "this is C",
                3: "",
                4: "this is E",
                5: "this is F",
                6: "this is G",
            },
        }
    )

    # Not tested keys
    not_tested_keys = [
        "plotly_correlation_numerical",
        "plotly_correlation_non_numerical",
        "histogram_matplotlib",
    ]

    return data_analysis_test_1, not_tested_keys


def output_1_df_cdf():
    df_cdf = pd.DataFrame(
        {
            "value": {
                0: 5.0,
                1: 5.0,
                2: 10.0,
                9: 10.0,
                13: 10.0,
                7: 17.0,
                3: 20.0,
                8: 20.0,
                10: 20.0,
                14: 20.0,
                4: 30.0,
                12: 30.0,
                15: 30.0,
                5: 40.0,
                16: 100.0,
                11: 20000000.0,
            },
            "count": {
                0: 1,
                1: 1,
                2: 1,
                9: 1,
                13: 1,
                7: 1,
                3: 1,
                8: 1,
                10: 1,
                14: 1,
                4: 1,
                12: 1,
                15: 1,
                5: 1,
                16: 1,
                11: 1,
            },
            "cum_count": {
                0: 1,
                1: 2,
                2: 3,
                9: 4,
                13: 5,
                7: 6,
                3: 7,
                8: 8,
                10: 9,
                14: 10,
                4: 11,
                12: 12,
                15: 13,
                5: 14,
                16: 15,
                11: 16,
            },
            "cdf": {
                0: 0.0625,
                1: 0.125,
                2: 0.1875,
                9: 0.25,
                13: 0.3125,
                7: 0.375,
                3: 0.4375,
                8: 0.5,
                10: 0.5625,
                14: 0.625,
                4: 0.6875,
                12: 0.75,
                15: 0.8125,
                5: 0.875,
                16: 0.9375,
                11: 1.0,
            },
            "1-cdf": {
                0: 0.9375,
                1: 0.875,
                2: 0.8125,
                9: 0.75,
                13: 0.6875,
                7: 0.625,
                3: 0.5625,
                8: 0.5,
                10: 0.4375,
                14: 0.375,
                4: 0.3125,
                12: 0.25,
                15: 0.1875,
                5: 0.125,
                16: 0.0625,
                11: 0.0,
            },
            "remaining_count": {
                0: 15,
                1: 14,
                2: 13,
                9: 12,
                13: 11,
                7: 10,
                3: 9,
                8: 8,
                10: 7,
                14: 6,
                4: 5,
                12: 4,
                15: 3,
                5: 2,
                16: 1,
                11: 0,
            },
        }
    )
    return df_cdf
