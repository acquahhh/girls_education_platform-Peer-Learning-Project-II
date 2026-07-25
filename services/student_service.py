from database.connection import db
from models.student import Student


def register_student(fullname, age, school, class_level, guardian_name, guardian_phone):
    query = """
        INSERT INTO Students
        (fullname, age, school, class_level, guardian_name, guardian_phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        db.execute(
            query,
            (fullname, age, school, class_level, guardian_name, guardian_phone),
            commit=True
        )
        return True
    except Exception as exc:
        print(f"Error registering student: {exc}")
        return False


def get_all_students():
    query = "SELECT * FROM Students"

    try:
        rows = db.fetch_all(query)
        return [Student.from_row(row) for row in rows]
    except Exception as exc:
        print(f"Error fetching students: {exc}")
        return []


def search_students(search_term):
    query = """
        SELECT * FROM Students
        WHERE student_id = %s OR fullname LIKE %s
    """

    try:
        rows = db.fetch_all(
            query,
            (search_term, f"%{search_term}%")
        )
        return [Student.from_row(row) for row in rows]

    except Exception as exc:
        print(f"Error searching students: {exc}")
        return []


def update_student_record(student_id, fullname, age, school, class_level, guardian_name, guardian_phone):
    query = """
        UPDATE Students
        SET fullname=%s,
            age=%s,
            school=%s,
            class_level=%s,
            guardian_name=%s,
            guardian_phone=%s
        WHERE student_id=%s
    """

    try:
        result = db.execute(
            query,
            (
                fullname,
                age,
                school,
                class_level,
                guardian_name,
                guardian_phone,
                student_id
            ),
            commit=True
        )

        return result > 0

    except Exception as exc:
        print(f"Error updating student: {exc}")
        return False


def delete_student_record(student_id):
    query = "DELETE FROM Students WHERE student_id=%s"

    try:
        result = db.execute(
            query,
            (student_id,),
            commit=True
        )

        return result > 0

    except Exception as exc:
        print(f"Error deleting student: {exc}")
        return False
