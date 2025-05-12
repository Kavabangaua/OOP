import copy
from functools import wraps

#метаклас для додавання можливості клонування
class CloneableMeta(type):
    def __new__(mcs, name, bases, attrs):
        #додаємо метод clone до класу
        def clone(self):
            #зберігаємо всі дані екземпляра (без методів)
            data_snapshot = {key: value for key, value in self.__dict__.items()}
            
            #метод для відновлення стану з збереженої копії
            def restore(self_instance):
                for key, value in data_snapshot.items():
                    setattr(self_instance, key, copy.deepcopy(value))
                return self_instance
            
            #додаємо метод restore до копії
            new_instance = copy.deepcopy(self)
            new_instance.restore = lambda: restore(new_instance)
            return new_instance
        
        attrs['clone'] = clone
        return super().__new__(mcs, name, bases, attrs)

#декоратор для додавання можливості клонування
def cloneable(cls):
    original_init = cls.__init__
    
    @wraps(original_init)
    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        #зберігаємо початковий стан після ініціалізації
        self.__initial_state = copy.deepcopy(self.__dict__)
    
    def clone(self):
        #створюємо нову копію об'єкта
        new_instance = copy.deepcopy(self)
        #зберігаємо поточний стан для можливості відновлення
        new_instance.__clone_state = copy.deepcopy(new_instance.__dict__)
        
        def restore():
            #відновлюємо стан з копії
            for key, value in new_instance.__clone_state.items():
                if key != "__clone_state":  # Щоб уникнути рекурсії
                    setattr(new_instance, key, copy.deepcopy(value))
            return new_instance
        
        #додаємо метод restore
        new_instance.restore = restore
        return new_instance
    
    #додаємо нові методи до класу
    cls.__init__ = __init__
    cls.clone = clone
    return cls

#приклад класу з використанням метакласу
class Person(metaclass=CloneableMeta):
    def __init__(self, name, age, hobbies=None):
        self.name = name
        self.age = age
        self.hobbies = hobbies or []
    
    def add_hobby(self, hobby):
        self.hobbies.append(hobby)
    
    def birthday(self):
        self.age += 1
    
    def __str__(self):
        return f"Person(name={self.name}, age={self.age}, hobbies={self.hobbies})"

#приклад класу з використанням декоратора
@cloneable
class Student:
    def __init__(self, name, grade, courses=None):
        self.name = name
        self.grade = grade
        self.courses = courses or []
    
    def add_course(self, course):
        self.courses.append(course)
    
    def upgrade(self):
        self.grade += 1
    
    def __str__(self):
        return f"Student(name={self.name}, grade={self.grade}, courses={self.courses})"

# Демонстрація використання
if __name__ == "__main__":
    #демонстрація метакласу
    print("демонстрація клонування з використанням метакласу:")
    person = Person("Іван", 25, ["Читання", "Програмування"])
    print(f"Оригінал: {person}")
    
    #клонуємо об'єкт
    person_clone = person.clone()
    print(f"клон початковий: {person_clone}")
    
    #змінюємо оригінал
    person.add_hobby("Спорт")
    person.birthday()
    print(f"оригінал після змін: {person}")
    print(f"клон (не змінився): {person_clone}")
    
    #змінюємо клон
    person_clone.add_hobby("Малювання")
    person_clone.birthday()
    print(f"клон після змін: {person_clone}")
    
    #відновлюємо початковий стан клону
    person_clone.restore()
    print(f"клон після відновлення: {person_clone}")
    
    print("\n" + "-" * 50 + "\n")
    
    #демонстрація декоратора
    print("демонстрація клонування з використанням декоратора:")
    student = Student("Марія", 10, ["Математика", "Історія"])
    print(f"оригінал: {student}")
    
    #клонуємо об'єкт
    student_clone = student.clone()
    print(f"клон початковий: {student_clone}")
    
    #змінюємо оригінал
    student.add_course("Фізика")
    student.upgrade()
    print(f"оригінал після змін: {student}")
    print(f"клон (не змінився): {student_clone}")
    
    #змінюємо клон
    student_clone.add_course("Хімія")
    student_clone.upgrade()
    print(f"клон після змін: {student_clone}")
    
    #відновлюємо початковий стан клону
    student_clone.restore()
    print(f"клон після відновлення: {student_clone}") 