from abc import ABC, abstractmethod

class AbstractUserRepository(ABC):
    @abstractmethod
    def add_user(self, username, chat_id, current_server=None):
        pass

    @abstractmethod
    def update_user_server(self, chat_id, server_name):
        pass

    @abstractmethod
    def update_user_notifications(self, chat_id, status):
        pass

    @abstractmethod
    def get_active_users(self):
        pass

    @abstractmethod
    def get_user_server(self,chat_id):
        pass