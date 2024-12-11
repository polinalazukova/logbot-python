#задает интерфейс для работы с репозиториями пользователей
from abc import ABC, abstractmethod

class AbstractUserRepository(ABC):
    @abstractmethod
    def add_user(self, username, chat_id):
        pass

    @abstractmethod
    def update_user_notifications(self, chat_id, status):
        pass

    @abstractmethod
    def get_active_users(self):
        pass

    @abstractmethod
    def get_servers_for_user(self,chat_id):
        pass

    @abstractmethod
    def has_no_servers(self, chat_id):
        pass

    @abstractmethod
    def remove_all_servers(self, chat_id):
        pass

    @abstractmethod
    def remove_server(self, chat_id, server_name):
        pass

    @abstractmethod
    def add_server(self, chat_id, server_name):
        pass