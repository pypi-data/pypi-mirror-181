import abc


class DbManagerProtocol(abc.ABC):

    @abc.abstractmethod
    def database_exists(self, name):
        pass

    @abc.abstractmethod
    def create_database(self, name: str):
        pass

    @abc.abstractmethod
    def insert_document(self, db_name, coll_name, doc):
        pass

    @abc.abstractmethod
    def count_documents(self, db_name, coll_name):
        pass

    @abc.abstractmethod
    def drop_database(self, name: str):
        pass
