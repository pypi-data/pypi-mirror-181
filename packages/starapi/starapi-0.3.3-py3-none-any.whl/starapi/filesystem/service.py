import io
import typing as t

from .driver.interface import FileSystemDriver


class FileSystemService:
    def __init__(self, driver: t.Type[FileSystemDriver], *args, **kwargs) -> None:
        self.driver = driver(*args, **kwargs)

    async def read(self, name: str) -> io.BytesIO:
        return await self.driver.read(name)

    async def write(self, data: io.BytesIO, name: str) -> str:
        return await self.driver.write(data, name)
