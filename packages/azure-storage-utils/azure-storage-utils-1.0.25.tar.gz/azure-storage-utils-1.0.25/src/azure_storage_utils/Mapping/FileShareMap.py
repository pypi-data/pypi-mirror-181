# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import os
import json
from datetime import datetime
import logging

# Related third party imports
from azure.storage.fileshare import ShareClient
from azure.core.exceptions import (
    ResourceNotFoundError,
)


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
