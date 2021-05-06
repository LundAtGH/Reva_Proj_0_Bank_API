from daos.client_dao import ClientDAO
from exceptions.resource_not_found import ResourceNotFound
from models.client import Client
from util.db_connection import connection


import logging
log = logging.getLogger("application")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class ClientDAOImpl(ClientDAO):

    @staticmethod
    def proj_zero_log(message):
        log.info("P-Zero: " + str(message))

    def create_client(self, client):

        self.proj_zero_log("Attempting to create client...")

        sql = "insert into clients values (DEFAULT, %s) returning *"

        name = client.name

        cursor = connection.cursor()
        cursor.execute(sql, [name])

        connection.commit()
        record = cursor.fetchone()

        return Client(record[0], record[1])

    def get_client(self, client_id):

        self.proj_zero_log("Attempting to get client...")

        sql = "select * from clients where id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])

        record = cursor.fetchone()

        if record:
            return Client(record[0], record[1])
        else:
            raise ResourceNotFound("Client not found.")

    def all_clients(self):

        self.proj_zero_log("Attempting to get all clients...")

        sql = "select * from clients"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1])

            client_list.append(client.json())

        return client_list

    def update_client(self, new):

        self.proj_zero_log("Attempting to update client...")

        sql = "update clients set name = %s where id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, [new.name, new.holder_id])

        connection.commit()
        record = cursor.fetchone()

        if record:
            return Client(record[0], record[1])
        else:
            raise ResourceNotFound("Client not found.")

    def delete_client(self, client_id):

        self.proj_zero_log("Attempting to delete client...")

        sql = "delete from clients where id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, [client_id])

        record = cursor.fetchone()
        connection.commit()

        if record:
            return Client(record[0], record[1])
        else:
            raise ResourceNotFound("Client not found.")
