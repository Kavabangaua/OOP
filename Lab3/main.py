from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Client(ABC):
    """Абстрактний базовий клас для клієнтів банку"""
    def __init__(self, name: str, account_number: str, balance: float = 0):
        self._name = name
        self._account_number = account_number
        self._balance = balance
        self._last_deposit_date = None
        self._transactions = []
    
    def deposit(self, amount: float) -> bool:
        """Внесення коштів на рахунок"""
        if self._can_deposit(amount):
            self._balance += amount
            self._last_deposit_date = datetime.now()
            self._transactions.append(f"Внесено {amount} грн. Баланс: {self._balance} грн")
            return True
        return False
    
    def withdraw(self, amount: float) -> bool:
        """Зняття коштів з рахунку"""
        if amount <= self._balance:
            self._balance -= amount
            self._transactions.append(f"Знято {amount} грн. Баланс: {self._balance} грн")
            return True
        return False
    
    def transfer(self, target_account, amount: float) -> bool:
        """Переказ коштів на інший рахунок"""
        if self.withdraw(amount):
            if target_account.deposit(amount):
                self._transactions.append(f"Переказано {amount} грн на рахунок {target_account._account_number}")
                return True
            else:
                self.deposit(amount)  #повертаємо кошти назад
        return False
    
    def get_balance(self) -> float:
        return self._balance
    
    def get_transactions(self) -> list:
        return self._transactions
    
    @abstractmethod
    def _can_deposit(self, amount: float) -> bool:
        """Абстрактний метод для перевірки можливості внесення коштів"""
        pass

class PrivateClient(Client):
    """Клас для приватних клієнтів"""
    def _can_deposit(self, amount: float) -> bool:
        if self._last_deposit_date is None:
            return True
        
        days_since_last_deposit = (datetime.now() - self._last_deposit_date).days
        return days_since_last_deposit >= 5

class CorporateClient(Client):
    """Клас для корпоративних клієнтів"""
    def __init__(self, name: str, account_number: str, balance: float = 0):
        super().__init__(name, account_number, balance)
        self._salary_payments_this_month = 0
        self._last_salary_month = None
    
    def _can_deposit(self, amount: float) -> bool:
        """Реалізація абстрактного методу для перевірки можливості внесення коштів"""
        current_month = datetime.now().month
        
        if self._last_salary_month != current_month:
            self._salary_payments_this_month = 0
            self._last_salary_month = current_month
        
        return self._salary_payments_this_month < 2
    
    def deposit(self, amount: float) -> bool:
        if super().deposit(amount):
            self._salary_payments_this_month += 1
            return True
        return False

class ClientContainer:
    """Клас-контейнер для управління клієнтами"""
    def __init__(self):
        self.__clients = []
        self.__total_transactions = 0
        self.__total_balance = 0
    
    def add_client(self, client: Client):
        """Додавання клієнта"""
        self.__clients.append(client)
        self.__update_totals()
    
    def remove_client(self, account_number: str):
        """Видалення клієнта за номером рахунку"""
        self.__clients = [c for c in self.__clients if c._account_number != account_number]
        self.__update_totals()
    
    def get_client(self, account_number: str) -> Client:
        """Отримання клієнта за номером рахунку"""
        for client in self.__clients:
            if client._account_number == account_number:
                return client
        return None
    
    def __update_totals(self):
        """Оновлення загальних показників"""
        self.__total_balance = sum(client.get_balance() for client in self.__clients)
        self.__total_transactions = sum(len(client.get_transactions()) for client in self.__clients)
    
    def process_monthly_operations(self):
        """Обробка щомісячних операцій для всіх клієнтів"""
        for client in self.__clients:
            if isinstance(client, CorporateClient):
                client._salary_payments_this_month = 0
                client._last_salary_month = datetime.now().month
    
    def get_statistics(self):
        """Отримання статистики по всіх клієнтах"""
        private_clients = sum(1 for c in self.__clients if isinstance(c, PrivateClient))
        corporate_clients = sum(1 for c in self.__clients if isinstance(c, CorporateClient))
        
        return {
            "total_clients": len(self.__clients),
            "private_clients": private_clients,
            "corporate_clients": corporate_clients,
            "total_balance": self.__total_balance,
            "total_transactions": self.__total_transactions
        }
    
    def print_all_clients(self):
        """Виведення інформації про всіх клієнтів"""
        print("\nІнформація про всіх клієнтів:")
        for client in self.__clients:
            print(f"\nКлієнт: {client._name}")
            print(f"Номер рахунку: {client._account_number}")
            print(f"Тип клієнта: {client.__class__.__name__}")
            print(f"Поточний баланс: {client.get_balance()} грн")
            print("Останні транзакції:")
            for transaction in client.get_transactions()[-3:]:
                print(f"  - {transaction}")
        
        #виведення загальної статистики
        stats = self.get_statistics()
        print("\nЗагальна статистика:")
        print(f"Всього клієнтів: {stats['total_clients']}")
        print(f"Приватних клієнтів: {stats['private_clients']}")
        print(f"Корпоративних клієнтів: {stats['corporate_clients']}")
        print(f"Загальний баланс: {stats['total_balance']} грн")
        print(f"Всього транзакцій: {stats['total_transactions']}")

#оновлена демонстрація роботи
if __name__ == "__main__":
    #створення контейнера
    bank = ClientContainer()
    
    #створення клієнтів
    clients = [
        PrivateClient("Ігнат Шкарпетка", "1001", 1000),
        PrivateClient("Марія Ковальчук", "1002", 2000),
        CorporateClient("ТОВ Трембіта", "2001", 5000),
        CorporateClient("ПП Веселка", "2002", 3000)
    ]
    
    #додавання клієнтів до контейнера
    for client in clients:
        bank.add_client(client)
    
    #демонстрація операцій
    for client in clients:
        if isinstance(client, PrivateClient):
            print(f"\nСпроба внесення коштів приватним клієнтом {client._name}:")
            if client.deposit(500):
                print("Кошти успішно внесено")
            else:
                print("Внесення коштів неможливе (має пройти 5 днів)")
    
    #переказ коштів між клієнтами
    for i in range(len(clients) - 1):
        print(f"\nПереказ коштів від {clients[i]._name} до {clients[i+1]._name}:")
        if clients[i].transfer(clients[i+1], 200):
            print("Переказ успішно виконано")
        else:
            print("Помилка переказу")
    
    #обробка щомісячних операцій
    bank.process_monthly_operations()
    
    #виведення інформації про всіх клієнтів та статистики
    bank.print_all_clients()
