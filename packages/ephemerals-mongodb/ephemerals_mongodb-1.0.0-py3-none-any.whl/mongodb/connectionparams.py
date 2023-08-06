class ConnectionParams:

    host_name: str
    port_number: int
    username: str
    password: str
    direct_connection: bool

    def __init__(self,
                 host_name: str,
                 port_number: int,
                 username: str,
                 password: str,
                 direct_connection: bool = True):
        self.host_name = host_name
        self.port_number = port_number
        self.username = username
        self.password = password
        self.direct_connection = direct_connection

    def get_connection_string(self):
        return f'mongodb://{self.username}:{self.password}@{self.host_name}:{self.port_number}/?directConnection={str(self.direct_connection).lower()}'
