from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

# Запобігання циклічним імпортам для type hinting
if TYPE_CHECKING:
    # Повертаємо відносний імпорт
    from .models import Employee, Department

# --- Інтерфейси ---
class IPaymentScheme(ABC):
    """Інтерфейс для схем розрахунку базової ЗП"""
    @abstractmethod
    def calculate_base_salary(self, employee: 'Employee', department: 'Department') -> float:
        """Розраховує базову зарплату працівника."""
        pass

class IBonusScheme(ABC):
    """Інтерфейс для схем розрахунку премії"""
    @abstractmethod
    def calculate_bonus(self, employee: 'Employee', department: 'Department', base_salary: float) -> float:
        """Розраховує премію працівника."""
        pass

class IPlanDistributionStrategy(ABC):
    """Інтерфейс для стратегій розподілу плану"""
    @abstractmethod
    def distribute_plan(self, department: 'Department') -> dict[int, float]:
        """Розподіляє план відділу між працівниками."""
        pass

# --- Конкретні схеми оплати ---
class FixedRateScheme(IPaymentScheme):
    """Фіксована ставка"""
    def __init__(self, rate: float):
        self._rate = rate

    def calculate_base_salary(self, employee: 'Employee', department: 'Department') -> float:
        # Для прикладу, ставка може залежати від досвіду
        experience_bonus = 1 + (employee.experience_years * 0.05) # +5% за рік досвіду
        return self._rate * experience_bonus

class ProductionScheme(IPaymentScheme):
    """Оплата від виробітку"""
    def __init__(self, price_per_unit: float):
        self._price_per_unit = price_per_unit

    def calculate_base_salary(self, employee: 'Employee', department: 'Department') -> float:
        return employee.monthly_production * self._price_per_unit

# --- Конкретні схеми преміювання ---
class FixedBonusScheme(IBonusScheme):
    """Фіксована премія"""
    def __init__(self, amount: float):
        self._amount = amount

    def calculate_bonus(self, employee: 'Employee', department: 'Department', base_salary: float) -> float:
        return self._amount

class PercentageBonusScheme(IBonusScheme):
    """Премія у % від базової ЗП"""
    def __init__(self, percentage: float):
        # percentage має бути від 0 до 100
        self._percentage = max(0, min(100, percentage))

    def calculate_bonus(self, employee: 'Employee', department: 'Department', base_salary: float) -> float:
        return base_salary * (self._percentage / 100.0)

class PlanCompletionBonusScheme(IBonusScheme):
    """Премія за виконання плану відділу"""
    def __init__(self, percentage: float, threshold: float = 100.0):
        self._percentage = max(0, min(100, percentage))
        self._threshold = threshold # Мінімальний % виконання плану для премії

    def calculate_bonus(self, employee: 'Employee', department: 'Department', base_salary: float) -> float:
        if department.monthly_plan <= 0:
            return 0.0 # Немає плану - немає премії

        total_production = sum(emp.monthly_production for emp in department.employees)
        plan_completion_percentage = (total_production / department.monthly_plan) * 100

        if plan_completion_percentage >= self._threshold:
            return base_salary * (self._percentage / 100.0)
        else:
            return 0.0

# --- Конкретні стратегії розподілу плану ---
class EqualPlanDistribution(IPlanDistributionStrategy):
    """Рівномірний розподіл плану"""
    def distribute_plan(self, department: 'Department') -> dict[int, float]:
        num_employees = len(department.employees)
        if num_employees == 0 or department.monthly_plan <= 0: # Додано перевірку на <= 0
            return {}
        plan_per_employee = department.monthly_plan / num_employees
        return {emp.id: plan_per_employee for emp in department.employees}

class ExperienceBasedPlanDistribution(IPlanDistributionStrategy):
    """Розподіл плану залежно від досвіду"""
    def distribute_plan(self, department: 'Department') -> dict[int, float]:
        # Визначаємо загальний "коефіцієнт досвіду" для відділу
        # Додаємо 1, щоб уникнути ділення на нуль і щоб працівники без досвіду теж мали частку
        total_experience_factor = sum(1 + emp.experience_years for emp in department.employees)

        if total_experience_factor == 0 or department.monthly_plan <= 0:
            # Якщо немає досвіду або плану, розподіляємо рівномірно
            num_employees = len(department.employees)
            if num_employees == 0: return {}
            plan_per_employee = department.monthly_plan / num_employees
            return {emp.id: plan_per_employee for emp in department.employees}

        distributed_plan = {}
        for emp in department.employees:
            # Частка працівника пропорційна його "коефіцієнту досвіду"
            share = (1 + emp.experience_years) / total_experience_factor
            distributed_plan[emp.id] = department.monthly_plan * share
        return distributed_plan
