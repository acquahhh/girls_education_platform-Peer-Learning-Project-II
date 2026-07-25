"""Schema creation for the Girls Education Platform."""

from database.connection import db

TABLE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role ENUM('admin', 'staff') NOT NULL DEFAULT 'staff'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        school VARCHAR(120) NOT NULL,
        class_level VARCHAR(50) NOT NULL,
        guardian_name VARCHAR(100) NOT NULL,
        guardian_phone VARCHAR(20) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Sponsors (
        sponsor_id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        organization VARCHAR(120),
        email VARCHAR(120) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Mentors (
        mentor_id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        profession VARCHAR(120) NOT NULL,
        email VARCHAR(120) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS SponsorAssignments (
        assignment_id INT AUTO_INCREMENT PRIMARY KEY,
        sponsor_id INT NOT NULL,
        student_id INT NOT NULL,
        date_assigned DATE NOT NULL,
        CONSTRAINT fk_sa_sponsor FOREIGN KEY (sponsor_id)
            REFERENCES Sponsors (sponsor_id) ON DELETE CASCADE,
        CONSTRAINT fk_sa_student FOREIGN KEY (student_id)
            REFERENCES Students (student_id) ON DELETE CASCADE,
        CONSTRAINT uq_sponsor_student UNIQUE (sponsor_id, student_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS MentorAssignments (
        assignment_id INT AUTO_INCREMENT PRIMARY KEY,
        mentor_id INT NOT NULL,
        student_id INT NOT NULL,
        date_assigned DATE NOT NULL,
        CONSTRAINT fk_ma_mentor FOREIGN KEY (mentor_id)
            REFERENCES Mentors (mentor_id) ON DELETE CASCADE,
        CONSTRAINT fk_ma_student FOREIGN KEY (student_id)
            REFERENCES Students (student_id) ON DELETE CASCADE,
        CONSTRAINT uq_mentor_student UNIQUE (mentor_id, student_id)
    )
    """,
]


def create_tables():
    """Create all tables if they do not yet exist."""
    connection = db.get_connection()
    cursor = connection.cursor()
    try:
        for statement in TABLE_STATEMENTS:
            cursor.execute(statement)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()