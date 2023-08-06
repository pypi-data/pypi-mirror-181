# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import os
import json
from datetime import datetime
import logging

# Related third party imports
from azure.storage.fileshare import ShareClient
from azure.core.exceptions import ResourceNotFoundError


# TAGS
__author__ = "Matthew Warren"
__version__ = "1.0.0"
__maintainer__ = ["Matthew Warren"]
__email__ = "mawarren@microsoft.com"
__status__ = "Release"


class FileShareMap:
    """ Creates a hierarchical json map containing metadata for files in the fileshare i.e. their location and size"""

    def __init__(self, conn_string_name, file_share_name, map_file_name="map.json"):
        """__init__ Initialize a file share mapping object

        :param conn_string_name: Name of connection string to retrieve from environment variables. Must be in format:
            https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string
            #configure-a-connection-string-for-an-azure-storage-account
        :type conn_string_name: str
        :param file_share_name: name of fileshare to access from storage account
        :type file_share_name: str
        """
        # TODO: Convert this into a super class that contains common methods for file share and blob container
        try:
            conn_string = os.environ[conn_string_name]
        except KeyError:
            self.logger.exception(f"Failed to retrieve connection string from environment variable {conn_string}"
                                  + "\n"
                                  + "Please provide an environment variable name containing the connection string "
                                  + "for the storage account")
        self.file_share_client = ShareClient.from_connection_string(
            conn_str=conn_string, share_name=file_share_name)
        self.file_list = self.file_share_client.list_directories_and_files()
        self.map_file_name = map_file_name
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.logger.info("### Init complete")

    def _map_directory(self, directory, absolute_paths):
        """_map_directory Create a json map defining size and location of objects within a directory

        Iteratively checks all contained files and subdirectories and recursively maps subdirectories

        :param directory: map object representing the current directory
        :type directory: dict
        :param absolute_paths: list of all parent directory names in order
        :type absolute_paths: list
        :return: a dict / map defining size and location of objects within a directory.
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :rtype: dict
        """
        parent_directory = "/".join(absolute_paths)
        for obj in list(self.file_share_client.list_directories_and_files(parent_directory)):
            self.logger.debug(
                f"### Examining [{obj.name}] in parent directory [{parent_directory}]")
            absolute_path = parent_directory + "/" + obj.name
            if obj['is_directory'] is True:
                absolute_paths.append(obj.name)
                directory['__Contents__'][obj.name] = {
                    '__Name__': obj.name, '__Count__': 0, '__Size__': 0, '__Contents__': {}}
                directory['__Contents__'][obj.name] = self._map_directory(
                    directory=directory['__Contents__'][obj.name], absolute_paths=absolute_paths)
                directory['__Size__'] += directory['__Contents__'][obj.name]['__Size__']
                directory['__Count__'] += directory['__Contents__'][obj.name]['__Count__']
                absolute_paths.pop()
            else:
                sfc = self.file_share_client.get_file_client(absolute_path)
                props = sfc.get_file_properties()
                directory['__Size__'] += props.size
                directory['__Count__'] += 1
                directory['__Contents__'][obj.name] = {
                    '__Name__': obj.name, '__Size__': props.size, '__Count__': 1, '__Path__': absolute_path}
            self.logger.debug(
                f"### Finished working [{obj.name}] in parent directory [{parent_directory}]")
        self.logger.debug(
            f"### Finished mapping directory: [{parent_directory}] with number of contents",
            f" [{len(directory['__Contents__'].keys())}]")
        return directory

    def _map_root(self, level):
        """_map_root Creates the root of the map filling up root level fields with metadata pulled from subdirectories

        _extended_summary_

        :param level: The contents of the root level directory
        :type level: dict
        :return: a dict / map defining size and location of objects within a directory.
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :rtype: dict
        """
        for content in level['__Contents__'].keys():
            level['__Count__'] += level['__Contents__'][content]['__Count__']
            level['__Size__'] += level['__Contents__'][content]['__Size__']
        return level

    def map_file_share(self):
        """map_file_share Generate a dictionary describing the size and location of all contents in a file share

        :return: a dict / map defining size and location of objects within a directory.
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :rtype: dict
        """
        today = datetime.now().strftime("%Y_%m")
        file_share_map = {'__Name__': 'root', '__Size__': 0,
                          '__Count__': 0, '__Contents__': {}, '__Date__': today}
        file_share_map['__Contents__'] = self._map_directory(
            directory=file_share_map, absolute_paths=[])
        file_share_map = self._map_root(file_share_map)
        self.logger.info("### Finished mapping root!")
        return file_share_map

    def write_map_remote(self, storage_map):
        """write_map Writes the supplied storage map to the file share as a json

        :param storeage_map: storage map containing metadata
        :type storage_map: dict
        """
        json_file = json.dumps(storage_map, sort_keys=True, indent=2)
        file_client = self.file_share_client.get_file_client(
            self.map_file_name)
        self.delete_map()
        file_client.upload_file(data=json_file)

    def delete_map(self):
        """delete_map Deletes the map from the file share if it exists"""
        map_file = self.file_share_client.get_file_client(self.map_file_name)
        try:
            props = map_file.get_file_properties()
            if props.size() > 0:
                map_file.delete_file()
        except ResourceNotFoundError as e:
            self.logger.warn(
                f"### Failed when pre-emptively deleting map file at {self.map_file_name}:\n{e}")
