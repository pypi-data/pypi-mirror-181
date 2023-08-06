from pymongo import MongoClient

from mongodb import ConnectionParams, DbManagerProtocol


class DbManager(DbManagerProtocol):

    __connection_params: ConnectionParams

    def __init__(self, connection_params: ConnectionParams):
        self.__connection_params = connection_params

    def database_exists(self, name):
        client = MongoClient(self.__connection_params.get_connection_string())
        all_databases = list(client.list_databases())
        return len([db_info.get('name') for db_info in all_databases if db_info.get('name') == name]) > 0

    def create_database(self, name: str):
        client = MongoClient(self.__connection_params.get_connection_string())
        client.get_database(name).get_collection('_dummy').insert_one({'hi': 'stranger'})

    def insert_document(self, db_name, coll_name, doc):
        client = MongoClient(self.__connection_params.get_connection_string())
        client.get_database(db_name).get_collection(coll_name).insert_one(doc)

    def count_documents(self, db_name, coll_name):
        client = MongoClient(self.__connection_params.get_connection_string())
        return client.get_database(db_name).get_collection(coll_name).count_documents({})

    def drop_database(self, name: str):
        client = MongoClient(self.__connection_params.get_connection_string())
        client.drop_database(name)
