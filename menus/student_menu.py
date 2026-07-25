from utils.helpers import print_header, pause
import services.student_service as student_service


def register_student():
    print_header("Register Student")

    fullname = input("Full Name: ")
    age = int(input("Age: "))
    school = input("School: ")
    class_level = input("Class Level: ")
    guardian_name = input("Guardian Name: ")
    guardian_phone = input("Guardian Phone: ")

    if student_service.register_student(
        fullname,
        age,
        school,
        class_level,
        guardian_name,
        guardian_phone
    ):
        print("Student registered successfully.")

    pause()


def view_students():
    print_header("All Students")

    students = student_service.get_all_students()

    for student in students:
        print(
            f"{student.student_id} | {student.fullname} | {student.school}"
        )

    pause()


def search_student():
    print_header("Search Student")

    term = input("Enter student ID or name: ")

    students = student_service.search_students(term)

    for student in students:
        print(
            f"{student.student_id} | {student.fullname}"
        )

    pause()


def update_student():
    print_header("Update Student")

    student_id = input("Student ID: ")

    students = student_service.search_students(student_id)

    if not students:
        print("Student not found.")
        pause()
        return

    student = students[0]

    fullname = input("New name: ")
    age = int(input("New age: "))
    school = input("New school: ")
    class_level = input("New class: ")
    guardian_name = input("Guardian name: ")
    guardian_phone = input("Guardian phone: ")

    if student_service.update_student_record(
        student.student_id,
        fullname,
        age,
        school,
        class_level,
        guardian_name,
        guardian_phone
    ):
        print("Updated successfully.")

    pause()


def delete_student():
    print_header("Delete Student")

    student_id = input("Student ID: ")

    if student_service.delete_student_record(student_id):
        print("Deleted successfully.")
    else:
        print("Student not found.")

    pause()


def student_menu():

    while True:
        print_header("STUDENT MANAGEMENT")

        print("1. Register Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Return")

        choice = input("Choose: ")

        if choice == "1":
            register_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            break
        else:
            print("Invalid choice")
