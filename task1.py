class GeometricProgression:
    __count = 0  #статична змінна для підрахунку екземплярів

    def __init__(self, first_element, ratio):
        if ratio == 0:
            raise ValueError("Знаменник прогресії не може бути нульовим")
        self.__first = first_element
        self.__ratio = ratio
        GeometricProgression.__count += 1
        self.__show_info()

    def __del__(self):
        GeometricProgression.__count -= 1
        print(f"Видалено прогресію. Залишилось {GeometricProgression.__count} прогресій")

    @staticmethod
    def __show_info():
        print(f"Всього створено {GeometricProgression.__count} прогресій")

    def __str__(self):
        return f"& {self.__first}, {self.__ratio}: " + self.get_first_n_elements(7)

    def get_element(self, n):
        """Повертає n-й елемент прогресії"""
        return self.__first * (self.__ratio ** (n - 1))

    def get_first_n_elements(self, n):
        """Повертає перші n елементів у вигляді рядка"""
        elements = [str(self.get_element(i)) for i in range(1, n + 1)]
        return "{" + ", ".join(elements) + "...}"

    def get_elements_from_to(self, k, m):
        """Повертає елементи прогресії від k-го до m-го"""
        if k > m:
            return "Неправильний діапазон"
        elements = [str(self.get_element(i)) for i in range(k, m + 1)]
        return "{" + ", ".join(elements) + "}"

    def change_parameters(self, new_first=None, new_ratio=None):
        """Змінює параметри прогресії"""
        if new_first is not None:
            self.__first = new_first
        if new_ratio is not None:
            if new_ratio == 0:
                raise ValueError("Знаменник прогресії не може бути нульовим")
            self.__ratio = new_ratio

    def __eq__(self, other):
        """Магічний метод для порівняння прогресій"""
        if not isinstance(other, GeometricProgression):
            return False
        return self.__first == other.__first and self.__ratio == other.__ratio

#робота класу
if __name__ == "__main__":
    #створюємо екземпляри
    prog1 = GeometricProgression(2, 3)
    print(prog1)  #виведимо форматі & a, b: {перші 7 членів}

    prog2 = GeometricProgression(1, 2)
    print(prog2)

    #отримуємо елементи
    print("\nЕлементи від 3 до 5 для prog1:")
    print(prog1.get_elements_from_to(3, 5))

    #зміна параметрів
    prog1.change_parameters(new_ratio=2)
    print("\nПрогресія 1 після зміни знаменника:")
    print(prog1)

    #перевірка рівності
    print("\nПеревірка рівності прогресій:")
    print("prog1 == prog2:", prog1 == prog2)

    #спроба створити прогресію з нульовим знаменником
    try:
        invalid_prog = GeometricProgression(1, 0)
    except ValueError as e:
        print("\nПомилка:", e)

    #видалення об'єктів
    del prog1
    del prog2
