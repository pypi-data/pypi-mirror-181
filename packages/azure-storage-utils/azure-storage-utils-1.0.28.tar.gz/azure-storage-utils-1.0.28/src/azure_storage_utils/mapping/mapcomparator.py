# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import sys
import logging
from os import error

# Related third party imports


# TAGS
__author__ = "Matthew Warren"
__version__ = "1.0.0"
__maintainer__ = ["Matthew Warren"]
__email__ = "mawarren@microsoft.com"
__status__ = "Release"


class MapComparator:
    """ Compares two storage maps, creating a differential map to distinguish the two

    Recursively checks levels of two different storage maps (dictionaries) to determine what
    differences exist in byte count and file count at each level. The maps are presumed to
    have the following schema:
    control fields for all nodes: ['__Name__', '__Size__'];
    control fields for branches: ['__Contents__', '__Count__'];
    control fields for leaves: ['__Path__']

    """

    def __init__(self, map1, map2, depth=sys.maxsize):
        self.map1 = map1
        self.map2 = map2
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.depth = depth
        self.logger.info("### Init complete")

    def compare_map(self):
        """Creates a differential map based on two input maps"""
        diff_map = {}
        diff_map = self._compare_map_full(
            depth=self.depth, map1=self.map1, map2=self.map2)
        return diff_map

    def _compare_map_full(self, depth, map1, map2):
        """_compare_map_full Compares all tags for both storage maps without short circuiting for size and count

        Recursively checks two maps (dictionaries) of storage containers to compare their contents and create
        a differential map between the two. The resultant map will show gains and losses in byte count and file
        size as well as the differences in file contents up to the depth specified.

        :param depth: The number of map levels to fully check
        :type depth: int
        :param map1: Primary storage map for comparison
        :type map1: dict
        :param map2: Secondary storage map for comparison
        :type map2: dict
        :raises AttributeError: The two map nodes being compared do not have the expected control fields
        :return: A differential map showing the contents between the two storages
        :rtype: dict
        """
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
                            keys=unique_keys_map1, storage_map=map1, diff_map=diff_level, next_depth=next_depth,
                            map1_primary=True)
                        self._compare_map_volume_subcontent(
                            keys=unique_keys_map2, storage_map=map2, diff_map=diff_level, next_depth=next_depth,
                            map1_primary=False)
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
                            keys=unique_keys_map1, storage_map=map1, diff_map=diff_level, next_depth=next_depth,
                            map1_primary=True)
                # Only map2 is branch
                elif '__Count__' in map2.keys() and '__Path__' in map1.keys():
                    # subtract single file value of map1
                    diff_level['__Count__'] = map2['__Count__'] - 1
                    if next_depth > 0:
                        diff_level['__Contents__'] = {}
                        unique_keys_map2 = map2['__Contents__'].keys()
                        self._compare_map_volume_subcontent(
                            keys=unique_keys_map2, storage_map=map2, diff_map=diff_level, next_depth=next_depth,
                            map1_primary=False)
                else:
                    raise AttributeError(
                        f"Failed to compare two maps:\n{map1}\n\n{map2}\n{error}")
        except Exception as e:
            self.logger.exception(
                f"Failed at depth [{depth}] while comparing:\n{map1}\n\n{map2}\n\n{e}")
        return diff_level

    def _compare_map_volume_subcontent(self, keys, storage_map, diff_map, next_depth, map1_primary):
        """_compare_map_volume_subcontent Compares the volume of map node subcontents

        :param keys: names of all subcontents in this dict of subcontents
        :type keys: list
        :param storage_map: dictionary of all storage contents conforming to the following structure:
            control fields for all nodes: ['__Name__', '__Size__'];
            control fields for branches: ['__Contents__', '__Count__'];
            control fields for leaves: ['__Path__']
        :type storage_map: dict
        :param diff_map: the resultant differential map being created
        :type diff_map: dict
        :param next_depth: The depth remaining to check after the current level
        :type next_depth: int
        :param map1_primary: Whether or not map1 is the primary map in this comparison
        :type map1_primary: bool
        """
        for subcontent in keys:  # iterate through unique subcontents
            subcontent_map = storage_map['__Contents__'][subcontent]
            if (map1_primary):
                new_subcontent_diff = self._compare_map_full(
                    depth=next_depth, map1=subcontent_map, map2=None)
            else:
                new_subcontent_diff = self._compare_map_full(
                    depth=next_depth, map1=None, map2=subcontent_map)
            if new_subcontent_diff is not None:
                diff_map['__Contents__'][subcontent] = new_subcontent_diff
