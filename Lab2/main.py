class SalaryCalculator:
    """Базовий клас для розрахунку зарплати"""
    def calculate(self) -> float:
        return 0.0

class FixedRateCalculator(SalaryCalculator):
    """Калькулятор фіксованої ставки"""
    def __init__(self, monthly_rate: float):
        self.__monthly_rate = monthly_rate
    
    def calculate(self) -> float:
        return self.__monthly_rate

class ProductionCalculator(SalaryCalculator):
    """Калькулятор оплати від виробітку"""
    def __init__(self, price_per_unit: float):
        self.__price_per_unit = price_per_unit
        self.__units_produced = 0
    
    def add_production(self, units: int):
        self.__units_produced += units
    
    def calculate(self) -> float:
        salary = self.__price_per_unit * self.__units_produced
        self.__units_produced = 0
        return salary

class BonusCalculator(SalaryCalculator):
    """Калькулятор бонусів"""
    def __init__(self, base_calculator: SalaryCalculator, bonus_percent: float):
        self.__base_calculator = base_calculator
        self.__bonus_percent = bonus_percent
    
    def calculate(self) -> float:
        base_salary = self.__base_calculator.calculate()
        bonus = base_salary * (self.__bonus_percent / 100)
        return base_salary + bonus

class PaymentSystem:
    """Система оплати"""
    def __init__(self, calculator: SalaryCalculator):
        self.__calculator = calculator
    
    def calculate_salary(self) -> float:
        return self.__calculator.calculate()
    
    def change_calculator(self, new_calculator: SalaryCalculator):
        self.__calculator = new_calculator

class Employee:
    """Клас для представлення працівника"""
    def __init__(self, name: str, position: str):
        self.__name = name
        self.__position = position
        self.__payment_system = None
    
    def set_payment_system(self, payment_system: PaymentSystem):
        self.__payment_system = payment_system
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def position(self) -> str:
        return self.__position
    
    def calculate_salary(self) -> float:
        if self.__payment_system:
            return self.__payment_system.calculate_salary()
        return 0.0

# Демонстрація роботи
if __name__ == "__main__":
    # Створення працівників
    manager = Employee("Іван Карасьович", "Менеджер")
    worker = Employee("Петро Бульбашка", "Робітник")
    lead_worker = Employee("Мемен Коваленко", "Провідний робітник")
    
    # Налаштування систем оплати
    manager.set_payment_system(
        PaymentSystem(FixedRateCalculator(15000))
    )
    
    worker_calculator = ProductionCalculator(100)
    worker.set_payment_system(
        PaymentSystem(worker_calculator)
    )
    
    lead_calculator = ProductionCalculator(120)
    lead_worker.set_payment_system(
        PaymentSystem(BonusCalculator(lead_calculator, 15))
    )
    
    # Демонстрація розрахунку зарплати
    print(f"Зарплата {manager.position}а {manager.name}: "
          f"{manager.calculate_salary():.2f} грн")
    
    # Додаємо виробіток для робітника
    worker_calculator.add_production(100)
    print(f"Зарплата {worker.position}а {worker.name}: "
          f"{worker.calculate_salary():.2f} грн")
    
    # Додаємо виробіток для провідного робітника
    lead_calculator.add_production(100)
    print(f"Зарплата {lead_worker.position}а {lead_worker.name}: "
          f"{lead_worker.calculate_salary():.2f} грн")
