# azure-storage-utils

Azure Storage Utilities performs several linked functions for azure storage accounts:

1. It enables translation of the flat storage format of blobs to the hierarchical format human users expect when navigating through storage accounts in the Azure Web Portal or Azure Storage Explorer application. This translated hierarchical storage is returned as a dictionary that can be saved locally or written back to the storage container.

2. It compares hierarchical maps of storage containers to produce a differential map that tracks gains and losses in file count and byte size, or the overall difference between two maps.