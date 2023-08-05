# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import os
import sys
from datetime import datetime
import logging

# Related third party imports


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
