# -*- coding: future_fstrings -*-
""" A utility for ensuring consistent use and formatting of connection strings across multiple objects.

    Connection strings come in many formats across Azure. The format intended for use across
    azure-storage-utils conforms to the format used in this documentation:
    https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string#connect-to-the-emulator-account-using-the-shortcut
"""
from __future__ import print_function
# Standard library imports
import time
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Related third party imports

CONN_STRING_SAMPLE = 'BlobEndpoint=https://contosostorageaccount.blob.core.windows.net/;QueueEndpoint=https: ' \
    + '//contosostorageaccount.queue.core.windows.net/;FileEndpoint=https://contosostorageaccount.file.' \
    + 'core.windows.net/;TableEndpoint=https://contosostorageaccount.table.core.windows.net/;' \
    + 'SharedAccessSignature=sv=...'


class ConnectionStringUtil:

    @staticmethod
    def check_conn_str(logger, conn_str, storage_url):
        """check_conn_str Ensures that the correct storage connection string format is used

        Checks for various data points in a supplied connection string and reformats it if necessary.
        This is guaranteed to take the commonly used shorter blob storage connection string and
        enable it to work with fileshares, tables, and queues.

        :param logger: Logger to use for output
        :type logger: logger
        :param conn_str: Connection string to check and reformat as necessary
        :type conn_str: str
        :param storage_url: Azure storage account endpoint
        :type storage_url: str
        :return: Proper connection string in the format used here:
            https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string#connect-to-the-emulator-account-using-the-shortcut
        :rtype: str
        """
        for kw in ['BlobEndpoint', 'QueueEndpoint', 'TableEndpoint', 'FileEndpoint', 'SharedAccessSignature', 'sv']:
            if kw not in conn_str:
                token = ""
                try:  # Fix storage_url
                    uri_parts = urlparse(storage_url)
                    storage_url_rebuilt = f"{uri_parts.scheme}://{uri_parts.netloc}"
                    storage_url_container = uri_parts.path
                    logger.info(
                        f"Rebuilding url storage with {storage_url_rebuilt} as base")
                    for storage_type in ['.table.', '.queue.', '.file.']:
                        if storage_type in storage_url_rebuilt:
                            storage_url_rebuilt = storage_url_rebuilt.replace(
                                storage_type, '.blob.')
                            break
                    if '.blob.' not in storage_url_rebuilt:
                        if '.core.windows.' in uri_parts.netloc:
                            storage_url_rebuilt = storage_url_rebuilt.replace(
                                '.core.windows.', '.blob.core.windows.')
                        else:
                            logger.warning("Encountered an unexpected storage url format when trying to fix"
                                           + "connection string storage url")
                    if len(storage_url_container) > 0:
                        logger.info(f"Removed {storage_url_container} from {storage_url} when recreating connection"
                                    + f"string \nusing {storage_url_rebuilt} instead")
                except Exception as e:
                    logger.info(
                        "Could not find blob container name in storage url, this is likely normal")
                    if e is not None:
                        logger.info(e)
                if 'sv=' in conn_str:
                    token = conn_str[conn_str.index('sv='):]
                else:
                    logger.exception(
                        "Storage Services tag ('sv=') not found in provided connection string token!")
                conn_str = f"BlobEndPoint={storage_url};QueueEndPoint={storage_url.replace('.blob.', '.queue.')}" \
                    + f";FileEndPoint={storage_url.replace('.blob.', '.file.')};TableEndPoint=" \
                    + f"{storage_url.replace('.blob.', '.table.')};SharedAccessSignature="
                logger.warning(
                    "Detected an invalid connection string not matching the format:\n"
                    + CONN_STRING_SAMPLE
                    + "Attempting to reconstruct connection string starting with:\n"
                    + f"{conn_str}...")
                conn_str = conn_str + token
                time.sleep(10)
                break
        return conn_str
