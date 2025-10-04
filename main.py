from datetime import datetime
from decimal import Decimal
from classes.people import Coach
from classes.gym_room import GymRoom
from classes.group_class import GroupClass
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository
from repositories.group_class_repository import GroupClassRepository

# 1. Сохраняем тренера
coach_repo = CoachRepository()
coach = Coach(1, "Иван", "Сидоров", "ivan@fit.com", "79998887766", "Кардио", Decimal("2000.00"))
coach_repo.save(coach)

# 2. Сохраняем зал
room_repo = GymRoomRepository()
room = GymRoom(1, "Cardio Hall", "кардио", 15)
room_repo.save(room)

# 3. Сохраняем занятие
group_repo = GroupClassRepository()
group_class = GroupClass(1, "Утренняя кардио-зарядка", coach, room, datetime(2025, 10, 5, 9, 0), 12)
group_repo.save(group_class)

# 4. Загружаем всё
loaded_classes = group_repo.find_all()
cardio_class=loaded_classes[0]
print(f"\nДо записи: {cardio_class}")
cardio_class.add_attendee(1)
group_repo.save(cardio_class)
# 6. Проверяем результат
updated_classes = group_repo.find_all()
print("\nПосле записи:")
for cls in updated_classes:
    print(cls)