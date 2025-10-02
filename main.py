# main.py
from datetime import date
from classes.people import Member
from repositories.member_repository import MemberRepository

def main():
    repo = MemberRepository()

    # Создаём участника
    member = Member(
        id=1,
        first_name="Анна",
        last_name="Петрова",
        email="anna@PUPUPU.max",
        phone="79123456789",
        membership_start_date=date(2025, 10, 2),
        membership_end_date=date(2026, 4, 2)
    )

    # Сохраняем
    repo.save(member)
    print("Участник сохранён!")

    # Загружаем всех
    all_members = repo.get_all()
    for m in all_members:
        print(f"- {m.get_full_name()} | активен: {m.is_active}")

if __name__ == "__main__":
    main()