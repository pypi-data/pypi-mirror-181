''' Provides the abstracted methods for each supported cloud client '''
from azure.storage.blob import BlobClient
import io

class AzureClient:
    def __init__(self, blobClient: BlobClient):
        self.blobClient = blobClient

    def getSize(self):
        return self.blobClient.get_blob_properties()['size']

    def partialDownloadToBuffer(self, offset, length, max_concurrency=8):
        return io.BytesIO(self.blobClient.download_blob(offset=offset, length=length, max_concurrency=max_concurrency).readall())