from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Employee:
    """Модель працівника"""
    id: int
    name: str
    position: str
    department_id: int
    base_salary_scheme_id: str # ID схеми оплати (наприклад, 'fixed', 'production')
    bonus_scheme_id: Optional[str] = None # ID схеми преміювання
    experience_years: int = 0
    monthly_production: float = 0.0 # Виробіток за місяць
    salary: float = 0.0 # Нарахована зарплата

    def __str__(self):
        return f"Працівник(ID: {self.id}, Ім'я: {self.name}, Посада: {self.position}, Департамент: {self.department_id})"

@dataclass
class Department:
    """Модель структурного підрозділу"""
    id: int
    name: str
    manager_id: Optional[int] = None
    monthly_plan: float = 0.0 # План на місяць
    employees: list[Employee] = field(default_factory=list) # Список працівників у відділі
    plan_distribution_strategy_id: str = 'equal' # ID стратегії розподілу плану

    def __str__(self):
        manager_name = f" (Керівник ID: {self.manager_id})" if self.manager_id else ""
        return f"Департамент(ID: {self.id}, Назва: {self.name}{manager_name}, План: {self.monthly_plan})"
