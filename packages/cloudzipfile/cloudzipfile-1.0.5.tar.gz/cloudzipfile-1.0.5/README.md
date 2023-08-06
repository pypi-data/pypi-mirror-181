# cloudzipfile
This module provides a way to access zipfiles in cloud storage without downloading the entire zip file. 
It is inspired by [remotezip](https://github.com/gtsystem/python-remotezip), but leverages the respective cloud APIs rather than requiring support for the [range header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests).
It currently only supports Azure, porting it to other systems should be fairly simple, pull requests very welcome!

## Installation
```
pip install cloudzipfile
```

## Usage
cloudzipfile is a subclass of Python's standard library [zipfile.Zipfile](https://docs.python.org/3/library/zipfile.html) and thus supports all its read methods. 

Instead of providing Zipfile with a path, you provide a blob client of your cloud provider, for example:
```
# Import
from azure.storage.blob import BlobClient
from cloudzipfile.cloudzipfile import CloudZipFile
import os, tempfile, uuid

# Define blob client
BLOB_URL = 'https://cloudzipfileexamples.blob.core.windows.net/test/files.zip'
blobClient = BlobClient.from_blob_url(BLOB_URL)

# Define link to zipfile
# Will download central directory (where to find specific files)
PATH_OUTPUT = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
FILES_DESIRED = ['file1.txt', 'file3.txt']
cloudZipFile = CloudZipFile(blobClient)

# Extract specific files
cloudZipFile.extractall(path=PATH_OUTPUT, members=FILES_DESIRED)

# Verify success: should show file1.txt and file2.txt
print(f'{PATH_OUTPUT}: {os.listdir(PATH_OUTPUT)}')

```

## Future Development
Supporting other systems is fairly straightforward as you require only two methods. One that determines the size of the cloud file and one that performs a partial download, these should be supported by all major providers (I simply don't have experience with them).

## How It Works
Zip files have a fixed structure, which can be leveraged for partial reading. They end with an [EOCD](https://en.wikipedia.org/wiki/ZIP_(file_format)#End_of_central_directory_record_(EOCD)) which lists where to find the central directory. The [central directory](https://en.wikipedia.org/wiki/ZIP_(file_format)#Central_directory_file_header) lists all files in the archive and where to find them. Python's [zipfile](https://docs.python.org/3/library/zipfile.html) uses these two pieces to determine which part of the file to load into memory when the user requests a particular file. This package overwrites that loading process to work with cloud APIs directly rather than only with local filesystems. All credit go to [remotezip](https://github.com/gtsystem/python-remotezip) for figuring out how to overwrite the process, I only edited it to use APIs rather than HTTP requests.