import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade

DATABASE_URL = "postgresql://postgres:qumtum-dizsof-1tyRmu@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def seed_data():
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    subjects = [
        Subject(name=fake.word().capitalize(), teacher=random.choice(teachers))
        for _ in range(8)
    ]
    session.add_all(subjects)
    session.commit()

    students = [
        Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)
    ]
    session.add_all(students)
    session.commit()

    grades = []
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(5, 20)):
                grades.append(
                    Grade(
                        student=student, subject=subject, grade=random.randint(60, 100)
                    )
                )

    session.add_all(grades)
    session.commit()


if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully!")
