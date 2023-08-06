# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import os
import json
from datetime import datetime
import logging

# Related third party imports
from azure.storage.blob import ContainerClient


# TAGS
__author__ = "Matthew Warren"
__version__ = "1.0.0"
__maintainer__ = ["Matthew Warren"]
__email__ = "mawarren@microsoft.com"
__status__ = "Release"


class ContainerMap:
    """ Create content dictionaries that map the size and location of files in blob containers"""

    def __init__(self, conn_string_name, container_name, map_file_name="map.json"):
        """__init__ Creates a mapping object utilizing a SAS Token Connection string

        :param conn_string_name:  Name of environment variable containing connection string. Connection string must be
            in the format provided from Azure Portal i.e.:
            https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string
            #configure-a-connection-string-for-an-azure-storage-account
        :type conn_string_name: str
        :param container_name:  Name of the container to be mapped
        :type container_name: str
        :param map_file_name: File name for resultant storage map (default "map.json")
        :type map_file_name: str, optional
        """
        # TODO: Convert this into a super class that contains common methods for file share and blob container
        try:
            conn_string = os.environ[conn_string_name]
        except KeyError:
            self.logger.exception(f"Failed to retrieve connection string from environment variable {conn_string}"
                                  + "\n"
                                  + "Please provide an environment variable name containing the connection string "
                                  + "for the storage account")
        self.container_client = ContainerClient.from_connection_string(
            conn_str=conn_string, container_name=container_name)
        self.container_name = container_name
        self.blob_list = self.container_client.list_blobs()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.map_file_name = map_file_name
        self.logger.info("### Init complete")

    def _map_level(self, level, levels, blob_size, path):
        """_map_level Translates a blob's flat path into a tree-like representation recursively, adding the blob's
            metadata to one 'level' of the tree at a time

        :param level: level to add blob data
        :type level: dict
        :param levels: blob subpaths requiring additional translation
        :type levels: list
        :param blob_size: blob bytes
        :type blob_size: int
        :param path: absolute path of the blob
        :type path: str
        :return: a dict / map defining size and location of objects within a directory.
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :rtype: dict
        """
        current_level = levels[0]  # The zero level is the current level in this list of subdirectories
        if current_level in level.keys():  # Level already exists in map from previous blob translation
            level[current_level]['__Size__'] += blob_size
            level[current_level]['__Count__'] += 1
        else:  # create level for the first time
            level[current_level] = {
                '__Name__': current_level,
                '__Size__': blob_size
            }
            if len(levels) > 1:  # new level has sublevels and needs a contents tag
                level[current_level]['__Contents__'] = {}
                # Count the first file being added in this instance
                level[current_level]['__Count__'] = 1
            else:  # No subpaths beneath this newly initialized map level; this is a leaf
                level[current_level]['__Path__'] = path
            # self.logger.info(f"### Level created for [{current_level}]")
        if len(levels) > 2:  # This subcontent contains at least one additional folder
            level[current_level]['__Contents__'] = self._map_level(
                level=level[current_level]['__Contents__'], levels=levels[1:], blob_size=blob_size, path=path)
        elif len(levels) > 1:  # This subcontent is a file / leaf
            level[current_level]['__Contents__'][levels[1]] = {  # The 'One' level is the 'next' level in @levels
                '__Name__': levels[1], '__Size__': blob_size, '__Path__': path}
        return level

    def _map_root(self, level):
        """_map_root Maps the root level of a blob container after all sublevels have been mapped into a dictionary

        :param level: The blob's root level dictionary map
        :type level: dict
        :return: a dict / map defining size and location of objects within a directory.
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :rtype: dict
        """
        for content in level['__Contents__'].keys():
            if '__Count__' in level['__Contents__'][content].keys():
                level['__Count__'] += level['__Contents__'][content]['__Count__']
            else:
                level['__Count__'] += 1
            level['__Size__'] += level['__Contents__'][content]['__Size__']
        return level

    def map_container(self):
        """map_container Translates a blob's flat path into a tree-like representation recursively, adding the blob's
            metadata to one 'level' of the tree at a time

        :return: a dict / map defining size and location of objects within a directory.
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :rtype: dict
        """
        today = datetime.now().strftime("%Y_%m")
        container_map = {'__Name__': 'root', '__Size__': 0,
                         '__Count__': 0, '__Contents__': {}, '__Date__': today}
        # self.logger.info("### Starting blob iteration")
        for blob in self.blob_list:
            container_map['__Contents__'] = self._map_level(
                level=container_map['__Contents__'], levels=blob.name.split("/"), blob_size=blob.size, path=blob.name)
        # self.logger.info(f"### Finished mapping all blobs! [{container_map}]")
        container_map = self._map_root(container_map)
        self.logger.info("Finished mapping root!")
        return container_map

    def write_map_remote(self, storage_map):
        """write_map Writes the supplied storage map to the blob container as a json

        :param storage_map: A json tree reflecting the contents of the provided blob storage container
        :type storage_map: dict
        """
        json_content = json.dumps(
            storage_map, sort_keys=True, indent=2)  # Double space indenting for readability
        blob_client = self.container_client.get_blob_client(self.map_file_name)
        self.delete_map()
        blob_client.upload_blob(data=json_content)
        self.logger.info(
            f"Finished writing map to storage account {self.container_name} at {self.map_file_name}")

    def write_map_local(self, storage_map):
        """write_map Writes the supplied storage map to the local host

        :param storage_map: A json tree reflecting the contents of the provided blob storage container
        :type storage_map: dict
        """
        json_content = json.dumps(
            storage_map, sort_keys=True, indent=2)  # Double space indenting for readability
        json_file = open(self.map_file_name, "w")
        json_file.write(json_content)
        json_file.close()
        self.logger.info(
            f"Finished writing at {os.path.abspath(self.map_file_name)}")

    def delete_map(self):
        """delete_map Deletes the map from the fileshare if it exists"""
        try:
            self.logger.info(f"Attempting to delete {self.map_file_name}")
            blob_client = self.container_client.get_blob_client(
                self.map_file_name)
            if blob_client.exists():
                blob_client.delete_blob()
        except Exception as e:
            self.logger.warn(
                f"Failed to delete {self.map_file_name} before mapping container:\n{e}")
