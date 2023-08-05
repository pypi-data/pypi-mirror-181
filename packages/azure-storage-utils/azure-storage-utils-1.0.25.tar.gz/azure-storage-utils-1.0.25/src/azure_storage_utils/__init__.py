#!/usr/bin/env python3
# -*- coding: future_fstrings -*-
from __future__ import print_function
# Standard library imports
import argparse
from datetime import datetime

# Related third party imports

# Local application/library specific imports
from PipelineOperator import PipelineOperator


if __name__ == '__main__':
    """Initializes a pipeline operator to collect storage account metadata from the specified container.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--conn_str', type=str, required=True, help="Azure Storage Container connection string in the format: <BlobEndpoint=https://contosostorageaccount.blob.core.windows.net/;QueueEndpoint=https://contosostorageaccount.queue.core.windows.net/;FileEndpoint=https://contosostorageaccount.file.core.windows.net/;TableEndpoint=https://contosostorageaccount.table.core.windows.net/;SharedAccessSignature=sv=...>")
    parser.add_argument('--storage_url', type=str, required=True, help="URL for the blob storage container specified")
    parser.add_argument('--container_name', type=str, required=True)
    parser.add_argument('--map_name', type=str, required=False,
                        default=f"storage_map_{datetime.now().strftime('%Y_%m')}.json")
    parser.add_argument('--publish_metrics', default=False, action='store_true',
                        help="Whether or not to publish metrics generated to the storage container specified in args")
    parser.add_argument('--generate_metrics', default=True, action='store_true', help="Whether or not to generate new metrics files using provided filenames")
    args = parser.parse_args()
    pipeline_operator = PipelineOperator(conn_str=args.conn_str, storage_url=args.storage_url,
                                         container_name=args.container_name, map_file_name=args.map_name)
    if args.generate_metrics:
        pipeline_operator.collect_pipeline_data()
    if args.publish_metrics:
        pipeline_operator.submit_pipeline_data()
