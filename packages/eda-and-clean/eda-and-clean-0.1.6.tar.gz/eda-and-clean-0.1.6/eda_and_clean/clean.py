import pandas as pd
import numpy as np
import warnings
from math import isclose
from .utils import filter_non_capitalized_words_from_list
from .const import std_vals


class clean_class:
    def __init__(
        self,
    ) -> None:
        """
        Options:
        1. remove_existing_index_and_make_new_one [input: _df: pd.DataFrame] [output: pd.DataFrame]
        2. drop_duplicate_rows [input: _df: pd.DataFrame] [output: pd.DataFrame]
        3. drop_columns [input: _df: pd.DataFrame, cols_to_drop: list] [output: pd.DataFrame]
        4. convert_dtype [input: _df: pd.DataFrame, dict_with_cols_to_convert: dict (key: dtype, value: list of columns)] [output: pd.DataFrame]
        5. convert_str_to_uid_int, NOT RECOMMENDED [input: _df_input: pd.DataFrame, col_to_convert_to_int: str,int_type: str] [output: pd.DataFrame]
        6. clean_str_columns [input: _df: pd.DataFrame, str_cols_to_clean: list, operations_to_perform: list = [
            "make_str_col_lowercase",
            "tokenize_remove_stop_words_and_stem",
            "remove_punctuation",
            "remove_non_alphabets",
            "remove_words_less_than_length_3", list_of_stopwords_to_remove: list = []
        ]] [output: pd.DataFrame]
        7. fill_value_in_masked_entries [input: _df: pd.DataFrame, dict_with_col_name_as_key_and_mask_as_value_to_make_na: dict] [output: pd.DataFrame]
        8. drop_rows [input: _df: pd.DataFrame, row_mask_to_drop: pd.Series] [output: pd.DataFrame]
        """

        # Initialize tracker
        self.cols_in_tracker = [
            "order",
            "activity",
            "cols_impacted",
            "num_of_cols_impacted",
            "rows_impacted",
            "num_of_rows_impacted",
        ]
        self.na_like_values = std_vals.na_like_items_in_str
        self.counter = 1
        self.TRACKER = pd.DataFrame(columns=self.cols_in_tracker)

    def remove_existing_index_and_make_new_one(self, _df: pd.DataFrame) -> pd.DataFrame:
        df = _df.copy()
        df = df.reset_index(drop=True)

        # Track changes
        self.track_changes(
            activity="remove_existing_index_and_make_new_one",
            cols_impacted=[],
            num_of_cols_impacted=0,
            rows_impacted=[],
            num_of_rows_impacted=np.nan,
        )

        # Save output
        self.OUTPUT = df.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def fill_value_in_masked_entries(
        self,
        _df: pd.DataFrame,
        dict_with_col_name_as_key_and_mask_as_value_to_make_na: dict,
        fill_value,
    ) -> pd.DataFrame:
        df = _df.copy()
        for (
            key,
            value,
        ) in dict_with_col_name_as_key_and_mask_as_value_to_make_na.items():
            df = self.fill_value_in_one_col_mask(
                _df=df, row_mask_to_make_na=value, col=key, fill_value=fill_value
            )

        # Note: Tracking is done in the underlying function

        # Save output
        self.OUTPUT = df.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def fill_value_in_one_col_mask(
        self, _df: pd.DataFrame, row_mask_to_make_na: pd.Series, col: str, fill_value
    ):
        df = _df.copy()
        df.loc[row_mask_to_make_na, col] = fill_value
        self.track_changes(
            activity="make_mask_na",
            cols_impacted=[col],
            num_of_cols_impacted=1,
            rows_impacted=(df[row_mask_to_make_na]).index.tolist(),
            num_of_rows_impacted=len((df[row_mask_to_make_na]).index.tolist()),
        )

        return df

    def drop_rows(self, _df: pd.DataFrame, row_mask_to_drop: pd.Series) -> pd.DataFrame:
        df = _df.copy()
        df_output = df.loc[~row_mask_to_drop]
        self.track_changes(
            activity="drop_rows",
            cols_impacted=[],
            num_of_cols_impacted=0,
            rows_impacted=(df[row_mask_to_drop]).index.tolist(),
            num_of_rows_impacted=len((df[row_mask_to_drop]).index.tolist()),
        )

        # Save output
        self.OUTPUT = df_output.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def _make_str_cols_lowercase(self, _df: pd.DataFrame, cols: list) -> pd.DataFrame:
        # Operations performed here will not be recorded. Please use clean_str_columns instead

        df = _df.copy()

        # Remove duplicates if any
        cols = list(set(cols))

        # Check if list of cols are in df
        cols_in_df = df.columns.tolist()
        cols_in_input_cols_not_in_df = list(set(cols) - set(cols_in_df))
        if len(cols_in_input_cols_not_in_df) > 0:
            warnings.warn(f"Some columns in {cols} are not in the dataframe")

        # Make sure cols are string
        str_cols_in_df = df.select_dtypes(exclude=np.number).columns.tolist()
        common_str_cols = list(set(cols).intersection(set(str_cols_in_df)))
        non_str_cols_in_input_cols = list(set(cols).difference(set(str_cols_in_df)))
        if len(non_str_cols_in_input_cols) > 0:
            warnings.warn(f"{non_str_cols_in_input_cols} are not string columns")

        # Make str_cols lowercase
        for col in common_str_cols:
            try:
                df[col] = df[col].str.lower()
            except AttributeError:
                warnings.warn(f"Could not make {col} lowercase")

        # return df so that we can use pandas pipe
        return df

    def track_changes(
        self,
        activity: str,
        cols_impacted: list,
        num_of_cols_impacted: int,
        rows_impacted: list,
        num_of_rows_impacted: int,
    ) -> None:
        temp = pd.DataFrame(
            [
                [
                    self.counter,
                    activity,
                    cols_impacted,
                    num_of_cols_impacted,
                    rows_impacted,
                    num_of_rows_impacted,
                ]
            ],
            columns=self.cols_in_tracker,
        )
        self.TRACKER = pd.concat([self.TRACKER, temp])
        self.counter += 1

    def drop_columns(self, _df: pd.DataFrame, cols_to_drop: list) -> pd.DataFrame:
        df = _df.copy()
        df = df.drop(columns=cols_to_drop)

        # Track changes
        self.track_changes(
            activity="drop_columns",
            cols_impacted=cols_to_drop,
            num_of_cols_impacted=len(cols_to_drop),
            rows_impacted=[],
            num_of_rows_impacted=np.nan,
        )

        # Save output
        self.OUTPUT = df.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def clean_str_columns(
        self,
        _df: pd.DataFrame,
        str_cols_to_clean: list,
        operations_to_perform: list = [
            "make_str_col_lowercase",
            "tokenize_remove_stop_words_and_stem",
            "remove_punctuation",
            "remove_non_alphabets",
            "remove_words_less_than_length_3",
        ],
        list_of_stopwords_to_remove=[],
    ) -> pd.DataFrame:

        df = _df.copy()
        df_original = df.copy()
        columns_impacted = []

        # Identify string columns
        string_cols = _df.select_dtypes(include=["object"]).columns.tolist()
        string_cols = list(set(string_cols).intersection(set(str_cols_to_clean)))
        if len(str_cols_to_clean) > len(string_cols):
            warnings.warn(
                f"Some columns in {str_cols_to_clean} are not string columns. Only {string_cols} will be cleaned"
            )

        # Loop through evert string column and clean textual data
        for col in string_cols:
            # Make na values as empty string
            df[col] = df[col].fillna("")

            if "make_str_col_lowercase" in operations_to_perform:
                df = self._make_str_cols_lowercase(_df=df, cols=[col])

            if "tokenize_remove_stop_words_and_stem" in operations_to_perform:
                from nltk.corpus import stopwords
                from nltk.tokenize import word_tokenize
                from nltk.stem.snowball import EnglishStemmer

                stemmer = EnglishStemmer()
                # Tokenize
                df[col] = df[col].apply(word_tokenize)
                # Remove stop words
                stop = stopwords.words("english")
                stop = list(set(stop) - set(list_of_stopwords_to_remove))

                df[col] = df[col].apply(
                    lambda x: [item for item in x if item not in stop]
                )
                # Stem every word
                df[col] = df[col].apply(lambda x: [stemmer.stem(y) for y in x])
                # Make column of list to str
                df[col] = df[col].apply(lambda x: " ".join(map(str, x)))

            if "remove_punctuation" in operations_to_perform:
                # Remove punctuations
                df[col] = df[col].str.replace("[^\w\s]", "")

            if "remove_non_alphabets" in operations_to_perform:
                # Remove everything other than alphabets
                df[col] = df[col].str.replace("[^a-zA-Z]", " ")

            if "remove_words_less_than_length_3" in operations_to_perform:
                # Remove words with length less than 3
                df[col] = df[col].str.findall("\w{3,}").str.join(" ")
            # Determine if the column was impacted
            columns_impacted.append(col) if df[col].equals(
                df_original[col]
            ) == False else None

        # Initiate tracker
        self.track_changes(
            activity="clean_str_columns",
            cols_impacted=columns_impacted,
            num_of_cols_impacted=len(columns_impacted),
            rows_impacted=[],
            num_of_rows_impacted=np.nan,
        )

        # Save output
        self.OUTPUT = df.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def drop_duplicate_rows(self, _df: pd.DataFrame) -> pd.DataFrame:
        df = _df.copy()
        df_original = df.copy()
        df = df.drop_duplicates()
        num_of_rows_dropped = df_original.shape[0] - df.shape[0]
        self.track_changes(
            activity="drop_duplicate_rows",
            cols_impacted=[],
            num_of_cols_impacted=0,
            rows_impacted=list(set(df_original.index) - set(df.index)),
            num_of_rows_impacted=num_of_rows_dropped,
        )

        # Save output
        self.OUTPUT = df.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def get_attributes_of_class(self) -> list:
        return [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]

    def get_output_attributes_of_class(self) -> list:
        all_attributes = self.get_attributes_of_class()
        return filter_non_capitalized_words_from_list(_list=all_attributes)

    def convert_dtype(
        self, _df: pd.DataFrame, dict_with_cols_to_convert: dict
    ) -> pd.DataFrame:
        df = _df.copy()

        # Loop through the dictionary and downcast the columns
        for target_dtype, list_of_cols in dict_with_cols_to_convert.items():
            df = self.convert_one_dtype_at_a_time(
                _df=df, cols_to_convert=list_of_cols, target_dtype=target_dtype
            )
        # Note: Tracking has been done in the underlying function

        # Save output
        self.OUTPUT = df.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT

    def convert_one_dtype_at_a_time(
        self, _df: pd.DataFrame, cols_to_convert: list, target_dtype: str
    ) -> pd.DataFrame:
        df = _df.copy()

        # Recording original df
        df_original = df.copy()
        original_numeric_dtypes = df_original.select_dtypes(
            include=np.number
        ).columns.to_list()

        # Get the columns in cols_to_convert that are in df
        cols_to_convert = list(set(cols_to_convert) & set(df.columns))

        record_of_cols_impacted = []
        # Downcast the columns
        for col in cols_to_convert:
            df[col] = df[col].astype(target_dtype)

            if col in original_numeric_dtypes:
                # Calculate mean of the columns in the original df and the downcasted df
                original_mean = df_original[col].mean()
                new_mean = df[col].mean()

                if isclose(original_mean, new_mean, rel_tol=0.000001) == False:
                    print(
                        f"Converting to {target_dtype} has resulted in loss of information for column {col} therefore reverting back to original dtype"
                    )
                    df[col] = df_original[col]
                else:
                    record_of_cols_impacted.append(col)

        # Track changes
        self.track_changes(
            activity=f"converting_to_{target_dtype}",
            cols_impacted=record_of_cols_impacted,
            num_of_cols_impacted=len(record_of_cols_impacted),
            rows_impacted=[],
            num_of_rows_impacted=np.nan,
        )

        return df

    def convert_str_to_uid_int(
        self,
        _df: pd.DataFrame,
        col_to_convert_to_int: str,
        int_type: str = "int32",
    ) -> pd.DataFrame:
        """
        This function is used to map unique values in a column to integer with objective of saving memory

        Parameters
        ----------------------------------------
        _df (pd.DataFrame): Input dataframe
        col_to_convert_to_int (str): column name in _df_input that needs to coded up using random numbers
        int_type (str): Deafult: "int32" or altenatively use "int64"

        Returns
        ---------------------------------------
        pd.DataFrame: Output dataframe with the str uid repalced with integer uid column
        """
        df_input = _df.copy()

        # Input validation
        if not isinstance(df_input, pd.DataFrame):
            raise ValueError(
                f"df_input needs to be a dataframe but got {type(df_input)}"
            )
        if col_to_convert_to_int not in _df_input.columns:
            raise ValueError(
                f"The input dataframe does not have the column by the name {col_to_convert_to_int}"
            )
        if int_type not in ["int32", "int64"]:
            raise ValueError("The function supports int32 and int64 alone")

        # Get a dictionary that maps the column value to an unique int value
        df_mapping = pd.DataFrame()
        df_mapping[col_to_convert_to_int] = df_input[col_to_convert_to_int].unique()
        df_mapping = df_mapping.reset_index()
        df_mapping = df_mapping.rename(
            columns={"index": col_to_convert_to_int + "_int"}
        )
        df_mapping = df_mapping.set_index([col_to_convert_to_int])
        dict_mapping = df_mapping.to_dict()[col_to_convert_to_int + "_int"]

        # Replace the col value with the int value
        df_input[col_to_convert_to_int] = df_input[col_to_convert_to_int].map(
            dict_mapping
        )
        df_input[col_to_convert_to_int] = df_input[col_to_convert_to_int].astype(
            int_type
        )

        # Save output
        self.OUTPUT = df_input.copy()
        self.UID_MAPPING_DF = df_mapping.copy()

        # return df so that we can use pandas pipe
        return self.OUTPUT
