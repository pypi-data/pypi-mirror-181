"""@Author: Rayane AMROUCHE

Data Sources Handling
"""

from typing import Any
from logging import Logger

import pandas as pd  # type: ignore

from dsmanager.datamanager.utils import DataManagerIOException


class DataSource():
    """Data Source Class
    """

    def __init__(self, logger: Logger) -> None:
        """Init a Data Source

        Args:
            logger (Logger): Passed down logger from the Data Manager
        """
        self.logger = logger

    def handle_file_types(self, file: Any, source_info: dict):
        """Handle different type of files before opening in pandas dataframe

        Args:
            file (Any): file to read
            source_info (dict): Source metadatas

        Returns:
            Any: file data
        """
        data = None
        if source_info["type"] == "csv":
            data = pd.read_csv(file, **source_info["args"])
        elif source_info["type"] == "excel":
            data = pd.read_excel(file, **source_info["args"])
        elif source_info["type"] == "json":
            data = pd.Series(file)
        elif source_info["type"] == "text":
            encoding = "utf-8"
            if "encoding" in source_info:
                encoding = source_info["encoding"]
            with open(file, "r", encoding=encoding) as file_obj:
                data = file_obj.read()
        else:
            raise DataManagerIOException(
                source_info,
                "File type unknown or not supported"
            )
        return data

    def read(self, source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns the source data

        Args:
            source_info (dict): Source metadatas

        Raises:
            Exception: Raised if missing needed metadatas

        Returns:
            Any: Source datas
        """
        if "args" not in source_info:
            source_info["args"] = {}
        source_info["args"].update(**kwargs)

    def read_db(self, source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns a source engine

        Args:
            source_info (dict): Source metadatas

        Raises:
            Exception: Raised if missing needed metadatas

        Returns:
            Any: Source engine
        """
        if "args" not in source_info:
            source_info["args"] = {}
        source_info["args"].update(**kwargs)
