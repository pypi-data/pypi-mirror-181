import json
from typing import List

from mongodb import DbManagerProtocol, EphemeralMongoDbContext, ConnectionParams, FilesManagerProtocol, FilesManager


class EphemeralMongoDbContextBuilder:

    __files_manager: FilesManagerProtocol
    __items: dict

    def __init__(self, files_manager: FilesManagerProtocol = None):
        self.__files_manager = files_manager or FilesManager()
        self.__items = {}

    def add_items_from_file(self, filepath):
        file_content = self.__files_manager.read_all_text(filepath)
        try:
            data: dict = json.loads(file_content)
            for coll_name in data.keys():
                if not isinstance(data[coll_name], list):
                    raise Exception(f'{filepath} content is not valid !')
                if coll_name not in self.__items:
                    self.__items[coll_name] = []
                self.__items[coll_name].extend(data[coll_name])
        except Exception:
            raise Exception(f'{filepath} content is not valid !')
        return self

    def add_items(self, coll_name, items: List[dict]):
        if coll_name not in self.__items:
            self.__items[coll_name] = []
        self.__items[coll_name].extend(items)
        return self

    def build(self,
              connection_params: ConnectionParams,
              db_name: str = None,
              db_manager: DbManagerProtocol = None):

        if connection_params.host_name not in ['127.0.0.1', 'localhost']:
            raise Exception('Ephemeral database server must be local, use localhost or 127.0.0.1 as host name.')

        if db_name in ['admin', 'config', 'local']:
            raise Exception(f'Database name {db_name} is not allowed !')

        return EphemeralMongoDbContext(connection_params,
                                       db_name,
                                       self.__items,
                                       db_manager)
