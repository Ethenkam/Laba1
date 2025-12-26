## Laba1 — Система управления фитнес-клубом

Учебный проект для управления фитнес-клубом. Реализована логика работы с участниками, абонементами, тренерами, залами и групповыми занятиями.

### Структура проекта

```
Laba1/
├── main.py                           # Точка входа с примером использования
├── classes/                          # Основные модели
│   ├── people.py                    # Member, Coach
│   ├── gym_room.py                  # GymRoom
│   ├── group_class.py               # GroupClass (занятия)
│   ├── Membership_plan.py           # MembershipPlan (абонементы)
│   ├── Payment.py                   # Payment (платежи)
│   ├── PaymentService.py            # PaymentService
│   └── Equipment.py                 # Equipment (оборудование)
├── repositories/                     # Слой доступа к данным
│   ├── member_repository.py
│   ├── coach_repository.py
│   ├── gym_room_repository.py
│   ├── group_class_repository.py
│   ├── membership_plan_repository.py
│   └── payment_repository.py
├── test*.py                         # Примеры и тесты
└── test_data.xml                    # Тестовые данные

```

### Основной функционал

- **Управление участниками** — добавление, отслеживание активности абонементов
- **Абонементы** — два тарифа (базовый и премиум) с разными сроками
- **Тренеры и залы** — назначение занятий по категориям (кардио, силовая и т.п.)
- **Групповые занятия** — запись на занятия с ограничением по местам
- **Платежи** — отслеживание платежей за абонементы через сервис

### Пример использования

```python
from classes.people import Member
from classes.Membership_plan import MembershipPlan
from repositories.member_repository import MemberRepository
from repositories.membership_plan_repository import MembershipPlanRepository

# Создание участника
member = Member(
    id=101,
    first_name="Иван",
    last_name="Петров",
    email="ivan@example.com",
    phone="79991234567",
    membership_start_date=date.today(),
    membership_end_date=date.today() + timedelta(days=365),
    is_active=True
)

# Сохранение в репозиторий
repo = MemberRepository()
repo.save(member)
```

### Запуск

```bash
python main.py
```

Скрипт создаст начальные данные (абонементы, тренера, залы) и продемонстрирует типичный сценарий работы: добавление участника, покупку абонемента, запись на занятие.

### Тестирование

Есть примеры в `test.py` и `test1.py` для проверки отдельных компонентов.
