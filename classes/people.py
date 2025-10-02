from abc import ABC, abstractmethod
import re
from datetime import date
from decimal import Decimal

class InvalidNameError(ValueError):
    """Имя или фамилия не соответствуют формату."""
    pass

class InvalidEmailError(ValueError):
    """Введите корректный email. Например, sergey@example.com"""
    pass

class InvalidPhoneError(ValueError):
    """Некорректный номер телефона."""
    pass

class Person(ABC):
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: str
    ):
        # Валидация и присвоение с обработкой ошибок
        try:
            self.id = self._validate_id(id)
            self.first_name = self._validate_name(first_name, "first_name")
            self.last_name = self._validate_name(last_name, "last_name")
            self.email = self._validate_email(email)
            self.phone = self._validate_phone(phone)
        except (InvalidNameError, InvalidEmailError, InvalidPhoneError, ValueError) as e:
            print(f"Ошибка при создании класса Person: {e}")
            raise  # Можно ловить выше, но не игнорировать

    @staticmethod
    def _validate_id(id_val: int) -> int:
        if not isinstance(id_val, int) or id_val <= 0:
            raise ValueError("ID должен быть положительным целым числом.")
        return id_val

    @staticmethod
    def _validate_name(name: str, field: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise InvalidNameError(f"Поле '{field}' не может быть пустым.")
        if not re.match(r"^[А-Яа-яA-Za-z\-']+$", name.strip()):
            raise InvalidNameError(f"Поле '{field}' содержит недопустимые символы.")
        return name.strip()

    @staticmethod
    def _validate_email(email: str) -> str:
        email = email.strip()
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise InvalidEmailError("Некорректный формат email.")
        return email

    @staticmethod
    def _validate_phone(phone: str) -> str:
        phone = re.sub(r"\D", "", phone)  # оставляем только цифры
        if len(phone)!=11:
            raise InvalidPhoneError("Номер телефона должен содержать 10 цифр, не считая +7")
        return phone

    @abstractmethod
    def get_full_name(self) -> str:
        #Абстрактный метод, это для наследуюемых классов
        pass

    def __str__(self) -> str:
        return f"{self.get_full_name()} <{self.email}>"
class Member(Person):
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, membership_start_date: date,
                 membership_end_date: date, is_active: bool=True):
        super().__init__(id, first_name, last_name, email, phone)
        self.membership_start_date = membership_start_date
        self.membership_end_date = membership_end_date
        self.is_active = is_active
    def get_full_name(self) -> str:
            return f"{self.first_name} {self.last_name}"
    def renew_membership(self, days: int = 365) -> None:
            from datetime import timedelta
            self.membership_end_date = date.today() + timedelta(days=days)
            self.is_active = True
    def cancel_membership(self) -> None:
            self.is_active = False

class Coach(Person):
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, specialization: str, hourly_rate : Decimal):
        super().__init__(id, first_name, last_name, email, phone)
        self.specialization = specialization
        self.hourly_rate = hourly_rate
        self.is_active = True

        def get_full_name(self) -> str:
            return f"{self.first_name} {self.last_name} ({self.specialization})"
        def set_availability(self, available: bool) -> None:
            self.is_active = available
class Staff(Person):
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, position: str, salary: Decimal, hire_date: date):
        super().__init__(id, first_name, last_name, email, phone)
        self.position = position
        self.salary = salary
        self.hire_date = hire_date

        def get_full_name(self) -> str:
            return f"{self.first_name} {self.last_name} ({self.position})"
        def perform_duty(self) -> None:
            pass