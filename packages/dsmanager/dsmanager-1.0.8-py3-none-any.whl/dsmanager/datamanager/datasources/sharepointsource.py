"""@Author: Rayane AMROUCHE

Local Sources Handling
"""

import os
import io

from typing import Any

from shareplum import Site  # type: ignore
from shareplum import Office365  # type: ignore
from shareplum.site import Version  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.utils import DataManagerIOException


class SharepointSource(DataSource):
    """Inherited Data Source Class for sharepoint sources
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

        path = source_info['sharepoint_path'].split("/")
        authcookie = Office365(
            "/".join(path[:3]),
            username=os.environ.get(source_info["username_env_name"]),
            password=os.environ.get(source_info["password_env_name"]),
        ).GetCookies()
        site = Site(
            "/".join(path[:5]),
            version=Version.v365,
            authcookie=authcookie,
        )
        folder = site.Folder("/".join(path[5:-1]))
        file = folder.get_file(path[-1])

        if isinstance(file, bytes) and "encoding" in source_info:
            try:
                file = io.StringIO(file.decode(source_info["encoding"]))
            except UnicodeDecodeError:
                return file

        data = super().handle_file_types(file, source_info)

        self.logger.info(
            "Get '%s' %s file from sharepoint's path: '%s'",
            source_info["type"],
            file,
            source_info["path"]
        )
        return data

    def read_db(self, source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns a sharepoint source engine

        Args:
            source_info (dict): Source metadatas

        Raises:
            Exception: Raised if missing needed metadatas

        Returns:
            Any: Source engine
        """

        raise DataManagerIOException(
            source_info,
            "Sharepoint source does not handle read_db"
        )
