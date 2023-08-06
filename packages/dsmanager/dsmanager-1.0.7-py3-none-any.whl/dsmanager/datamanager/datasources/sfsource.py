"""@Author: Rayane AMROUCHE

Local Sources Handling
"""

from typing import Any

import pandas as pd  # type: ignore
from simple_salesforce import Salesforce  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource


class SFSource(DataSource):
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

        username = source_info["username"]
        password = source_info["password"]
        token = source_info["token"]
        domain = source_info["domain"]
        table_name = source_info["table_name"]

        engine = Salesforce(
            username=username,
            password=password,
            security_token=token,
            domain=domain
        )

        column_list = (
            pd.DataFrame(
                getattr(engine, table_name)
                .describe()
                ["fields"]
            )["name"]
        ).to_list()

        columns = ", ".join(column_list)
        query = f"""SELECT {columns} FROM {table_name}"""

        data = engine.query(query)["records"]
        data = pd.DataFrame.from_dict(data, orient='columns').drop("attributes", axis=1)

        self.logger.info(
            "Request salesforce server '%s' with query '%s'",
            f"User={username}&Password=***&SecurityToken=***",
            query,
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
        super().read_db(source_info, **kwargs)

        username = source_info["username"]
        password = source_info["password"]
        token = source_info["token"]
        domain = source_info["domain"]

        engine = Salesforce(
            username=username,
            password=password,
            security_token=token,
            domain=domain
        )

        self.logger.info(
            "Handle salesforce server '%s'",
            f"User={username}&Password=***&SecurityToken=***"
        )

        return engine
