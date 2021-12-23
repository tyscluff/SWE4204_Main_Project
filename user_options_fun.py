from admin_func import *
from login_func import create_user
from staff_func import *
from student_func import *

# These functions will be called based on what type of user is selected


def is_student(user_email):
    """This will let a student"""
    choice = input(
        """Enter the number next to the action you would like to perform
                        1) View my courses
                        2) View my modules
                        3) Logout: """
    )
    while choice not in ["1", "2", "3"]:
        choice = input("Error: you must enter 1,2, or 3 to select an option: ")
    if choice == "1":
        view_courses_for_students(user_email)
    elif choice == "2":
        view_modules_for_students(user_email)
    else:
        # make logout function to call
        pass


def is_staff(user_email):
    """This will let the staff pick their options and execute them"""
    choice = input(
        """Enter the number next to the action you would like to perform
                            1) View courses
                            2) View modules
                            3) View staff
                            4) View rooms
                            5) View students
                            6) Logout: """
    )
    while choice not in ["1", "2", "3", "4", "5", "6"]:
        choice = input("Error: you must enter 1,2,3,4,5, or 6 to select an option: ")
    if choice == "1":
        view_courses_staff(user_email)
    elif choice == "2":
        view_modules_staff(user_email)
    elif choice == "3":
        view_staff_staff()
    elif choice == "4":
        view_rooms_staff()
        pass
    elif choice == "5":
        view_students_staff(user_email)
    else:
        # make logout function
        pass


def is_admin():
    """This will give the staff the options of what they can do and execute it"""
    first_choice = input(
        """Enter the number next to the action you would like to perform
                1) Create Records
                2) View Records
                3) Update Records
                4) Delete Records
                5) Logout:
                                """
    )
    while first_choice not in ["1", "2", "3", "4", "5"]:
        first_choice = input(
            "Error: you must enter 1,2,3,4, or 5 to select an option: "
        )

    if first_choice == "1":
        second_choice = input(
            """Enter the number next to the records you want to create: 
                1) Create course
                2) Create module
                3) Create staff
                4) Create room
                5) Create student: 
                                """
        )
        while second_choice not in ["1", "2", "3", "4", "5"]:
            second_choice = input(
                "Error: you must enter 1,2,3,4, or 5 to select an option: "
            )

        if second_choice == "1":
            print("You will now be able to create a course")
            create_course()
        elif second_choice == "2":
            print("You will now be able to create a module")
            create_module()
        elif second_choice == "3":
            print(
                "To create a new staff member you must create a new user with account type staff"
            )
            create_user()
        elif second_choice == "4":
            print("You will now be able to create a new room")
            create_room()
        elif second_choice == "5":
            print(
                "To create a new student you must create a new user with account type student"
            )
            create_user()

    elif first_choice == "2":
        second_choice = input(
            """Enter the number next to the records you want to view: 
                1) View courses
                2) View modules
                3) View staff
                4) View rooms
                5) View students: 
                                """
        )
        while second_choice not in ["1", "2", "3", "4", "5"]:
            second_choice = input(
                "Error: you must enter 1,2,3,4, or 5 to select an option: "
            )
        if second_choice == "1":
            print(
                "You will now get to see the modules included in a course of your choosing"
            )
            view_course_modules()
        elif second_choice == "2":
            print("You will now see some info on a module of your choosing")
            view_module_info()
        elif second_choice == "3":
            print(
                "You will now be able to see info for a member of staff of your choosing"
            )
            view_staff()
        elif second_choice == "4":
            print("You will now be able to see info on a room of your choosing")
            view_rooms()
        elif second_choice == "5":
            print("You will now be able to see what courses a student is taking")
            view_students_in_courses()

    elif first_choice == "3":
        second_choice = input(
            """Enter the number next to the records you want to update: 
                1) Update courses
                2) Update modules
                3) Update staff
                4) Update rooms
                5) Update students
                6) Update user
                                """
        )
        while second_choice not in ["1", "2", "3", "4", "5", "6"]:
            second_choice = input(
                "Error: you must enter 1,2,3,4, or 5 to select an option: "
            )

        if second_choice == "1":
            print("You will now be able to update a course")
            update_course()
        elif second_choice == "2":
            print("You will now be able to update a module")
            update_module()
        elif second_choice == "3":
            print("You will now be able to update a staff")
        elif second_choice == "4":
            print("You will now be able to update a room")
            update_room()
        elif second_choice == "5":
            print("You will now be able to update a student")
            update_student()
        elif second_choice == "6":
            print("You will now be able to update a user")
            update_user()

    elif first_choice == "4":
        second_choice = input(
            """Enter the number next to the records you want to delete: 
                1) Delete courses
                2) Delete modules
                3) Delete staff
                4) Delete rooms
                5) Delete students
                6) Delete user
                                """
        )
        while second_choice not in ["1", "2", "3", "4", "5", "6"]:
            second_choice = input(
                "Error: you must enter 1,2,3,4, or 5 to select an option: "
            )

        if second_choice == "1":
            print("You wil now be able to delete a course")
            delete_course()
        elif second_choice == "2":
            print("You will now be able to delete a module")
            delete_module()
        elif second_choice == "3":
            print(
                """You will now be able to delete a staff member.
                    WARNING: This will delete them completely from the database
                    including their user login. """
            )
            delete_staff()
        elif second_choice == "4":
            print("You will now be able to delete a room")
            delete_room()
        elif second_choice == "5":
            print(
                """You will now be able to delete a student.
                    WARNING: This will delete them completely from the database
                    including their user login. """
            )
            delete_student()
        elif second_choice == "6":
            print(
                """You will now be able to delete a user. 
                This will not delete the student, staff, or admin completely from the database.
                It will take away their login information."""
            )
            delete_user()

    elif first_choice == "5":
        # make a logout function
        pass
