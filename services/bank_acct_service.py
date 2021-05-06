from daos.bank_acct_dao_impl import BankAcctDAOImpl


class BankAcctService:

    bank_acct_dao = BankAcctDAOImpl()

    @classmethod
    def create_bank_acct(cls, bank_acct):
        return cls.bank_acct_dao.create_bank_acct(bank_acct)

    @classmethod
    def all_bank_accts(cls, client_id):
        return cls.bank_acct_dao.all_bank_accts(client_id)

    @classmethod
    def some_bank_accts(cls, client_id, conditions):
        return cls.bank_acct_dao.some_bank_accts(client_id, conditions)

    @classmethod
    def get_bank_acct_by_id(cls, client_id, bank_acct_id):
        return cls.bank_acct_dao.get_bank_acct(client_id, bank_acct_id)

    @classmethod
    def update_bank_acct(cls, bank_acct):
        return cls.bank_acct_dao.update_bank_acct(bank_acct)

    @classmethod
    def delete_bank_acct(cls, client_id, bank_acct_id):
        return cls.bank_acct_dao.delete_bank_acct(client_id, bank_acct_id)

    # Withdraw, Deposit, & Transfer methods:

    @classmethod
    def deposit_funds(cls, client_id, bank_acct_id, amount):
        return cls.bank_acct_dao.deposit_funds(client_id, bank_acct_id, amount)

    @classmethod
    def withdraw_funds(cls, client_id, bank_acct_id, amount):
        return cls.bank_acct_dao.withdraw_funds(client_id, bank_acct_id, amount)

    @classmethod
    def transfer_funds(cls, client_id, id_of_BA_taken_from, id_of_BA_depos_into, amount):
        return cls.bank_acct_dao.transfer_funds(
            client_id, id_of_BA_taken_from, id_of_BA_depos_into, amount
        )
