from typing import List

from mongodb import DbManagerProtocol, EphemeralMongoDbContext, ConnectionParams


class EphemeralMongoDbContextBuilder:

    __items: dict

    def __init__(self):
        self.__items = {}

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
