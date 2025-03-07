from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc, create_engine
from models import Student, Subject, Grade, Group, Teacher

DATABASE_URL = "postgresql://postgres:qumtum-dizsof-1tyRmu@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    """Find the top 5 students with the highest average grade."""
    return (
        session.query(
            Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(subject_id):
    """Find the student with the highest average grade for a specific subject."""
    return (
        session.query(
            Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    )


def select_3(subject_id):
    """Find the average grade in groups for a specific subject."""
    return (
        session.query(
            Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.name)
        .all()
    )


def select_4():
    """Find the overall average grade."""
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()


def select_5(teacher_id):
    """Find courses taught by a specific teacher."""
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


def select_6(group_id):
    """Find students in a specific group."""
    return session.query(Student.name).filter(Student.group_id == group_id).all()


def select_7(group_id, subject_id):
    """Find student grades in a group for a specific subject."""
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


def select_8(teacher_id):
    """Find the average grade given by a specific teacher."""
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


def select_9(student_id):
    """Find courses attended by a specific student."""
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )


def select_10(student_id, teacher_id):
    """Find courses taken by a student from a specific teacher."""
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
