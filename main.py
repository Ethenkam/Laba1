from datetime import date, datetime, timedelta
from decimal import Decimal


from classes.people import Member, Coach
from classes.gym_room import GymRoom
from classes.group_class import GroupClass
from classes.Membership_plan import MembershipPlan
from classes.Payment import Payment

from repositories.member_repository import MemberRepository
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository
from repositories.group_class_repository import GroupClassRepository
from repositories.membership_plan_repository import MembershipPlanRepository
from repositories.payment_repository import PaymentRepository


def ensure_data_exists():
    plan_repo = MembershipPlanRepository()
    if not plan_repo.find_all():
        plan_repo.save(MembershipPlan(1, "Базовый (10 мес)", 300, 34800))
        plan_repo.save(MembershipPlan(2, "Премиум (14 мес)", 420, 41200))
        print("Созданы базовые абонементы")

    coach_repo = CoachRepository()
    if not coach_repo.find_all():
        coach = Coach(1, "Иван", "Сидоров", "ivan@fit.com", "79998887766", "Кардио", Decimal("2000.00"))
        coach_repo.save(coach)
        print("Создан тренер")

    room_repo = GymRoomRepository()
    if not room_repo.find_all():
        room = GymRoom(1, "Зал для кардио", "кардио", 15)
        room_repo.save(room)
        print("Создан зал")



print("Добро пожаловать в систему управления фитнес-клубом!\n")

ensure_data_exists()

member_repo = MemberRepository()
plan_repo = MembershipPlanRepository()
payment_repo = PaymentRepository()
group_repo = GroupClassRepository()
coach_repo = CoachRepository()
room_repo = GymRoomRepository()


print("👥 Существующие участники:")
members = member_repo.get_all()
if members:
    for m in members:
        status = "активен" if m.is_active else "неактивен"
        print(f"  - {m.get_full_name()} | {status} | до: {m.membership_end_date}")
else:
    print("  (пока нет участников)")


print("\nДобавляем нового участника...")
new_member = Member(
    id=101,
    first_name="Пупа",
    last_name="Лупович",
    email="pupa@example.com",
    phone="79123848498",
    membership_start_date=date.today(),
    membership_end_date=date.today() - timedelta(days=1),
    is_active=False
)
member_repo.save(new_member)
print(f"Участник {new_member.get_full_name()} добавлен (пока без абонемента).")

print("\nПокупка абонемента...")
plans = plan_repo.find_all()
chosen_plan = plans[0]
print(f"Выбран план: {chosen_plan}")

payment = Payment(
    payment_id=1,
    member_id=new_member.id,
    plan_id=chosen_plan.plan_id,
    amount=chosen_plan.price,
    payment_date=date.today(),
)
payment_repo.save(payment)
print(f"Платёж создан: {payment.amount} руб.")


new_member.membership_start_date = date.today()
new_member.membership_end_date = date.today() + timedelta(days=chosen_plan.duration_days)
new_member.is_active = True
member_repo.save(new_member)
print(f"Абонемент активирован до: {new_member.membership_end_date}")

print("\nЗапись на групповое занятие...")


classes = group_repo.find_all()
coach = coach_repo.find_by_id(1)
room = room_repo.find_by_id(1)
if coach and room:
    group_class = GroupClass(
        class_id=1,
        class_name="Утренняя кардио-зарядка",
        coach=coach,
        room=room,
        schedule=datetime(2025, 10, 5, 9, 0),
        max_capacity=12
    )
    group_repo.save(group_class)
    classes = [group_class]
    print("Создано новое групповое занятие")

if classes:
    cardio_class = classes[0]
    print(f"Занятие: {cardio_class}")

    if cardio_class.add_attendee(new_member.id):
        group_repo.save(cardio_class)
        print(f"{new_member.get_full_name()} записан(а) на занятие!")
    else:
        print("Нет свободных мест!")

print("\n" + "="*60)
print("ИТОГОВОЕ СОСТОЯНИЕ:")
print("="*60)

print("\nВсе участники:")
for m in member_repo.get_all():
    status = "активен" if m.is_active else "неактивен"
    print(f"  - {m.get_full_name()} | {status} | абонемент до: {m.membership_end_date}")

print("\nВсе занятия:")
for cls in group_repo.find_all():
    print(f"  - {cls}")

print("\nПоследние платежи:")
for p in payment_repo.find_all()[-3:]:
    print(f"  - {p}")

