# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import sys
import logging
from os import error

# Related third party imports


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
