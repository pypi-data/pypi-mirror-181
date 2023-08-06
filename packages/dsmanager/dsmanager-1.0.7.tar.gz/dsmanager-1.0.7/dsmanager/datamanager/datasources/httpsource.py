"""@Author: Rayane AMROUCHE

Local Sources Handling
"""

from typing import Any

import pandas as pd  # type: ignore
import requests  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.utils import DataManagerIOException

REQUEST_PARAMS = [
    "url", "data", "json", "params", "headers", "cookies",
    "files", "auth", "timeout", "allow_redirects", "proxies", "hooks",
    "stream", "verify", "cert",
]


class HttpSource(DataSource):
    """Inherited Data Source Class for http sources
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

        request_params = {}
        for param in REQUEST_PARAMS:
            if param in source_info:
                request_params[param] = source_info[param]
            if "args" in source_info and param in source_info["args"]:
                if param in request_params and isinstance(source_info[param], dict):
                    request_params[param].update(source_info["args"][param])
                else:
                    request_params[param] = source_info["args"][param]
                del source_info["args"][param]

        session = requests.Session()

        args = request_params

        if source_info['request_type'] == "get":
            data = session.get(**args)
        elif source_info['request_type'] == "post":
            data = session.post(**args)
        else:
            raise Exception("Request type not handled")

        self.logger.info(
            "Handle %s http request '%s' with response: '%s'",
            source_info['request_type'],
            str(args),
            data
        )

        if source_info["type"] == "json":
            file = pd.Series(data.json())
        elif source_info["type"] == "text":
            file = data.text
        else:
            file = data
        return file

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
        raise DataManagerIOException(
            source_info,
            "Http source does not handle read_db"
        )
