import io
import pathlib
import uuid

from google.cloud import storage

from .interface import FileSystemDriver


class GCSDriver(FileSystemDriver):
    def __init__(self, json_credentials_path: str, bucket_name: str, prefix_path: str = None) -> None:
        self.client = storage.Client(json_credentials_path)
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(self.bucket_name)
        self.path = prefix_path if prefix_path else ""

    async def read(self, name: str) -> io.BytesIO:
        name = name.replace(f"{self.bucket_name}/", "")
        blob: storage.Blob = self.bucket.blob(name)
        return io.BytesIO(blob.download_as_bytes())

    async def write(self, data: io.BytesIO, name: str) -> str:
        suffix_name = pathlib.Path(name).suffix
        filename = f"{uuid.uuid4()}{suffix_name}"
        blob: storage.Blob = self.bucket.blob(f"{self.path}{filename}")
        blob.upload_from_file(data)
        return f"{self.bucket_name}/{self.path}{filename}"
