# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import os
import json
from datetime import datetime
import logging

# Related third party imports
from azure.storage.blob import ContainerClient


class ContainerMap:

    MAP_FILE_NAME = "map.json"
    CONTAINER_NAME = ""
    container_client = None
    generator = None
    logger = None

    def __init__(self, conn_string_name, container_name, map_file_name="map.json"):
        """Creates a mapping object utilizing a SAS Token Connection string in the format provided by Azure Portal

        Args:
            conn_string_name (str): Name of environment variable containing connection string. Connection string must be in the format provided from Azure Portal i.e.:
                BlobEndpoint=https://<storage account name>.blob.core.windows.net/;QueueEndpoint=https://<storage account name>.queue.core.windows.net/;FileEndpoint=https://<storage account name>.file.core.windows.net/;TableEndpoint=https://<storage account name>.table.core.windows.net/;SharedAccessSignature=<SAS query string>
            container_name (str): Name of the container to be mapped
            map_file_name (str): File name for resultant storage map (default "map.json")
        """
        conn_string = os.environ[conn_string_name]
        self.container_client = ContainerClient.from_connection_string(
            conn_str=conn_string, container_name=container_name)
        self.CONTAINER_NAME = container_name
        self.generator = self.container_client.list_blobs()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.MAP_FILE_NAME = map_file_name
        self.logger.info("### Init complete")

    def _map_level(self, level, levels, blob_size, path):
        """Translates a blob's flat path into a tree-like representation recursively, adding the blob's metadata to one 'level' of the tree at a time

        Args:
            level (dict): level to add blob data
            levels (list): blob subpaths requiring additional translation
            blob_size (int): blob bytes
            path (str): absolute path of the blob

        Returns:
            dict: A dictionary filled with the provided blob's metadata at all sublevels
        """
        current_level = levels[0]
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
                level[current_level]['__Count__'] = 1
            else:  # No subpaths beneath this newly initialized map level; this is a leaf
                level[current_level]['__Path__'] = path
            # self.logger.info(f"### Level created for [{current_level}]")
        if len(levels) > 2:
            level[current_level]['__Contents__'] = self._map_level(
                level=level[current_level]['__Contents__'], levels=levels[1:], blob_size=blob_size, path=path)
        elif len(levels) > 1:
            level[current_level]['__Contents__'][levels[1]] = {
                '__Name__': levels[1], '__Size__': blob_size, '__Path__': path}
        return level

    def _map_root(self, level):
        """Maps the root level of a blob storage container after all sublevels have been mapped into a dictionary

        Args:
            level (dict): The blob's root level dictionary map

        Returns:
            dict: A dictionary filled with the provided blob's metadata at all sublevels
        """
        for content in level['__Contents__'].keys():
            if '__Count__' in level['__Contents__'][content].keys():
                level['__Count__'] += level['__Contents__'][content]['__Count__']
            else:
                level['__Count__'] += 1
            level['__Size__'] += level['__Contents__'][content]['__Size__']
        return level

    def map_container(self):
        """Creates a json tree representation of the blob storage container, removing the old one of the same name first if it exists

        Returns:
            dict: A json tree reflecting the contents of the provided blob storage container
        """
        today = datetime.now().strftime("%Y_%m")
        container_map = {'__Name__': 'root', '__Size__': 0,
                         '__Count__': 0, '__Contents__': {}, '__Date__': today}
        # self.logger.info("### Starting blob iteration")
        for blob in self.generator:
            container_map['__Contents__'] = self._map_level(
                level=container_map['__Contents__'], levels=blob.name.split("/"), blob_size=blob.size, path=blob.name)
        # self.logger.info(f"### Finished mapping all blobs! [{container_map}]")
        container_map = self._map_root(container_map)
        self.logger.info("### Finished mapping root!")
        return container_map

    def write_map_remote(self, map):
        """Creates json file from storage container map and writes it to the container directly. Overwrites existing file

        Args:
            map (dict): A json tree reflecting the contents of the provided blob storage container
        """
        json_content = json.dumps(map, sort_keys=True, indent=2)
        blob_client = self.container_client.get_blob_client(self.MAP_FILE_NAME)
        self.delete_map()
        blob_client.upload_blob(data=json_content)
        self.logger.info(f"Finished writing map to storage account {self.CONTAINER_NAME} at {self.MAP_FILE_NAME}")

    def write_map_local(self, map):
        """Creates a local copy of the storage container map

        Args:
            map (dict): A json tree reflecting the contents of the provided blob storage container
        """
        json_content = json.dumps(map, sort_keys=True, indent=2)
        json_file = open(self.MAP_FILE_NAME, "w")
        json_file.write(json_content)
        json_file.close()
        self.logger.info(f"Finished writing at {os.path.abspath(self.MAP_FILE_NAME)}")

    def delete_map(self):
        """Deletes the storage map from the blob storage container if it exists
        """
        try:
            self.logger.info(f"Attempting to delete {self.MAP_FILE_NAME}")
            blob_client = self.container_client.get_blob_client(self.MAP_FILE_NAME)
            if blob_client.exists():
                blob_client.delete_blob()
        except Exception as e:
            self.logger.warn(f"Failed to delete {self.MAP_FILE_NAME} before mapping container:\n{e}")
