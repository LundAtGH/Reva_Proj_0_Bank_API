from abc import abstractmethod, ABC


class ClientDAO(ABC):

    @abstractmethod
    def create_client(self, client):
        pass

    @abstractmethod
    def get_client(self, client_id):
        pass

    @abstractmethod
    def all_clients(self):
        pass

    @abstractmethod
    def update_client(self, new):
        pass

    @abstractmethod
    def delete_client(self, client_id):
        pass
