# pytest
# Test from testpypi
#   flit publish --repository testpypi
#   testenv/Scripts/activate
#   pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple cloudzipfile
#   python -m "G:\Other\Python Packages\cloudzipfile\tests\test_azure.py"
# If satisfied:
#   flit publish --repository pypi
# DEBUG: tmpdir = 'data'
from cloudzipfile.cloudzipfile import CloudZipFile
from azure.storage.blob import BlobClient
import os

def test_extractall(tmpdir):
    # Define blob client
    BLOB_URL = 'https://cloudzipfileexamples.blob.core.windows.net/test/files.zip'
    blobClient = BlobClient.from_blob_url(BLOB_URL)

    # Extract specific files
    PATH_OUTPUT = tmpdir
    FILES_DESIRED = ['file1.txt', 'file4.txt']
    cloudZipFile = CloudZipFile(blobClient)
    cloudZipFile.extractall(path=PATH_OUTPUT, members=FILES_DESIRED)

    assert all((file in os.listdir(PATH_OUTPUT) for file in FILES_DESIRED))

if __name__ == '__main__':
    import tempfile
    import uuid
    dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    test_extractall(dir)
    print(f'{dir}: {os.listdir(dir)}')