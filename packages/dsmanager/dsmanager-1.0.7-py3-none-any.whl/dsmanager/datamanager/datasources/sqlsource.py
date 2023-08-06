"""@Author: Rayane AMROUCHE

Local Sources Handling
"""

import os

from urllib.parse import quote
from typing import Any

import pandas as pd  # type: ignore
import sqlalchemy  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource


class SqlSource(DataSource):
    """Inherited Data Source Class for sql sources
    """

    def read(self, source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data

        Args:
            source_info (dict): Source metadatas

        Returns:
            Any: Source datas
        """
        data = None

        super().read(source_info, **kwargs)

        dialect = source_info["dialect"]
        database = source_info["database"]
        username = os.environ.get(source_info["username_env_name"], "")
        password = os.environ.get(source_info["password_env_name"], "")
        address = source_info["address"]

        engine = sqlalchemy.create_engine(
            f"{dialect}://{username}:{quote(password)}@{address}/{database}"
        )

        conn = engine.connect()
        if "query" in source_info:
            data = pd.read_sql_query(
                source_info["query"],
                conn,
                **source_info["args"]
            )
        conn.close()

        self.logger.info(
            "Query sql server '%s' with query: '%s'",
            f"{dialect}://{username}:***@{address}/{database}",
            source_info["query"]
        )

        return data

    def read_db(self, source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns a source engine

        Args:
            source_info (dict): Source metadatas

        Raises:
            Exception: Raised if missing needed metadatas

        Returns:
            Any: Source engine
        """
        super().read(source_info, **kwargs)

        dialect = source_info["dialect"]
        database = source_info["database"]
        username = os.environ.get(source_info["username_env_name"], "")
        password = os.environ.get(source_info["password_env_name"], "")
        address = source_info["address"]

        engine = sqlalchemy.create_engine(
            f"{dialect}://{username}:{quote(password)}@{address}/{database}"
        )

        self.logger.info(
            "Handle sql server '%s'",
            f"{dialect}://{username}:***@{address}/{database}"
        )

        return engine
