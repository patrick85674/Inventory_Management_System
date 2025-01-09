from datetime import datetime


class InventoryLogger:
    """
    Store actions and informations of the inventory in a list of messages
    and optional in a file.
    """

    def __init__(self, filename: str = None):
        """Initialize the logger and set up the log storage."""
        self.__logs: list[str] = []
        self.__filename: str = filename
        self._open_filestream()

    def __del__(self):
        self._close_filestream()

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

    def log(self, message: str):
        """Log a message by appending it to the log storage."""
        self.__logs.append(message)
        if self._filestream:
            self._filestream.write(message + '\n')
        print("Test " + message)

    def get_logs(self) -> str:
        """Return the stored messages as a text with line breaks."""
        return '\n'.join(self.__logs)
