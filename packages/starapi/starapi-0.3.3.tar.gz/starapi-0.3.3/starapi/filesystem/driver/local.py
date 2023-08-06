import io
import pathlib
import uuid

from .interface import FileSystemDriver


class LocalDriver(FileSystemDriver):
    def __init__(self, prefix_path: str = None) -> None:
        self.path = f"{pathlib.Path().resolve()}/{prefix_path}" if prefix_path else f"{pathlib.Path().resolve()}/"

    async def read(self, name: str) -> io.BytesIO:
        with open(name, "rb") as file:
            return io.BytesIO(file.read())

    async def write(self, data: io.BytesIO, name: str) -> str:
        suffix_name = pathlib.Path(name).suffix
        filename = f"{uuid.uuid4()}{suffix_name}"
        with open(f"{self.path}s{filename}", "wb+") as file:
            file.write(data.getbuffer())

        return f"{self.path}{filename}"
