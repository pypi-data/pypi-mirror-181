# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import os
import sys
from datetime import datetime
import logging

# Related third party imports


# TAGS
__author__ = "Matthew Warren"
__version__ = "1.0.0"
__maintainer__ = ["Matthew Warren"]
__email__ = "mawarren@microsoft.com"
__status__ = "Release"


class MapReporter:
    """Create a CSV file reporting the contents of a storage map"""

    def __init__(self, storage_map, depth=sys.maxsize, prefix="", output_file_name="map.csv"):
        """__init__ Create a CSV file reporting the contents of a storage map

        :param storage_map: The map to report to CSV that should conform to the format:
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :type storage_map: dict
        :param depth: The lowest level from which to return specific data, defaults to sys.maxsize
        :type depth: int, optional
        :param prefix: the file path at which to begin reporting, defaults to ""
        :type prefix: str, optional
        :param output_file_name: name to use when saving output file, defaults to "map.csv"
        :type output_file_name: str, optional
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.storage_map = storage_map
        self.depth = depth
        self.prefix = prefix.replace('\\', '/')
        self.output_file_name = output_file_name
        self.logger.info(
            f"### Init complete for map with depth: [{self.depth}]")

    def _start_at_prefix(self):
        prefix_list = self.prefix.split('/')
        current_prefix = ""
        try:
            for prefix in prefix_list:
                current_prefix = prefix
                self.storage_map = self.storage_map['__Contents__'][prefix]
        except Exception as e:
            self.logger.exception(
                f"Failed to access storage map using prefix: {self.prefix} at level {current_prefix}:"
                + f"\n{self.storage_map}"
                + f"\n{e}")

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
                        info_string += f"{map_level['__Contents__'][content]['__Count__']}," \
                            + f"{map_level['__Contents__'][content]['__Size__']},"
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
        csv_data = f"Month, Total Bytes, Total Blobs\n{today}, {self.storage_map['__Count__']}," + \
            f" {self.storage_map['__Size__']}\n\n"
        if len(self.prefix) > 0:
            self._start_at_prefix()
        [content_headers, content_info] = self._map_branches(
            self.storage_map, self.depth)
        csv_data += f"\n{content_headers}\n{content_info}"
        self.logger.info("Successfully created csv")
        return csv_data

    def write_csv_local(self):
        self.logger.info(f"Writing csv to {self.output_file_name}")
        csv_data = self.create_csv()
        output_file = open(self.output_file_name, "w")
        output_file.write(csv_data)
        output_file.close()
        self.logger.info(
            f"Finished writing at {os.path.abspath(self.output_file_name)}")
