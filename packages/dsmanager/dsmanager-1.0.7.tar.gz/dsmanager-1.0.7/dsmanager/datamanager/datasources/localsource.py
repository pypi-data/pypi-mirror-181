"""@Author: Rayane AMROUCHE

Local Sources Handling
"""

from typing import Any

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.utils import DataManagerIOException


class LocalSource(DataSource):
    """Inherited Data Source Class for local sources
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

        path = source_info["path"]

        data = super().handle_file_types(path, source_info)

        self.logger.info(
            "Get '%s' file from '%s'",
            source_info["type"],
            source_info["path"]
        )
        return data

    def read_db(self, source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns a local source engine

        Args:
            source_info (dict): Source metadatas

        Raises:
            Exception: Raised if missing needed metadatas

        Returns:
            Any: Source engine
        """

        raise DataManagerIOException(
            source_info,
            "Local source does not handle read_db"
        )
