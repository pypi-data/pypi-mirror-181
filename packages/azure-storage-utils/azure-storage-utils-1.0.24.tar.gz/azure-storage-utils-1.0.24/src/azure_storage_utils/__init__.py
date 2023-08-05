# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import logging
import argparse
from datetime import datetime
import os
import time

# Related third party imports

# Local application/library specific imports
from azure_storage_utils.mapping import ContainerMap
from azure_storage_utils.mapping import MapReporter


class PipelineOperator:

    logger = None
    OUTPUT_NAME_CSV = ""
    OUTPUT_NAME_JSON = ""
    CONTAINTER_NAME = ""
    CONNECTION_STRING_NAME = 'STORAGE_CONNECTION_STRING'
    STORAGE_MAP = None

    def __init__(self, conn_str, storage_url, container_name, map_file_name=f"storage_map_{datetime.now().strftime('%Y_%m')}.json"):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.OUTPUT_NAME_JSON = map_file_name
        if '.json' not in self.OUTPUT_NAME_JSON:
            self.OUTPUT_NAME_JSON += ".json"
        self.OUTPUT_NAME_CSV = map_file_name.replace('json', 'csv')
        self.CONTAINTER_NAME = container_name
        conn_str = self._check_conn_str(
            conn_str=conn_str, storage_url=storage_url)
        os.environ[self.CONNECTION_STRING_NAME] = conn_str
        self.logger.info(
            f"### Init complete for {storage_url}, preparing auth...")

    def collect_pipeline_data(self):
        container_mapper = ContainerMap(conn_string_name=self.CONNECTION_STRING_NAME,
                                        container_name=self.CONTAINTER_NAME, map_file_name=self.OUTPUT_NAME_JSON)
        storage_map = container_mapper.map_container()
        container_mapper.write_map_local(storage_map)
        map_reporter = MapReporter(
            storage_map=storage_map, depth=2, output_file_name=self.OUTPUT_NAME_CSV)
        map_reporter.write_csv_local()

    def submit_pipeline_data(self):
        from azure.storage.blob import ContainerClient
        conn_string = os.environ[self.CONNECTION_STRING_NAME]
        container_client = ContainerClient.from_connection_string(
            conn_str=conn_string, container_name=self.CONTAINTER_NAME)
        for file_name in [self.OUTPUT_NAME_CSV, self.OUTPUT_NAME_JSON]:
            with open(file_name, 'r') as file:
                file_contents = file.read()
                blob_client = container_client.get_blob_client(file_name)
                blob_client.upload_blob(file_contents)

    def _check_conn_str(self, conn_str, storage_url):
        for kw in ['BlobEndpoint', 'QueueEndpoint', 'TableEndPoint', 'FileEndPoint', 'SharedAccessSignature', 'sv']:
            if kw not in conn_str:
                token = ""
                try:
                    storage_url_container = storage_url[storage_url.rindex('.net/'):]
                    storage_url = storage_url[0:storage_url.index(storage_url_container)] + ".net"
                    self.logger.info(f"Removed {storage_url_container} from {storage_url} when recreating connection string")
                except Exception as e:
                    self.logger.info(f"Could not find blob container name in storage url, this is likely normal \n{e}")
                if 'sv=' in conn_str:
                    token = conn_str[conn_str.index('sv='):]
                conn_str = f"BlobEndPoint={storage_url};QueueEndPoint={storage_url.replace('.blob.', '.queue.')};FileEndPoint={storage_url.replace('.blob.', '.file.')};TableEndPoint={storage_url.replace('.blob.', '.table.')};SharedAccessSignature="
                self.logger.warning(
                    f"Detected an invalid connection string not matching the format:\n" +
                    f"<BlobEndpoint=https://contosostorageaccount.blob.core.windows.net/;QueueEndpoint=https://contosostorageaccount.queue.core.windows.net/;FileEndpoint=https://contosostorageaccount.file.core.windows.net/;TableEndpoint=https://contosostorageaccount.table.core.windows.net/;SharedAccessSignature=sv=...>" +
                    f"\nAttempting to reconstruct connection string starting with:\n" +
                    f"{conn_str}...")
                conn_str += token
                time.sleep(10)
                break
        return conn_str


if __name__ == '__main__':
    """Initializes a pipeline operator to collect storage account metadata from the specified container.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--conn_str', type=str, required=True, help="Azure Storage Container connection string in the format: <BlobEndpoint=https://contosostorageaccount.blob.core.windows.net/;QueueEndpoint=https://contosostorageaccount.queue.core.windows.net/;FileEndpoint=https://contosostorageaccount.file.core.windows.net/;TableEndpoint=https://contosostorageaccount.table.core.windows.net/;SharedAccessSignature=sv=...>")
    parser.add_argument('--storage_url', type=str, required=True, help="URL for the blob storage container specified")
    parser.add_argument('--container_name', type=str, required=True)
    parser.add_argument('--map_name', type=str, required=False,
                        default=f"storage_map_{datetime.now().strftime('%Y_%m')}.json")
    parser.add_argument('--publish_metrics', type=bool, default=False, action='store_true',
                        help="Whether or not to publish metrics generated to the storage container specified in args")
    parser.add_argument('--generate_metrics', type=bool, default=True, action='store_true', help="Whether or not to generate new metrics files using provided filenames")
    args = parser.parse_args()
    pipeline_operator = PipelineOperator(conn_str=args.conn_str, storage_url=args.storage_url,
                                         container_name=args.container_name, map_file_name=args.map_name)
    if args.generate_metrics:
        pipeline_operator.collect_pipeline_data()
    if args.publish_metrics:
        pipeline_operator.submit_pipeline_data()
