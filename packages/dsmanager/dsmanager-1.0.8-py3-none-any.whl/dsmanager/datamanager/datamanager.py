"""@Author: Rayane AMROUCHE

Datamanager Class
"""

import os
import json
from typing import Any

from dotenv import load_dotenv  # type: ignore

from dsmanager.datamanager.utils import Utils, DataManagerIOException
from dsmanager.controller.logger import make_logger
from dsmanager.controller.utils import json_to_dict
from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.datasources.localsource import LocalSource
from dsmanager.datamanager.datasources.httpsource import HttpSource
from dsmanager.datamanager.datasources.sqlsource import SqlSource
from dsmanager.datamanager.datasources.ftpsource import FtpSource
from dsmanager.datamanager.datasources.sharepointsource import SharepointSource
from dsmanager.datamanager.datasources.sfsource import SFSource


class DataManager:
    """DataManager class handle all the data work"""

    def __init__(self,
                 metafile_path: str = "data/metadata.json",
                 logger_path: str = "/tmp/logs",
                 env_path: str = None,
                 preload: bool = False,
                 ) -> None:
        """Init Datamanager by giving the datasets metadata path

        Args:
            metafile_path (str, optional): Path of the metadata file of the
                datasets. Defaults to "data/metadata.json".
        """
        if env_path:
            load_dotenv(env_path)
        if metafile_path:
            json_to_dict(metafile_path)

        self.databases = DataStorage()
        self.datas = DataStorage()
        self.env_path = env_path
        self.logger = make_logger(
            os.path.join(logger_path, "datamanager"),
            "datamanager"
        )
        self.metadata_path = metafile_path
        self.datasources = DataStorage()
        self.utils = Utils(self, logger_path)

        self.datasources["local"] = LocalSource
        self.datasources["http"] = HttpSource
        self.datasources["sql"] = SqlSource
        self.datasources["ftp"] = FtpSource
        self.datasources["sharepoint"] = SharepointSource
        self.datasources["salesforce"] = SFSource

        if preload:
            metadata = json_to_dict(self.metadata_path)
            for key in metadata.keys():
                try:
                    self.get_data(key)
                    self.logger.info("Preloaded %s", key)
                except DataManagerIOException as dm_e:
                    self.logger.info("Failed to preload '%s' with message : '%s'",
                                     key,
                                     dm_e)

    def add_datasource(self, name: str, source: DataSource):
        """Add a source class to datasources dict

        Args:
            name (str): Name of the source
            source (DataSource): Data Source class
        """
        self.datasources[name] = source

    def add_source(self, name: str, source_info: dict):
        """Add a source class to sources dict

        Args:
            name (str): Name of the source
            source (DataSource): Data Source class
        """
        metadata = json_to_dict(self.metadata_path)
        metadata[name] = source_info
        with open(self.metadata_path, "w", encoding="utf-8") as metadata_file:
            json.dump(metadata, metadata_file)

    def get_sources(self):
        """Get source from metadata

        Args:
            name (str): Name of the source
            source (DataSource): Data Source class
        """
        metadata = json_to_dict(self.metadata_path)
        return metadata

    def get_source_info(self, name: str) -> dict:
        """Handle access to metadata info for a given source

        Args:
            name (str): Name of the source to access

        Raises:
            Exception: Raised if the name given is not in the metadata

        Returns:
            dict: Return the metadata of the data source
        """
        metadata = json_to_dict(self.metadata_path)
        if name not in metadata:
            raise DataManagerIOException(
                {}, f"{name} not in the metadata file")
        data = metadata[name]
        return data

    def get_source_reader(self, source_info: dict) -> DataSource:
        """Get data sources reader for a given data source's metadata

        Args:
            source_info (dict): Metadata of a data source

        Raises:
            DataManagerIOException: Raised if the source is not handled

        Returns:
            DataSource: Data source reader
        """
        if "source_type" in source_info:
            source_type = source_info["source_type"]
            del source_info["source_type"]
        else:
            source_type = "local"

        if source_type in self.datasources:
            source_class = self.datasources[source_type]
        else:
            raise DataManagerIOException(source_info)

        return source_class

    def get_data(self,
                 name: str,
                 save: bool = True,
                 reload: bool = False,
                 alias: str = None,
                 **kwargs: Any
                 ) -> Any:
        """Get info for a given source and return its data

        Args:
            name (str): Name of the data source
            save (bool, optional): If True save the data. Defaults to True.
            reload (bool, optional): If False try to load from datas. Defaults
                to False.
            alias (str, optional): Alias name of the data in datas. Defaults to
                None.

        Returns:
            Any: Requested data
        """
        if not reload and name in self.datas:
            data = self.datas[name]
        else:
            source_info = self.get_source_info(name)
            source = self.get_source_reader(source_info)
            data = source(self.logger).read(source_info, **kwargs)
        if save:
            self.datas[name] = data
            if alias:
                self.datas[alias] = self.datas[name]

        return data

    def get_database(self,
                     name: str,
                     save: bool = True,
                     reload: bool = False,
                     alias: str = None,
                     **kwargs: Any
                     ) -> Any:
        """Get info for a given source and return its data

        Args:
            name (str): Name of the data source
            save (bool, optional): If True save the database. Defaults to True.
            reload (bool, optional): If False try to load from databases. Defaults
                to False.
            alias (str, optional): Alias name of the data in databases. Defaults
                to None.

        Returns:
            Any: Requested database engine
        """
        if not reload and name in self.databases:
            data = self.databases[name]
        else:
            source_info = self.get_source_info(name)
            source = self.get_source_reader(source_info)
            data = source(self.logger).read_db(source_info, **kwargs)
        if save:
            self.databases[name] = data
            if alias:
                self.databases[alias] = self.databases[name]

        return data

    def get_env(self,
                name: str,
                default: str = "",
                ) -> str:
        """Get info for a specified dataset and return it as a DataFrame

        Args:
            name (str): Name of the variable in env
            default (str): Default value if name is not in env
            env_path (str): Path of the env file

        Returns:
            str: env variable
        """
        if self.env_path:
            load_dotenv(self.env_path)
        res = os.environ.get(name, default)
        return res
