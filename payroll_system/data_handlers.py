import json
import csv
from abc import ABC, abstractmethod
from typing import Any, List, Dict

class IDataHandler(ABC):
    """Інтерфейс для читання/запису даних"""

    @abstractmethod
    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """Зчитує дані з файлу."""
        pass

    @abstractmethod
    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """Записує дані у файл."""
        pass

class JsonDataHandler(IDataHandler):
    """Обробник JSON даних"""
    def read(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Перевіряємо чи файл не порожній
                content = f.read()
                if not content:
                    print(f"Попередження: Файл {file_path} порожній.")
                    return []
                return json.loads(content) # Використовуємо loads для обробки порожнього рядка
        except FileNotFoundError:
            print(f"Помилка: Файл не знайдено {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Помилка: Некоректний формат JSON у файлі {file_path}")
            return []
        except Exception as e:
            print(f"Неочікувана помилка читання JSON файлу {file_path}: {e}")
            return []


    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Помилка запису у файл {file_path}: {e}")
        except Exception as e:
            print(f"Неочікувана помилка запису JSON файлу {file_path}: {e}")


class CsvDataHandler(IDataHandler):
    """Обробник CSV даних"""
    def read(self, file_path: str) -> List[Dict[str, Any]]:
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                # Перевірка на порожній файл
                first_char = f.read(1)
                if not first_char:
                    print(f"Попередження: Файл {file_path} порожній.")
                    return []
                f.seek(0) # Повертаємося на початок файлу

                reader = csv.DictReader(f)
                if not reader.fieldnames:
                     print(f"Помилка: Не вдалося прочитати заголовки у CSV файлі {file_path}. Перевірте формат.")
                     return []

                for row in reader:
                    # Спроба конвертувати числові значення
                    processed_row = {}
                    for key, value in row.items():
                        if value is None: # Обробка порожніх значень
                            processed_row[key] = None
                            continue
                        try:
                            # Спробуємо int спочатку
                            processed_row[key] = int(value)
                        except (ValueError, TypeError):
                            try:
                                # Якщо не int, спробуємо float
                                processed_row[key] = float(value)
                            except (ValueError, TypeError):
                                # Якщо не число, залишаємо як рядок
                                processed_row[key] = value

                    data.append(processed_row)
            return data
        except FileNotFoundError:
            print(f"Помилка: Файл не знайдено {file_path}")
            return []
        except Exception as e:
             print(f"Помилка читання CSV файлу {file_path}: {e}")
             return []


    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        if not data:
            # Не будемо вважати це помилкою, просто створимо порожній файл із заголовками, якщо можливо
            # Або просто вийдемо, якщо не хочемо створювати порожні файли
            print(f"Попередження: Немає даних для запису у файл {file_path}.")
            # Можна створити порожній файл: open(file_path, 'w').close()
            return

        try:
            # Визначаємо заголовки з ключів першого словника
            headers = list(data[0].keys())
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        except IOError as e:
            print(f"Помилка запису у файл {file_path}: {e}")
        except IndexError:
             # Ця помилка виникає, якщо data порожній, але ми обробили це вище
             print(f"Помилка: Неможливо визначити заголовки для CSV, дані порожні.")
        except Exception as e:
             print(f"Неочікувана помилка запису CSV файлу {file_path}: {e}")
