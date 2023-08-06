"""@Author: Rayane AMROUCHE

Preprocesser for DataManager
"""

import os

from typing import Any, List

import pandas as pd  # type: ignore

from dsmanager.controller.logger import make_logger


class Preprocesser:
    """Preprocess class brings preprocess tools for the data manager
    """

    def __init__(self,
                 logger_path: str = "/tmp/logs"):
        """Init class Preprocesser with an empty local storage
        """
        self.logger = make_logger(
            os.path.join(logger_path, "datamanager"),
            "preprocess")
        self.local_vars = {}

    def standard_scale(self, df_: pd.DataFrame, subset: List[str]) -> pd.DataFrame:
        """Print head of a dataframe

        Args:
            df_ (pd.DataFrame): DataFrame whose head is to be displayed
            n_val (int, optional): Number of rows to display. Defaults to 5.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining
        """
        if not subset:
            subset = df_.columns.values
        df_[subset] -= df_[subset].mean() / df_[subset].std()
        return df_

    def minmax_scale(self, df_: pd.DataFrame, subset: List[str], max_=1, min_=0) -> pd.DataFrame:
        """Print head of a dataframe

        Args:
            df_ (pd.DataFrame): DataFrame whose head is to be displayed
            n_val (int, optional): Number of rows to display. Defaults to 5.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining
        """
        if not subset:
            subset = df_.columns.values
        x_std = df_[subset] - df_[subset].min(axis=0)
        x_std /= (df_[subset].max(axis=0) - df_[subset].min(axis=0))
        df_[subset] = x_std * (max_ - min_) + min_
        return df_

    def to_category(self,
                    df_: pd.DataFrame,
                    column: str,
                    category_name: str,
                    load: bool = True,
                    **kwargs: Any
                    ) -> pd.DataFrame:
        """Assign category type to a given category and add the category in
            the local vars

        Args:
            df_ (pd.DataFrame): DataFrame whose head is to be displayed

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining
        """
        if "categories" not in kwargs:
            kwargs["categories"] = df_[column].dropna().unique()

        if load and category_name in self.local_vars:
            col_type = self.local_vars[category_name]
            self.logger.info("Load category in preprocesser local vars at: `%s` for column `%s`",
                             category_name,
                             column)
        else:
            col_type = pd.api.types.CategoricalDtype(**kwargs)
            self.local_vars[category_name] = col_type
            self.logger.info("Add category in preprocesser local vars at: `%s` for column `%s`",
                             category_name,
                             column)
        return (
            df_
            .assign(**{
                column: lambda df_: df_[column].astype(col_type)
            })
        )
