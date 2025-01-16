from datetime import datetime
import atexit


class InventoryLogger:
    """
    Store actions and informations of the inventory in a list of messages
    and optional in a file.
    """

    def __init__(self, filename: str = None):
        """Initialize the logger and set up the log storage."""
        self.__logs: list[str] = []
        self.__filename: str = filename
        self._filestream = None
        if filename:
            self.logToFile(filename=filename)
        atexit.register(self._close_filestream)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close_filestream()
        return self

    @property
    def filename(self) -> str:
        """Returns the filename of the logger."""
        return self.__filename

    @filename.setter
    def filename(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        if not filename.strip():
            raise ValueError("Filename must be a non-empty string.")
        self.__filename = filename

    def _open_filestream(self):
        if self.__filename:
            self._filestream = open(self.__filename, "a")
            now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log(f"Start logging at {now}.")
        else:
            self._filestream = None

    def _close_filestream(self):
        if self._filestream:
            now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log(f"Stop logging at {now}.")
            self._filestream.close()
            self._filestream = None

    def log(self, message: str):
        """Log a message by appending it to the log storage."""
        self.__logs.append(message)
        if self._filestream:
            now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._filestream.write(f"[{now}]" + message + '\n')

    def get_logs(self) -> str:
        """Return the stored messages as a text with line breaks."""
        return '\n'.join(self.__logs)

    def logToFile(self, enable=True, filename=None):
        self._close_filestream()
        if not enable:
            return
        if filename:
            self.__filename = filename
        self._open_filestream()
