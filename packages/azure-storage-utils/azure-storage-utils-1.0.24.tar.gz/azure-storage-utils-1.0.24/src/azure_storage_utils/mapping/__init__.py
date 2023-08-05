# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
from copy import error
import os
import json
import sys
from datetime import datetime
import logging

# Related third party imports
from azure.storage.blob import ContainerClient
from azure.storage.fileshare import ShareClient
from azure.core.exceptions import (
    ResourceNotFoundError,
)

TEMP_FOLDER = "/tmp"  # https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level#temporary-files
HOME_DIR = os.getcwd()
TEMP = f'{TEMP_FOLDER}/TEMP.txt'


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
        # self.logger.info(f"### Checking [{current_level}] in [{level.keys()}]")
        if current_level in level.keys():  # Level already exists in map from previous blob translation
            level[current_level]['__Size__'] += blob_size
            level[current_level]['__Count__'] += 1
        else:  # create level for the first time
            # self.logger.info(f"### Creating new level for [{current_level}]")
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
            # self.logger.info(f"### Mapping sublevel: [{levels[1]}]")"
            level[current_level]['__Contents__'] = self._map_level(
                level=level[current_level]['__Contents__'], levels=levels[1:], blob_size=blob_size, path=path)
        elif len(levels) > 1:
            # self.logger.info(f"### Mapping leaf: [{levels[1]}] in node [{level[current_level]}]")
            level[current_level]['__Contents__'][levels[1]] = {
                '__Name__': levels[1], '__Size__': blob_size, '__Path__': path}
        # self.logger.info(f"### Finished mapping level: [{current_level}]: [{level}]")
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


class FileShareMap:

    MAP_FILE_NAME = "map.json"
    file_share_client = None
    generator = None
    logger = None

    def __init__(self, conn_string_name, file_share_name, prefix):
        conn_string = os.environ[conn_string_name]
        self.file_share_client = ShareClient.from_connection_string(
            conn_str=conn_string, share_name=file_share_name)
        self.generator = self.file_share_client.list_directories_and_files()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.blob_prefix = prefix
        self.logger.info("### Init complete")

    def _map_directory(self, directory, absolute_paths, ):
        parent_directory = "/".join(absolute_paths)
        for obj in list(self.file_share_client.list_directories_and_files(parent_directory)):
            # self.logger.info(f"### Examining [{obj.name}] in parent directory [{parent_directory}]")
            absolute_path = parent_directory + "/" + obj.name
            if obj['is_directory'] is True:
                absolute_paths.append(obj.name)
                directory['__Contents__'][obj.name] = {
                    '__Name__': obj.name, '__Count__': 0, '__Size__': 0, '__Contents__': {}}
                directory['__Contents__'][obj.name] = self._map_directory(
                    directory=directory['__Contents__'][obj.name], absolute_paths=absolute_paths)
                directory['__Size__'] += directory['__Contents__'][obj.name]['__Size__']
                directory['__Count__'] += directory['__Contents__'][obj.name]['__Count__']
                # self.logger.info(f"### Mapped sublevel: \n{dir_map}")
                absolute_paths.pop()
            else:
                sfc = self.file_share_client.get_file_client(absolute_path)
                props = sfc.get_file_properties()
                directory['__Size__'] += props.size
                directory['__Count__'] += 1
                directory['__Contents__'][obj.name] = {
                    '__Name__': obj.name, '__Size__': props.size, '__Count__': 1, '__Path__': absolute_path}
            self.logger.info(
                f"### Finished working [{obj.name}] in parent directory [{parent_directory}]")
        self.logger.info(
            f"### Finished mapping directory: [{parent_directory}] with number of contents [{len(directory['__Contents__'].keys())}]")
        return directory

    def _map_root(self, level):
        for content in level['__Contents__'].keys():
            level['__Count__'] += level['__Contents__'][content]['__Count__']
            level['__Size__'] += level['__Contents__'][content]['__Size__']
        return level

    def map_file_share(self):
        self.delete_map()
        today = datetime.now().strftime("%Y_%m")
        file_share_map = {'__Name__': 'root', '__Size__': 0,
                          '__Count__': 0, '__Contents__': {}, '__Date__': today}
        file_share_map = {'__Name__': 'root', '__Size__': 0,
                          '__Count__': 0, '__Contents__': {}}
        file_share_map['__Contents__'] = self._map_directory(
            directory=file_share_map, absolute_paths=[])
        file_share_map = self._map_root(file_share_map)
        self.logger.info("### Finished mapping root!")
        return file_share_map

    def write_map(self, map):
        json_file = json.dumps(map, sort_keys=True, indent=2)
        file_client = self.file_share_client.get_file_client(
            self.MAP_FILE_NAME)
        self.delete_map()
        file_client.upload_file(data=json_file)

    def delete_map(self):
        map_file = self.file_share_client.get_file_client(self.MAP_FILE_NAME)
        try:
            props = map_file.get_file_properties()
            if props.size() > 0:
                map_file.delete_file()
        except ResourceNotFoundError as e:
            self.logger.warn(
                f"### Failed when pre-emptively deleting map file at {self.MAP_FILE_NAME}:\n{e}")


class MapComparator:

    MAP1 = {}
    MAP2 = {}
    DEPTH = 0
    PREFIX = ""

    def __init__(self, map1, map2, depth=sys.maxsize):
        self.MAP1 = map1
        self.MAP2 = map2
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.DEPTH = depth
        self.logger.info("### Init complete")

    def compare_map(self):
        """Creates a differential map based on two input maps"""
        diff_map = {}
        diff_map = self._compare_map_full(
            depth=self.DEPTH, map1=self.MAP1, map2=self.MAP2)
        return diff_map

    def _compare_map_full(self, depth, map1, map2):
        diff_level = None
        next_depth = depth - 1
        try:
            if map1 is None or len(map1.keys()) == 0:
                map1 = {'__Name__': '__None__',
                        '__Size__': 0, '__Path__': '__None__'}
            if map2 is None or len(map1.keys()) == 0:
                map2 = {'__Name__': '__None__',
                        '__Size__': 0, '__Path__': '__None__'}
            if map1 != map2:  # maps do not match
                diff_level = {'__Name__': map1['__Name__'], '__Size__': (
                    map1['__Size__'] - map2['__Size__'])}
                if '__Path__' in map1.keys() and '__Path__' in map2.keys():
                    # both are leaves
                    pass
                elif '__Count__' in map1.keys() and '__Count__' in map2.keys():  # both maps are branches
                    diff_level['__Count__'] = map1['__Count__'] - \
                        map2['__Count__']
                    if next_depth > 0:  # Should continue comparing deeper?
                        # Collect keys
                        map1_content_keys_set = set(
                            map1['__Contents__'].keys())
                        map2_content_keys_set = set(
                            map2['__Contents__'].keys())
                        unique_keys_map1 = set(
                            map1_content_keys_set) - set(map2_content_keys_set)
                        unique_keys_map2 = set(
                            map2_content_keys_set) - set(map1_content_keys_set)
                        shared_map_keys_set = set(map1['__Contents__'].keys()).intersection(
                            map2['__Contents__'].keys())
                        diff_level['__Contents__'] = {}
                        new_subcontent_diff = None
                        # Find all unique subcontents in both
                        self._compare_map_volume_subcontent(
                            keys=unique_keys_map1, storage_map=map1, diff_map=diff_level, next_depth=next_depth, map1_primary=True)
                        self._compare_map_volume_subcontent(
                            keys=unique_keys_map2, storage_map=map2, diff_map=diff_level, next_depth=next_depth, map1_primary=False)
                        # Find all shared subcontents in both
                        for subcontent in shared_map_keys_set:
                            subcontent_map1 = map1['__Contents__'][subcontent]
                            subcontent_map2 = map2['__Contents__'][subcontent]
                            subcontent_diff_map = self._compare_map_full(
                                depth=next_depth, map1=subcontent_map1, map2=subcontent_map2)
                            if new_subcontent_diff is not None:
                                diff_level['__Contents__'][subcontent] = subcontent_diff_map
                # Only map1 is branch
                elif '__Count__' in map1.keys() and '__Path__' in map2.keys():
                    # subtract single file value of map2, check subcontents
                    diff_level['__Count__'] = map1['__Count__'] - 1
                    if next_depth > 0:
                        diff_level['__Contents__'] = {}
                        unique_keys_map1 = map1['__Contents__'].keys()
                        self._compare_map_volume_subcontent(
                            keys=unique_keys_map1, storage_map=map1, diff_map=diff_level, next_depth=next_depth, map1_primary=True)
                # Only map2 is branch
                elif '__Count__' in map2.keys() and '__Path__' in map1.keys():
                    # subtract single file value of map1
                    diff_level['__Count__'] = map2['__Count__'] - 1
                    if next_depth > 0:
                        diff_level['__Contents__'] = {}
                        unique_keys_map2 = map2['__Contents__'].keys()
                        self._compare_map_volume_subcontent(
                            keys=unique_keys_map2, storage_map=map2, diff_map=diff_level, next_depth=next_depth, map1_primary=False)
                else:
                    raise AttributeError(
                        f"Failed to compare two maps:\n{map1}\n\n{map2}\n{error}")
        except Exception as e:
            self.logger.exception(
                f"Failed at depth [{depth}] while comparing:\n{map1}\n\n{map2}\n\n{e}")
        return diff_level

    def _compare_map_volume_subcontent(self, keys, storage_map, diff_map, next_depth, map1_primary):
        for subcontent in keys:  # iterate through unique subcontents
            subcontent_map = storage_map['__Contents__'][subcontent]
            new_subcontent_diff = None
            if (map1_primary):
                new_subcontent_diff = self._compare_map_full(
                    depth=next_depth, map1=subcontent_map, map2=None)
            else:
                new_subcontent_diff = self._compare_map_full(
                    depth=next_depth, map1=None, map2=subcontent_map)
            if new_subcontent_diff is not None:
                diff_map['__Contents__'][subcontent] = new_subcontent_diff


class MapReporter:

    logger = None
    STORAGE_MAP = None
    DEPTH = 0
    PREFIX = ""
    OUTPUT_FILE_NAME = "map.cvs"

    def __init__(self, storage_map, depth=sys.maxsize, prefix="", output_file_name="map.csv"):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.STORAGE_MAP = storage_map
        self.DEPTH = depth
        self.PREFIX = prefix.replace('\\', '/')
        self.OUTPUT_FILE_NAME = output_file_name
        self.logger.info(
            f"### Init complete for map with depth: [{self.DEPTH}]")

    def _start_at_prefix(self):
        prefix_list = self.PREFIX.split('/')
        try:
            for prefix in prefix_list:
                self.STORAGE_MAP = self.STORAGE_MAP['__Contents__'][prefix]
        except Exception as e:
            self.logger.exception(
                f"Failed to access storage map using prefix: {self.PREFIX} at level {prefix}:", f"\n{self.STORAGE_MAP}",
                f"\n{e}")

    def _map_branches(self, map_level, depth=0):
        header_string = ""
        info_string = ""
        self.logger.info(f"### Working depth {depth}: {map_level['__Name__']}")
        if '__Contents__' in map_level:
            for content in map_level['__Contents__']:
                try:
                    if depth > 0 and '__Contents__' in map_level['__Contents__'][content].keys():
                        self.logger.info("### Proceeding to next level...")
                        [lower_header_string, lower_info_string] = self._map_branches(
                            map_level=map_level['__Contents__'][content], depth=(depth-1))
                        header_string += lower_header_string
                        info_string += lower_info_string
                    elif '__Path__' in map_level['__Contents__'][content].keys():
                        self.logger.info(f"### Acquiring leaf: {content}")
                        header_string += f"{content} Bytes,"
                        info_string += f"{map_level['__Contents__'][content]['__Size__']},"
                    else:
                        self.logger.info(
                            f"### Acquiring final node: {content}")
                        header_string += f"{content} Blobs, {content} Bytes,"
                        info_string += f"{map_level['__Contents__'][content]['__Count__']}, {map_level['__Contents__'][content]['__Size__']},"
                except KeyError as ke:
                    self.logger.warning(
                        f"Failed when trying to find key in \n{map_level.keys()}\n for content [{content}]:\n {ke} ")
        else:
            header_string += f"{map_level['__Name__']} Blobs, {map_level['__Name__']} Bytes,"
            info_string += f"{map_level['__Count__']}, {map_level['__Size__']},"
        self.logger.info(f"### Returning: \n{header_string}\n{info_string}")
        return [header_string, info_string]

    def create_csv(self):
        """Returns formatted text meant to be stored in a csv file"""
        self.logger.info("### Creating csv...")
        today = datetime.now().strftime("%m-%Y")
        csv_data = (f"Month, Total Bytes, Total Blobs\n{today}, {self.STORAGE_MAP['__Count__']}, {self.STORAGE_MAP['__Size__']}\n\n")
        if len(self.PREFIX) > 0:
            self._start_at_prefix()
        [content_headers, content_info] = self._map_branches(
            self.STORAGE_MAP, self.DEPTH)
        csv_data += f"\n{content_headers}\n{content_info}"
        self.logger.info("Successfully created csv")
        return csv_data

    def write_csv_local(self):
        self.logger.info(f"Writing csv to {self.OUTPUT_FILE_NAME}")
        csv_data = self.create_csv()
        file = open(self.OUTPUT_FILE_NAME, "w")
        file.write(csv_data)
        file.close()
        self.logger.info(f"Finished writing at {os.path.abspath(self.OUTPUT_FILE_NAME)}")
