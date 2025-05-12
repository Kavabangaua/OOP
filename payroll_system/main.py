from .payroll import PayrollSystem
from .schemes import (
    FixedRateScheme, ProductionScheme,
    FixedBonusScheme, PercentageBonusScheme, PlanCompletionBonusScheme,
    EqualPlanDistribution, ExperienceBasedPlanDistribution
)

if __name__ == "__main__":
    # Створюємо екземпляр системи
    payroll_system = PayrollSystem()

    # Реєструємо схеми та стратегії
    payroll_system.register_payment_scheme('fixed', FixedRateScheme(rate=10000)) # Базова ставка 10000
    payroll_system.register_payment_scheme('production', ProductionScheme(price_per_unit=50)) # 50 за одиницю

    payroll_system.register_bonus_scheme('fixed_1k', FixedBonusScheme(amount=1000))
    payroll_system.register_bonus_scheme('percent_10', PercentageBonusScheme(percentage=10))
    payroll_system.register_bonus_scheme('plan_15', PlanCompletionBonusScheme(percentage=15, threshold=95)) # Премія 15%, якщо план >95%

    payroll_system.register_plan_strategy('equal', EqualPlanDistribution())
    payroll_system.register_plan_strategy('experience', ExperienceBasedPlanDistribution())

    # Шляхи до файлів даних (залишаємо як є, відносно папки запуску `payroll_system`)
    employees_file = 'payroll_system/data/employees.json'
    departments_file = 'payroll_system/data/departments.json'
    production_file = 'payroll_system/data/production.csv'
    output_file = 'payroll_system/data/payroll_output.json' # Можна змінити на .csv

    # Завантажуємо дані
    payroll_system.load_data(employees_file, departments_file, production_file)

    # Розподіляємо плани
    payroll_system.distribute_department_plans()

    # Розраховуємо зарплату
    payroll_system.calculate_payroll()

    # Зберігаємо результати
    payroll_system.save_payroll_results(output_file)

    print("\nРобота системи завершена.")
