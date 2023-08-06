# -*- coding: future_fstrings -*-
""" Runs metrics collections on azure blob storage automatically in a pipeline

    Example usage:
    pipelineoperator.py --conn_str $conn_str --storage_url $storage_url --container_name $container_name
    --map_name $map_name --publish_metrics $True
"""
from __future__ import print_function
# Standard library imports
import logging
from datetime import datetime
import os
import argparse

# Related third party imports
from azure.storage.blob import ContainerClient

# Local application/library specific imports
from mapping.containermap import ContainerMap
from mapping.mapreporter import MapReporter
from auth.connectionstringutil import ConnectionStringUtil

# TAGS
__author__ = "Matthew Warren"
__version__ = "1.0.0"
__maintainer__ = ["Matthew Warren"]
__email__ = "mawarren@microsoft.com"
__status__ = "Release"


# GLOBALS

CONN_STRING_SAMPLE = "<BlobEndpoint=https://contosostorageaccount.blob.core.windows.net/;QueueEndpoint=https:",
"//contosostorageaccount.queue.core.windows.net/;FileEndpoint=https://contosostorageaccount.file.",
"core.windows.net/;TableEndpoint=https://contosostorageaccount.table.core.windows.net/;",
"SharedAccessSignature=sv=...>"


class PipelineOperator:
    """Runs automated process in a pipeline to collect metrics information"""

    CONNECTION_STRING_NAME = 'STORAGE_CONNECTION_STRING'

    def __init__(self, conn_str, storage_url, container_name,
                 map_file_name=f"storage_map_{datetime.now().strftime('%Y_%m')}.json"):
        """__init__ Creates a pipeline operator object similar to the init from scipt with argparse

        :param conn_str: Connection string used to authenticate into Azure. Must be in format:
            https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string
            #configure-a-connection-string-for-an-azure-storage-account
        :type conn_str: str
        :param storage_url: URL of storage account
        :type storage_url: str
        :param container_name: Name of blob storage container
        :type container_name: str
        :param map_file_name: File name for .json output, defaults to
            f"storage_map_{datetime.now().strftime('%Y_%m')}.json"
        :type map_file_name: str, optional
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.output_name_json = map_file_name
        if '.json' not in self.output_name_json:
            self.output_name_json += ".json"
        self.output_name_csv = map_file_name.replace('json', 'csv')
        self.container_name = container_name
        conn_str = ConnectionStringUtil.check_conn_str(self.logger,
                                                       conn_str=conn_str, storage_url=storage_url)
        os.environ[self.CONNECTION_STRING_NAME] = conn_str
        self.logger.info(
            f"### Init complete for {storage_url}, preparing auth...")

    def collect_pipeline_data(self):
        container_mapper = ContainerMap(conn_string_name=self.CONNECTION_STRING_NAME,
                                        container_name=self.container_name, map_file_name=self.output_name_json)
        storage_map = container_mapper.map_container()
        container_mapper.write_map_local(storage_map)
        map_reporter = MapReporter(
            storage_map=storage_map, depth=2, output_file_name=self.output_name_csv)
        map_reporter.write_csv_local()

    def submit_pipeline_data(self):
        conn_string = os.environ[self.CONNECTION_STRING_NAME]
        container_client = ContainerClient.from_connection_string(
            conn_str=conn_string, container_name=self.container_name)
        for file_name in [self.output_name_csv, self.output_name_json]:
            with open(file_name, 'r') as file:
                file_contents = file.read()
                blob_client = container_client.get_blob_client(file_name)
                blob_client.upload_blob(file_contents)


if __name__ == '__main__':
    """Initializes a pipeline operator to collect storage account metadata from the specified container"""
    parser = argparse.ArgumentParser()
    conn_str_help = "Azure Storage Container connection string in the format:", "\n", \
                    CONN_STRING_SAMPLE
    parser.add_argument('--conn_str', type=str,
                        required=True, help=conn_str_help)
    parser.add_argument('--storage_url', type=str, required=True,
                        help="URL for the blob storage container specified")
    parser.add_argument('--container_name', type=str, required=True)
    parser.add_argument('--map_name', type=str, required=False,
                        default=f"storage_map_{datetime.now().strftime('%Y_%m')}.json")
    parser.add_argument('--publish_metrics', default=False, action='store_true',
                        help="Whether or not to publish metrics generated to the storage container specified in args")
    parser.add_argument('--generate_metrics', default=True, action='store_true',
                        help="Whether or not to generate new metrics files using provided filenames")
    args = parser.parse_args()
    pipeline_operator = PipelineOperator(conn_str=args.conn_str, storage_url=args.storage_url,
                                         container_name=args.container_name, map_file_name=args.map_name)
    if args.generate_metrics:
        pipeline_operator.collect_pipeline_data()
    if args.publish_metrics:
        pipeline_operator.submit_pipeline_data()
