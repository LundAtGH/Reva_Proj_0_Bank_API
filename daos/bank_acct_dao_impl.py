from daos.bank_acct_dao import BankAcctDAO
from exceptions.resource_not_found import ResourceNotFound
from exceptions.resource_unavailable import ResourceUnavailable
from models.bank_acct import BankAcct
from util.db_connection import connection


import logging
log = logging.getLogger("application")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class BankAcctDAOImpl(BankAcctDAO):

    @staticmethod
    def proj_zero_log(message):
        log.info("P-Zero: " + str(message))

    def create_bank_acct(self, bank_acct):

        self.proj_zero_log("Attempting to create bank account...")

        sql = "insert into bank_accounts values (DEFAULT, %s, %s, %s, DEFAULT) returning *"

        cursor = connection.cursor()
        cursor.execute(sql, (bank_acct.holder_id, bank_acct.type, bank_acct.funds))

        connection.commit()
        record = cursor.fetchone()

        return BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])

    def get_bank_acct(self, client_id, bank_acct_id):

        self.proj_zero_log("Attempting to get bank account...")

        sql = "select * from bank_accounts where holder_id = %s and id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (int(client_id), int(bank_acct_id)))

        record = cursor.fetchone()

        if record:
            return BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])
        else:
            raise ResourceNotFound("Bank account not found.")

    def all_bank_accts(self, client_id):

        self.proj_zero_log("Attempting to get all bank accounts...")

        sql = "select * from bank_accounts where holder_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        bank_acct_list = []

        for record in records:
            bank_acct = BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])

            bank_acct_list.append(bank_acct.json())

        if records:
            return bank_acct_list
        else:
            raise ResourceNotFound("Client not found.")

    def some_bank_accts(self, client_id, conditions):  # Condition req. for Pr. 0 hardcoded below:

        self.proj_zero_log("Attempting to get bank accounts meeting condition...")

        sql = "select * from bank_accounts where holder_id = %s and funds < 2000 and funds > 400"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        bank_acct_list = []

        for record in records:
            bank_acct = BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])

            bank_acct_list.append(bank_acct.json())

        if records:
            return bank_acct_list
        else:
            raise ResourceNotFound("Client not found.")

    def update_bank_acct(self, new):

        self.proj_zero_log("Attempting to update bank account...")

        sql = "update bank_accounts set type=%s, funds=%s where holder_id = %s and id = %s returning *"
        cursor = connection.cursor()
        cursor.execute(sql, (new.type, new.funds, new.holder_id, new.bank_acct_id))
        connection.commit()

        record = cursor.fetchone()

        if record:
            return BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])
        else:
            raise ResourceNotFound("Client or account not found.")

    def delete_bank_acct(self, client_id, bank_acct_id):

        self.proj_zero_log("Attempting to delete bank account...")

        sql = "delete from bank_accounts where holder_id = %s and id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, (int(client_id), int(bank_acct_id)))
        connection.commit()

        record = cursor.fetchone()

        if not record:
            raise ResourceNotFound("Client or account not found.")

    def deposit_funds(self, client_id, bank_acct_id, amount):

        self.proj_zero_log("Attempting to deposit funds...")

        sql = "select * from bank_accounts where holder_id = %s and id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (int(client_id), int(bank_acct_id)))

        record = cursor.fetchone()

        if record:
            sql = "update bank_accounts set funds=%s where holder_id = %s and id = %s returning *"
            cursor = connection.cursor()
            cursor.execute(sql, (
                float(amount) + float(str(record[3])),
                int(client_id), int(bank_acct_id)
            ))
            connection.commit()

            record = cursor.fetchone()

            if record:
                return BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])
        else:
            raise ResourceNotFound("Bank account not found.")

    def withdraw_funds(self, client_id, bank_acct_id, amount):

        self.proj_zero_log("Attempting to withdraw funds...")

        sql = "select * from bank_accounts where holder_id = %s and id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (int(client_id), int(bank_acct_id)))

        record = cursor.fetchone()

        if record:
            if float(amount) <= float(str(record[3])):

                sql = "update bank_accounts set funds=%s where holder_id = %s and id = %s returning *"
                cursor = connection.cursor()
                cursor.execute(sql, (
                    float(str(record[3])) - float(amount),
                    int(client_id), int(bank_acct_id)
                ))
                connection.commit()

                record = cursor.fetchone()

                if record:
                    return BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])
            else:
                raise ResourceUnavailable("Insufficient funds for that withdrawal.")
        else:
            raise ResourceNotFound("Bank account not found.")

    def transfer_funds(self, client_id, id_of_BA_taken_from, id_of_BA_depos_into, amount):

        self.proj_zero_log("Attempting to transfer funds...")

        sql = "select * from bank_accounts where holder_id = %s and id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (int(client_id), int(id_of_BA_taken_from)))
        record = cursor.fetchone()

        if record:
            if float(amount) <= float(str(record[3])):

                # Taking from 1st account...

                sql = "update bank_accounts set funds=%s where holder_id = %s and id = %s returning *"
                cursor = connection.cursor()
                cursor.execute(sql, (
                    float(str(record[3])) - int(amount),
                    int(client_id), int(id_of_BA_taken_from)
                ))
                connection.commit()

                # Depositing to 2nd account...

                sql = "select * from bank_accounts where holder_id = %s and id = %s"
                cursor = connection.cursor()
                cursor.execute(sql, (
                    int(client_id), int(id_of_BA_depos_into)
                ))
                record = cursor.fetchone()

                if record:
                    sql = "update bank_accounts set funds=%s where holder_id = %s and id = %s returning *"
                    cursor = connection.cursor()
                    cursor.execute(sql, (
                        float(amount) + float(str(record[3])),
                        int(client_id), int(id_of_BA_depos_into)
                    ))
                    connection.commit()
                    record = cursor.fetchone()

                    if record:
                        return BankAcct(record[0], record[1], record[2], float(str(record[3])), record[4])
                else:
                    raise ResourceNotFound("Client or account not found.")

                # End of deposit to 2nd account.

            else:
                raise ResourceUnavailable("Insufficient funds for that transfer.")
        else:
            raise ResourceNotFound("Client or account not found.")
