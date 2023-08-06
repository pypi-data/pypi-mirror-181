"""@Author: Rayane AMROUCHE

Local Sources Handling
"""

import os

from typing import Any

import paramiko  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource


class FtpSource(DataSource):
    """Inherited Data Source Class for ftp sources
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

        sftp_server = source_info["sftp_server"]
        port = int(source_info["port"])
        username = os.environ.get(source_info["username_env_name"], "")
        password = os.environ.get(source_info["password_env_name"], "")

        transport = paramiko.Transport((sftp_server, port))
        transport.connect(None, username, password)
        engine = paramiko.SFTPClient.from_transport(transport)

        file = engine.open(source_info["path"])

        data = super().handle_file_types(file, source_info)

        engine.close()

        self.logger.info(
            "Handle '%s' file in path: '%s' on ftp server '%s'",
            source_info["type"],
            source_info["path"],
            sftp_server
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

        sftp_server = source_info["sftp_server"]
        port = int(source_info["port"])
        username = os.environ.get(source_info["username_env_name"], "")
        password = os.environ.get(source_info["password_env_name"], "")

        transport = paramiko.Transport((sftp_server, port))
        transport.connect(None, username, password)
        engine = paramiko.SFTPClient.from_transport(transport)

        self.logger.info(
            "Handle ftp server '%s'",
            sftp_server
        )

        return engine
