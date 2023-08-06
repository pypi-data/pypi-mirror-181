import abc
import io


class FileSystemDriver(abc.ABC):
    @abc.abstractmethod
    async def read(self, name: str) -> io.BytesIO:
        """Read file

        Args:
            name (str): file absolute path name

        Returns:
            io.BytesIO: data by BytesIO
        """
        return NotImplemented

    @abc.abstractmethod
    async def write(self, data: io.BytesIO, name: str) -> str:
        """Write file

        Args:
            data (io.BytesIO): data by BytesIO
            name (str): file name

        Returns:
            str: file absolute path
        """
        return NotImplemented
