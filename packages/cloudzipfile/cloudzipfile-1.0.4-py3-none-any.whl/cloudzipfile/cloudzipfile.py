import io
import zipfile
from azure.storage.blob import BlobClient as BlobClient_AZURE
from cloudzipfile.cloudclients.cloudclients import AzureClient

__all__ = ['RemoteIOError', 'CloudZipFile']
INITIAL_BUFFER_SIZE = 64*1024

class RemoteZipError(Exception):
    pass

class OutOfBound(RemoteZipError):
    pass


class RemoteIOError(RemoteZipError):
    pass


class PartialBuffer:
    def __init__(self, buffer, offset, size, stream):
        self.buffer = buffer if stream else io.BytesIO(buffer.read())
        self.offset = offset
        self.size = size
        self.position = offset
        self.stream = stream

    def __repr__(self):
        return "<PartialBuffer off=%s size=%s stream=%s>" % (self.offset, self.size, self.stream)

    def read(self, size=0):
        if size == 0:
            size = self.offset + self.size - self.position

        content = self.buffer.read(size)
        self.position = self.offset + self.buffer.tell()
        return content

    def close(self):
        if not self.buffer.closed:
            self.buffer.close()
            if hasattr(self.buffer, 'release_conn'):
                self.buffer.release_conn()

    def seek(self, offset, whence):
        if whence == 2:
            self.position = self.size + self.offset + offset
        elif whence == 0:
            self.position = offset
        else:
            self.position += offset

        relative_position = self.position - self.offset

        if relative_position < 0 or relative_position >= self.size:
            raise OutOfBound("Position out of buffer bound")

        if self.stream:
            buff_pos = self.buffer.tell()
            if relative_position < buff_pos:
                raise OutOfBound("Negative seek not supported")

            skip_bytes = relative_position - buff_pos
            if skip_bytes == 0:
                return self.position
            self.buffer.read(skip_bytes)
        else:
            self.buffer.seek(relative_position)

        return self.position


class RemoteIO(io.IOBase):
    def __init__(self, fetchZipDataByRange, initial_buffer_size=INITIAL_BUFFER_SIZE):
        self.fetchZipDataByRange = fetchZipDataByRange
        self.initial_buffer_size = initial_buffer_size
        self.buffer = None
        self.file_size = None
        self.position = None
        self._seek_succeeded = False
        self.member_pos2size = None
        self._last_member_pos = None

    def set_pos2size(self, pos2size):
        self.member_pos2size = pos2size

    def read(self, size=0):
        if size == 0:
            size = self.file_size - self.buffer.position

        if not self._seek_succeeded:
            if self.member_pos2size is None:
                fetch_size = size
                stream = False
            else:
                try:
                    fetch_size = self.member_pos2size[self.buffer.position]
                    self._last_member_pos = self.buffer.position
                except KeyError:
                    if self._last_member_pos and self._last_member_pos < self.buffer.position:
                        fetch_size = self.member_pos2size[self._last_member_pos]
                        fetch_size -= (self.buffer.position - self._last_member_pos)
                    else:
                        raise OutOfBound("Attempt to seek outside boundary of current zip member")
                stream = True

            self._seek_succeeded = True
            self.buffer.close()
            self.buffer = self.fetchZipDataByRange((self.buffer.position, self.buffer.position + fetch_size -1), stream=stream)

        return self.buffer.read(size)

    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        if whence == 2 and self.file_size is None:
            size = self.initial_buffer_size
            self.buffer = self.fetchZipDataByRange((-size, None), stream=False)
            self.file_size = self.buffer.size + self.buffer.position

        try:
            pos = self.buffer.seek(offset, whence)
            self._seek_succeeded = True
            return pos
        except OutOfBound:
            self._seek_succeeded = False
            return self.buffer.position   # we ignore the issue here, we will check if buffer is fine during read

    def tell(self):
        return self.buffer.position

    def close(self):
        if self.buffer:
            self.buffer.close()
            self.buffer = None


class CloudZipFile(zipfile.ZipFile):
    def __init__(self, blobClient:BlobClient_AZURE, initial_buffer_size=INITIAL_BUFFER_SIZE, **kwargs):
        ''' Pass a blob client pointing to a zip file on Azure. Then use regular zipfile functions.
        Will only download the required parts rather than the entire zip file.'''
        self.kwargs = kwargs
        if isinstance(blobClient, BlobClient_AZURE):
            self.blobClient = AzureClient(blobClient)
        else:
            raise Exception(f'Client of type {type(blobClient)} not supported.')

        rio = RemoteIO(self.fetchZipDataByRange, initial_buffer_size)
        super(CloudZipFile, self).__init__(rio)
        rio.set_pos2size(self.get_position2size())

    def get_position2size(self):
        ilist = self.infolist()
        if len(ilist) == 0:
            return {}

        position2size = {ilist[-1].header_offset: self.start_dir - ilist[-1].header_offset}
        for i in range(len(ilist) - 1):
            m1, m2 = ilist[i: i+2]
            position2size[m1.header_offset] = m2.header_offset - m1.header_offset

        return position2size

    def fetchZipDataByRange(self, data_range, stream=io.BytesIO()):
        start, end = data_range
        if start < 0:
            # Get file size
            size = self.blobClient.getSize()
            offset = size + start
            if offset < 0: 
                offset = 0      # Should offset always be nonzero? Potential bug source.
        else:
            offset = start
        

        length = end-start+1 if end is not None else None

        print(f'Fetching remote data: offset: {offset}, length: {length}')
        buffer = self.blobClient.partialDownloadToBuffer(offset=offset, length=length)
        size = buffer.seek(0, 2); buffer.seek(0,0)

        return PartialBuffer(buffer, offset, size, stream)