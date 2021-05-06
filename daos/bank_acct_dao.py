# Data Access Object (Bank Account)
from abc import abstractmethod, ABC


class BankAcctDAO(ABC):

    @abstractmethod
    def create_bank_acct(self, bank_acct):
        pass

    @abstractmethod
    def get_bank_acct(self, bank_acct_id):
        pass

    @abstractmethod
    def all_bank_accts(self):
        pass

    @abstractmethod
    def some_bank_accts(self, client_id, conditions):
        pass

    @abstractmethod
    def update_bank_acct(self, new):
        pass

    @abstractmethod
    def delete_bank_acct(self, bank_acct_id):
        pass

    @abstractmethod
    def deposit_funds(self, client_id, bank_acct_id, amount):
        pass

    @abstractmethod
    def withdraw_funds(self, client_id, bank_acct_id, amount):
        pass

    @abstractmethod
    def transfer_funds(self, client_id, id_of_BA_taken_from, id_of_BA_depos_into, amount):
        pass
