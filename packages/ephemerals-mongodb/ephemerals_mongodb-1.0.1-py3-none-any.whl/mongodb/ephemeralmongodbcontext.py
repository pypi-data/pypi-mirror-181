import uuid

from mongodb import DbManagerProtocol, DbManager, ConnectionParams


class EphemeralMongoDbContext:

    __db_manager: DbManagerProtocol
    __db_name: str = None
    __items: dict

    def __init__(self,
                 connection_params: ConnectionParams,
                 db_name: str,
                 items: dict,
                 db_manager: DbManagerProtocol = None):

        self.__db_manager = db_manager or DbManager(connection_params)
        self.__db_name = db_name
        self.__items = items

    def __enter__(self):
        if self.__db_name is None:
            self.__db_name = f'edb_{uuid.uuid4().hex}'
        else:
            if self.__db_manager.database_exists(self.__db_name):
                raise Exception(f'Database name {self.__db_name} is already taken !')

        self.__db_manager.create_database(self.__db_name)
        initialization_errors = []
        for coll_name in self.__items.keys():
            for payload in self.__items[coll_name]:
                try:
                    self.__db_manager.insert_document(self.__db_name, coll_name, payload)
                except Exception as e:
                    initialization_errors.append(e)
        return self, self.__db_name, initialization_errors

    def count_documents(self, coll_name):
        return self.__db_manager.count_documents(self.__db_name, coll_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__db_manager.drop_database(self.__db_name)
