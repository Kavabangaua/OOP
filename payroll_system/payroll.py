from typing import Dict, List, Optional, Type
from .models import Employee, Department
from .schemes import IPaymentScheme, IBonusScheme, IPlanDistributionStrategy
from .data_handlers import IDataHandler, JsonDataHandler, CsvDataHandler
from dataclasses import asdict

class PayrollSystem:
    """Основний клас системи нарахування зарплати"""

    def __init__(self):
        self.employees: Dict[int, Employee] = {}
        self.departments: Dict[int, Department] = {}
        self.payment_schemes: Dict[str, IPaymentScheme] = {}
        self.bonus_schemes: Dict[str, IBonusScheme] = {}
        self.plan_strategies: Dict[str, IPlanDistributionStrategy] = {}
        self.data_handlers: Dict[str, IDataHandler] = {
            'json': JsonDataHandler(),
            'csv': CsvDataHandler()
        }

    def register_payment_scheme(self, scheme_id: str, scheme: IPaymentScheme):
        self.payment_schemes[scheme_id] = scheme

    def register_bonus_scheme(self, scheme_id: str, scheme: IBonusScheme):
        self.bonus_schemes[scheme_id] = scheme

    def register_plan_strategy(self, strategy_id: str, strategy: IPlanDistributionStrategy):
        self.plan_strategies[strategy_id] = strategy

    def _get_data_handler(self, file_path: str) -> Optional[IDataHandler]:
        """Визначає обробник даних за розширенням файлу."""
        extension = file_path.split('.')[-1].lower()
        return self.data_handlers.get(extension)

    def load_data(self, employees_path: str, departments_path: str, production_path: Optional[str] = None):
        """Завантажує дані працівників, відділів та виробітку."""
        emp_handler = self._get_data_handler(employees_path)
        dep_handler = self._get_data_handler(departments_path)

        if not emp_handler or not dep_handler:
            print("Помилка: Не вдалося визначити обробник для файлів працівників або відділів.")
            return

        employees_data = emp_handler.read(employees_path)
        departments_data = dep_handler.read(departments_path)

        # Створюємо об'єкти Department
        self.departments = {d['id']: Department(**d) for d in departments_data}

        # Створюємо об'єкти Employee і додаємо їх до словника та відділів
        self.employees = {}
        for emp_data in employees_data:
            employee = Employee(**emp_data)
            self.employees[employee.id] = employee
            if employee.department_id in self.departments:
                self.departments[employee.department_id].employees.append(employee)
            else:
                 print(f"Попередження: Працівник ID {employee.id} має неіснуючий ID відділу {employee.department_id}")


        # Завантажуємо дані виробітку (якщо є)
        if production_path:
            prod_handler = self._get_data_handler(production_path)
            if prod_handler:
                production_data = prod_handler.read(production_path)
                for prod_entry in production_data:
                    emp_id = prod_entry.get('employee_id')
                    units = prod_entry.get('units_produced', 0.0)
                    if emp_id in self.employees:
                        self.employees[emp_id].monthly_production += float(units) # Додаємо, якщо є кілька записів
                    else:
                        print(f"Попередження: Не знайдено працівника з ID {emp_id} для даних виробітку.")
            else:
                 print("Помилка: Не вдалося визначити обробник для файлу виробітку.")


        print("Дані успішно завантажено.")


    def distribute_department_plans(self):
        """Розподіляє плани для всіх відділів."""
        print("\nРозподіл планів...")
        for dep_id, department in self.departments.items():
            strategy_id = department.plan_distribution_strategy_id
            if strategy_id in self.plan_strategies:
                strategy = self.plan_strategies[strategy_id]
                distributed_plan = strategy.distribute_plan(department)
                print(f"  Розподіл для відділу '{department.name}': {distributed_plan}")
                # Тут можна було б зберегти індивідуальний план для кожного працівника,
                # але для поточного розрахунку це не обов'язково.
            else:
                print(f"  Попередження: Не знайдено стратегію розподілу '{strategy_id}' для відділу '{department.name}'")

    def calculate_payroll(self):
        """Розраховує зарплату для всіх працівників."""
        print("\nРозрахунок заробітної плати...")
        if not self.employees:
            print("Немає даних про працівників для розрахунку.")
            return

        for emp_id, employee in self.employees.items():
            department = self.departments.get(employee.department_id)
            if not department:
                print(f"  Помилка: Не знайдено відділ для працівника {employee.name} (ID: {emp_id}). Пропускаємо.")
                continue

            # Розрахунок базової ЗП
            base_salary = 0.0
            payment_scheme = self.payment_schemes.get(employee.base_salary_scheme_id)
            if payment_scheme:
                base_salary = payment_scheme.calculate_base_salary(employee, department)
            else:
                print(f"  Попередження: Не знайдено схему оплати '{employee.base_salary_scheme_id}' для {employee.name}. Базова ЗП = 0.")

            # Розрахунок премії
            bonus = 0.0
            if employee.bonus_scheme_id:
                bonus_scheme = self.bonus_schemes.get(employee.bonus_scheme_id)
                if bonus_scheme:
                    bonus = bonus_scheme.calculate_bonus(employee, department, base_salary)
                else:
                     print(f"  Попередження: Не знайдено схему преміювання '{employee.bonus_scheme_id}' для {employee.name}. Премія = 0.")

            # Загальна зарплата
            employee.salary = base_salary + bonus
            print(f"  Працівник: {employee.name}, База: {base_salary:.2f}, Премія: {bonus:.2f}, Всього: {employee.salary:.2f}")

        print("Розрахунок зарплати завершено.")

    def save_payroll_results(self, output_path: str):
        """Зберігає результати розрахунку зарплати."""
        print(f"\nЗбереження результатів у {output_path}...")
        output_handler = self._get_data_handler(output_path)
        if not output_handler:
            print("Помилка: Не вдалося визначити обробник для вихідного файлу.")
            return

        # Готуємо дані для збереження (тільки необхідні поля)
        payroll_data = []
        for employee in self.employees.values():
             payroll_data.append({
                 "id": employee.id,
                 "name": employee.name,
                 "position": employee.position,
                 "department_id": employee.department_id,
                 "calculated_salary": round(employee.salary, 2)
             })
             # Можна додати інші поля за потреби

        output_handler.write(output_path, payroll_data)
        print("Результати успішно збережено.")
