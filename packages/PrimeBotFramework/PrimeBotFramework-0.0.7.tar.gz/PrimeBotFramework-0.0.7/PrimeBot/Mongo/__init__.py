from ast import Return
from mongoengine import connect, disconnect
      
class Mongo:

    def open_connections(self, username, password, host, alias, db):
        alias = connect(
            username=username,
            password=password,
            host=host,
            alias=alias,
            db=db
        )
        return alias

    def close_connections(self, alias):
        disconnect(alias)



