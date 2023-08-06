import abc
from abc import ABC


class FilesManagerProtocol(ABC):

    @abc.abstractmethod
    def read_all_text(self, filepath: str):
        pass


class FilesManager(FilesManagerProtocol):

    def read_all_text(self, filepath: str):
        file = open(filepath)
        file_content = file.read()
        file.close()
        return file_content
