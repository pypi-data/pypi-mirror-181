# -*- coding: future_fstrings -*-
""" A utility for ensuring consistent use and formatting of connection strings across multiple objects.

    Connection strings come in many formats across Azure. The format intended for use across
    azure-storage-utils conforms to the format used in this documentation:
    https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string#connect-to-the-emulator-account-using-the-shortcut
"""
from __future__ import print_function
# Standard library imports
import time

# Related third party imports

CONN_STRING_SAMPLE = "<BlobEndpoint=https://contosostorageaccount.blob.core.windows.net/;QueueEndpoint=https: "\
    + "//contosostorageaccount.queue.core.windows.net/;FileEndpoint=https://contosostorageaccount.file." \
    + "core.windows.net/;TableEndpoint=https://contosostorageaccount.table.core.windows.net/;" \
    + "SharedAccessSignature=sv=...>"


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
                try:
                    storage_url_container = storage_url[storage_url.rindex(
                        '.net/'):]
                    storage_url = storage_url[0:storage_url.index(
                        storage_url_container)] + ".net"
                    logger.info(
                        f"Removed {storage_url_container} from {storage_url} when recreating connection string")
                except Exception as e:
                    logger.info(
                        f"Could not find blob container name in storage url, this is likely normal \n{e}")
                if 'sv=' in conn_str:
                    token = conn_str[conn_str.index('sv='):]
                conn_str = f"BlobEndPoint={storage_url};QueueEndPoint={storage_url.replace('.blob.', '.queue.')}" \
                    + f";FileEndPoint={storage_url.replace('.blob.', '.file.')};TableEndPoint=" \
                    + f"{storage_url.replace('.blob.', '.table.')};SharedAccessSignature="
                logger.warning(
                    "Detected an invalid connection string not matching the format:\n",
                    CONN_STRING_SAMPLE,
                    "Attempting to reconstruct connection string starting with:\n",
                    f"{conn_str}...")
                conn_str = conn_str + token
                time.sleep(10)
                break
        return conn_str
