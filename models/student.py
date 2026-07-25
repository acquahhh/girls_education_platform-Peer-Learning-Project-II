"""Student domain model."""


class Student:
    """Represents a girl enrolled on the platform."""

    def __init__(self, fullname, age, school, class_level,
                 guardian_name, guardian_phone, student_id=None):
        """Initialize a Student record."""
        self.student_id = student_id
        self.fullname = fullname
        self.age = age
        self.school = school
        self.class_level = class_level
        self.guardian_name = guardian_name
        self.guardian_phone = guardian_phone

    @classmethod
    def from_row(cls, row):
        """Build a Student from a database dict row."""
        if not row:
            return None
        return cls(
            student_id=row.get("student_id"),
            fullname=row.get("fullname"),
            age=row.get("age"),
            school=row.get("school"),
            class_level=row.get("class_level"),
            guardian_name=row.get("guardian_name"),
            guardian_phone=row.get("guardian_phone"),
        )