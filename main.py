# Author: Tyson Cluff
# FoS4204

# The purpose of this program is to allow users to create, view, update,
# and delete data related to students, lecturers, courses, and modules at
# an imaginary university. There will be three kinds of users, student,
# staff, and adminstrator. Each user will be given different kinds of
# authorization for what they are allowed to do in the program.


# Import my dependecies
import sqlite3
from typing import NewType
import bcrypt
import getpass

# I'm opening my connection to the database
con = sqlite3.connect("UoM.db")
cur = con.cursor()

# I'm making functions to create all of my tables
def create_user_table():
    """This function will create the user table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user
        (
            user_email TEXT PRIMARY KEY,
            user_password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    """
    )
    con.commit()
    return


def create_student_table():
    """This function will create the student table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS student 
        (
            student_email TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )    
        """
    )
    con.commit()
    return


def create_staff_table():
    """This function will create the staff table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS staff
        (
            staff_email TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
        """
    )
    con.commit()
    return


def create_admin_table():
    """This function will create the admin table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS admin
        (
            admin_email TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
        """
    )
    con.commit()
    return


def create_course_table():
    """This function will create the course table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS course
        (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL
        )        
        """
    )
    con.commit()
    return


def create_module_table():
    """This function will create the module table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS module
        (
            module_id TEXT PRIMARY KEY,
            module_name TEXT NOT NULL,
            module_day TEXT NOT NULL,
            event_type TEXT NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL
        )    
        """
    )
    con.commit()
    return


def create_room_table():
    """This function will create the room table if it doesn't already exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS room
        (
            room_id TEXT PRIMARY KEY        
        )
        """
    )
    con.commit()
    return


# These functions will create the tables that combine data from two other tables
def create_course_enrollment_table():
    """This function will create the course_enrollment table if it doesn't exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS course_enrollment
        (
            student_email TEXT NOT NULL,
            course_id TEXT NOT NULL,
            FOREIGN KEY (student_email) REFERENCES student(student_email),
            FOREIGN KEY (course_id) REFERENCES course(course_id),
            primary key ( student_email, course_id )
        )
        """
    )
    con.commit()
    return


create_course_enrollment_table()


def create_course_modules_table():
    """This function will create the course_modules table if it doesn't exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS course_modules 
        (
            course_id TEXT NOT NULL,
            module_id TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES course(course_id),
            FOREIGN KEY (module_id) REFERENCES module(module_id),
            primary key ( course_id, module_id )
        )
        """
    )
    con.commit()
    return


def create_staff_modules_table():
    """This function will create the staff_modules table if it doesn't exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS staff_modules
        (
            staff_email TEXT NOT NULL,
            module_id TEXT NOT NULL,
            FOREIGN KEY (staff_email) REFERENCES staff(staff_email),
            FOREIGN KEY (module_id) REFERENCES module(module_id),
            primary key ( staff_email, module_id )      
        )    
        """
    )
    con.commit()
    return


def create_module_rooms_table():
    """This function will create the room_modules table if it doesn't exist"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS module_rooms 
        (
            module_id TEXT NOT NULL,
            room_id TEXT NOT NULL,
            FOREIGN KEY (module_id) REFERENCES module(module_id),
            FOREIGN KEY (room_id) REFERENCES room(room_id),
            primary key ( module_id, room_id ) 
        )
        """
    )
    con.commit()
    return


# This is going to be the start of the user interaction with the program
# Here the user will get to choose to login or create an account and then
# create an account and login or just create an account depending on the user choice


def login_or_create():
    """This function will let the user choose to login or create an account"""
    choice = input("Would you like to 1) Login or 2) Create an account: ")
    while choice not in ["1", "2"]:
        choice = input("Please enter 1 to login or 2 to create an account: ")
    return choice


def collect_email():
    """This function will collect the email value for create user"""
    email = input("Please enter your university email: ")
    confirm_email = input(
        f"Please enter Y to confirm that {email} is the correct email address or N to enter a different email address: "
    ).upper()
    while confirm_email not in ["Y", "N"]:
        confirm_email = input(f"Error you must enter Y or N: ").upper()
    while confirm_email == "N":
        email = input("Please enter your university email address: ")
        confirm_email = input(
            f"Please enter Y to confirm that {email} is the correct email address or N to enter a different email address: "
        ).upper()
        while confirm_email not in ["Y", "N"]:
            confirm_email = input(f"Error you must enter Y or N: ").upper()
    return email


def collect_and_hash_password():
    """This function will collect the password and hash it for the create user"""
    password = getpass.getpass("Enter your password: ")
    confirm_password = getpass.getpass("Confirm your password: ")

    while password != confirm_password:
        print("Passwords did not match. Try again")
        password = getpass.getpass("Enter your password: ")
        confirm_password = getpass.getpass("Confirm your password: ")

    password = password.strip().encode("utf-8")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def collect_account_type():
    account_type = input(
        """What type of account would you like to make?
           1) Student
           2) Staff account
           3) Admin account 
           Enter 1, 2, or 3 to select student, staff, or admin: """
    )
    while account_type not in ["1", "2", "3"]:
        account_type = input(
            """Error: 
            Please enter 1 to make a student account,
            2 to make a staff account,
            3 to make an admin account
             """
        )

    if account_type == "1":
        account_type = "student"
    elif account_type == "2":
        account_type = "staff"
    else:
        account_type = "admin"

    return account_type


def create_user():
    """This function will take user input to create a new user in the db"""
    email = collect_email()
    password = collect_and_hash_password()
    account_type = collect_account_type()
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")

    cur.execute("INSERT INTO user VALUES (?,?,?)", (email, password, account_type))

    if account_type == "student":
        cur.execute(
            "INSERT INTO student VALUES (?,?,?)", (email, first_name, last_name)
        )
    elif account_type == "staff":
        cur.execute("INSERT INTO staff VALUES (?,?,?)", (email, first_name, last_name))
    else:
        cur.execute("INSERT INTO admin VALUES (?,?,?)", (email, first_name, last_name))

    con.commit()

    print(f"Your account with the email {email} was created")
    return


def login_user():
    """This function will let a user login"""
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ").strip().encode("utf-8")

    cur.execute("SELECT * FROM user WHERE user_email = ?", (email,))
    result = cur.fetchall()

    if result == []:
        print("No user was found with that email")
    else:
        user_email = result[0][0]
        user_password = result[0][1]
        account_type = result[0][2]

        correct_password = bcrypt.checkpw(password, user_password)

        if correct_password == False:
            print("Incorrect password ")
        else:
            print(
                f"You were successfully logged in with the email: {user_email}. You have {account_type} access."
            )
    return


# These functions will be for the admin to query the database

# This first group are the create functions essesntially only for the admin
def create_module():
    """This function will let the admin create a module"""
    module_id = input("Please enter the module ID: ")
    module_name = input("Please enter the name of the module: ")
    module_day = input("Please enter the day of the module: ")
    event_type = input(
        "Enter 1 if this is an in person event or enter 2 if it is a zoom event: "
    )
    while event_type not in ["1", "2"]:
        event_type = input(
            "Error: You must enter 1 for an in person event or 2 for a zoom event: "
        )
    if event_type == "1":
        event_type = "In Person Lecture"
    else:
        event_type = "Zoom Lecture"
    start_time = input("Please enter the start time of the module: ")
    end_time = input("Please enter the end time of the module: ")

    cur.execute(
        "INSERT INTO module VALUES (?,?,?,?,?,?)",
        (module_id, module_name, module_day, event_type, start_time, end_time),
    )
    con.commit()

    print("Module was successfully created. ")
    return


def create_course():
    """This function will let an admin create a course"""
    course_id = input("Please enter the course id: ")
    course_name = input("Please enter the course name: ")

    cur.execute("INSERT INTO course VALUES (?,?)", (course_id, course_name))
    con.commit()

    print("Course was successfully created.")
    return


def create_room():
    """This function will let an admin create a room"""
    room_id = input("Please enter the room id: ")

    print(room_id)

    cur.execute("INSERT INTO room VALUES (?)", (room_id,))
    con.commit()

    print("Room was successfully created.")
    return


def assign_staff_modules():
    """This will let the admin assign staff modules"""
    staff = input("Enter the email of the staff you would like to assign: ")
    module = input("Enter the id of the module you would like to assign the staff: ")

    cur.execute("INSERT INTO staff_modules VALUES (?,?)", (staff, module))
    con.commit()

    print(f"{staff} was successfully assigned module {module}. ")
    return


def assign_course_modules():
    """This will let the admin assign course modules"""
    module = input("Please enter the id of the module you would like to assign: ")
    course = input(
        "Please enter the id of the course you would like to the module to be assigned to: "
    )

    cur.execute("INSERT INTO course_modules VALUES (?,?)", (course, module))
    con.commit()

    print(f"{module} was assigned to the course {course}.")
    return


def enroll_student():
    """This function will let the admin enroll a student"""
    student = input("Enter the email of the student you would like to enroll: ")
    course = input(
        "Enter the course id of the course you wyould like to enroll the student in: "
    )

    cur.execute("INSERT INTO course_enrollment VALUES (?,?)", (student, course))
    con.commit()

    print(f"{student} was enrolloed in {course}")
    return


def assign_room_modules():
    """This function will let the admin assign a module to a room"""
    room = input("Please enter the id of the room you would like to use: ")
    module = input(
        "Plese enter the id of the module you would like to assign to the room: "
    )

    cur.execute("INSERT INTO module_rooms VALUES (?,?)", (module, room))
    con.commit()

    print(f"{module} was assigned to room {room}.")
    return


# These are the general view functions
# I need to add formatting later but today it is about getting the basic queries right
def view_module_info():
    """This function will let an admin view info on a specific module"""
    module = input("Please enter the module id of the module you would like to view: ")

    cur.execute(
        """SELECT module.module_name, module.start_time, module.end_time, module.event_type, 
    module.module_day, staff.first_name, staff.last_name, module_rooms.room_id
    FROM (((staff_modules
    inner join module on staff_modules.module_id = module.module_id)
    inner join staff on staff_modules.staff_email = staff.staff_email)
    inner join module_rooms on staff_modules.module_id = module_rooms.module_id)
    where module.module_id = ?
    """,
        (module,),
    )

    # when formatting make sure to add a duration row based on the start_time
    # and end_time attributes

    table = cur.fetchall()
    if table == []:
        print(f"Module with id {module} not found. ")
    else:
        print(table)
    return


def view_course_modules():
    """This will let anyone view the modules that are on a specific course"""
    course = input("Plese enter the course id of the course you would like to view: ")

    cur.execute(
        """SELECT module.module_name
    FROM course_modules
    inner join module on course_modules.module_id = module.module_id
    where course_modules.course_id = ?
    """,
        (course,),
    )

    # when formatting display the course before all of the modules

    table = cur.fetchall()
    if table == []:
        print(f"Course with id {course} not found ")
    else:
        print(table)
    return


def view_lecturer_modules():
    """This will let a staff or admin view the modules a lecturer teaches and their workload"""
    lecturer = input("Please enter the email of the lecturer you would like to view: ")

    cur.execute(
        """SELECT module.module_name
        from staff_modules
        inner join module on staff_modules.module_id = module.module_id
        where staff_modules.staff_email = ?
    """,
        (lecturer,),
    )

    # You'll want to add more info about the module when formatting but the basic query works

    table = cur.fetchall()
    if table == []:
        print(
            f"Lecturer with email {lecturer} either doesn't exist or isn't teaching any modules at the moment."
        )
    else:
        print(table)
    return


def view_staff():
    """This will let the admin see the staff and their workload"""

    cur.execute(
        """select staff.staff_email, staff.first_name, staff.last_name, module.module_name, 
            module.module_day, module.start_time, module.end_time 
            from((staff_modules
            inner join staff on staff_modules.staff_email = staff.staff_email)
            inner join module on staff_modules.module_id = module.module_id)"""
    )

    # This gets all the info we need
    # When formatting need to make sure to make a workload value

    table = cur.fetchall()
    print(table)
    # for index in enumerate(table):
    #     print(f"Staff Id: {index[1][0]}")
    #     print(f"First Name: {index[1][1]}")
    #     print(f"Last Name: {index[1][2]}")
    #     print("---------------------------")


def view_rooms():
    """This will let the admin see the rooms with the modules in each room"""

    # Need to format and maybe add choosing a room instead of seeing all
    # of the rooms

    cur.execute(
        """SELECT room.room_id, module.module_name, module.module_day, 
                    module.start_time, module.end_time
                    FROM((module_rooms
                    INNER JOIN room on module_rooms.room_id = room.room_id)
                    INNER JOIN module on module_rooms.module_id = module.module_id)
    """
    )

    table = cur.fetchall()
    print(table)


def view_students_in_courses():
    """This will let the admin see what students are in each course"""

    # You need to format this a lot better

    cur.execute(
        """SELECT student.student_email, course.course_id
            FROM((course_enrollment
            INNER JOIN student on course_enrollment.student_email = student.student_email)
            INNER JOIN course on course_enrollment.course_id = course.course_id)
        
    """
    )

    table = cur.fetchall()
    print(table)


# These are the update functions for the admin


def update_student():
    """This will let the admin update the student table"""
    student_to_update = input("Enter the email of the student you want to update: ")

    new_first_name = input(
        "Enter the new first name you would like to give the student: "
    )
    new_last_name = input(
        "Enter the new last name you would like to give the student: "
    )

    cur.execute(
        """UPDATE student
                set first_name = ?,
                last_name = ? 
                where student_email = ?""",
        (new_first_name, new_last_name, student_to_update),
    )

    con.commit()

    print(
        f"Student with email {student_to_update} now has a first name of {new_first_name} and a last name of {new_last_name}"
    )


def update_staff():
    """This will let the admin update the staff table"""
    staff_to_update = input("Enter the email of the staff you want to update: ")

    new_first_name = input(
        "Enter the new first name you would like to give the staff: "
    )
    new_last_name = input("Enter the new last name you would like to give the staff: ")

    cur.execute(
        """UPDATE staff
                set first_name = ?,
                last_name = ? 
                where staff_email = ?""",
        (new_first_name, new_last_name, staff_to_update),
    )

    con.commit()

    print(
        f"Staff with email {staff_to_update} now has a first name of {new_first_name} and a last name of {new_last_name}"
    )


def update_admin():
    """This will let the admin update the admin table"""
    admin_to_update = input("Enter the email of the admin you want to update: ")

    new_first_name = input(
        "Enter the new first name you would like to give the admin: "
    )
    new_last_name = input("Enter the new last name you would like to give the admin: ")

    cur.execute(
        """UPDATE admin 
                set first_name = ?,
                last_name = ? 
                where admin_email = ?""",
        (new_first_name, new_last_name, admin_to_update),
    )

    con.commit()

    print(
        f"Staff with email {admin_to_update} now has a first name of {new_first_name} and a last name of {new_last_name}"
    )


def update_course():
    """This will let the admin update the course table"""
    course_to_update = input(
        "Please enter the id of the course you would like to update: "
    )

    new_course_name = input("Please enter the new name of the course: ")

    cur.execute(
        """UPDATE course
                set course_name = ?
                where course_id = ?""",
        (new_course_name, course_to_update),
    )

    con.commit()

    print(f"Course with id {course_to_update} now has the name {new_course_name}")


def update_module():
    """This will let the admin update the module table"""
    module_to_update = input(
        "Please enter the id of the module you would like to update: "
    )

    new_module_name = input("Please enter the new name of the module: ")
    new_module_day = input("Please enter the day the module will be on: ")
    new_event_type = input(
        "Enter 1 if this is an in person event or enter 2 if it is a zoom event: "
    )
    while new_event_type not in ["1", "2"]:
        new_event_type = input(
            "Error: You must enter 1 for an in person event or 2 for a zoom event: "
        )
    if new_event_type == "1":
        new_event_type = "In Person Lecture"
    else:
        new_event_type = "Zoom Lecture"
    new_start_time = input("Please enter the start time of the module: ")
    new_end_time = input("Please enter the end time of the module: ")

    cur.execute(
        """UPDATE module
                set module_name = ?, module_day = ?, event_type = ?, start_time = ?, end_time = ?
                where module_id = ?""",
        (
            new_module_name,
            new_module_day,
            new_event_type,
            new_start_time,
            new_end_time,
            module_to_update,
        ),
    )

    con.commit()

    print(
        f"""Module with id {module_to_update} now has the name {new_module_name} will be on {new_module_day},
            it will start at {new_start_time} and end at {new_end_time}. This is a {new_event_type} module."""
    )


# I don't think letting the admin update the room would be a good idea because the key is the only attribute
def update_room():
    """This will let the admin update the room"""

    room_to_update = input("Enter the id of the room you want to update: ")
    new_id = input("Enter the new id of the room: ")

    cur.execute(
        """UPDATE room
                set room_id = ?
                where room_id = ?""",
        (new_id, room_to_update),
    )
    con.commit()

    print(f"Room with id {room_to_update}, now has id {new_id}")


def update_user():
    """This will let the admin update the user table"""
    user_to_update = input("Enter the email of the user you would like to update: ")
    new_password = collect_and_hash_password()
    new_account_type = collect_account_type()

    cur.execute(
        """UPDATE user set user_password = ?, user_type = ? where user_email = ?""",
        (new_password, new_account_type, user_to_update),
    )
    con.commit()

    print(
        f"User with email {user_to_update} has a new password and is now an account type {new_account_type}"
    )


def update_course_enrollment():
    """This function will let the admin update enrollment"""

    student = input(
        "Enter the email of the student whose enrollment status you want to update: "
    )

    cur.execute(
        "SELECT course_id from course_enrollment where student_email = ?", (student,)
    )
    table = cur.fetchall()
    print(f"Student with email {student} is enrolled in: ")
    for index in enumerate(table):
        print(index[1])

    course = input("Enter the ID of the course you would like to change: ")
    new_course = input(
        "Enter the ID of the new course you want to replace with the old course: "
    )

    cur.execute(
        "UPDATE course_enrollment set course_id = ? where student_email = ? and course_id = ?",
        (new_course, student, course),
    )
    con.commit()

    print(
        f"Student with email {student} is no longer enrolled in {course} and is now enrolled in {new_course}"
    )


def update_course_modules():
    """This function will let the admin update the course modules table"""

    course = input("Enter the id of the course you want to update: ")

    cur.execute("SELECT module_id from course_modules where course_id = ?", (course,))
    table = cur.fetchall()
    print(f"Course with id {course} has the modules: ")
    for index in enumerate(table):
        print(index[1])

    module = input("Enter the id of the module you want to replace: ")
    new_module = input(f"Enter the id of the module you to add instead of {module}: ")

    cur.execute(
        "UPDATE course_modules set module_id = ? where course_id = ? and module_id = ?",
        (new_module, course, module),
    )
    con.commit()

    print(
        f"Course with id {course} no longer includes module {module} and now includes module {new_module}"
    )


def update_module_rooms():
    """This will let the admion ui[date the module_rooms table"""

    module = input("Enter the id of the module that you want to change the room: ")

    cur.execute("SELECT room_id from module_rooms where module_id = ?", (module,))
    table = cur.fetchall()
    print(f"Module with id {module} currently takes place in: {table[0]}")

    new_room = input(
        "Enter the id of the room you would like module {module} to take place in: "
    )

    cur.execute(
        "UPDATE module_rooms set room_id = ? where module_id = ?", (new_room, module)
    )
    con.commit()

    print(f"Module with id {module} now takes place in {new_room}.")


def update_staff_modules():
    """This will let the admin update the staff_modules table"""
    staff = input("Enter the email of the staff you want to update: ")

    cur.execute("SELECT module_id from staff_modules where staff_email = ?", (staff,))
    table = cur.fetchall()
    print(f"Staff with email {staff} is currently teaching modules: ")
    for index in enumerate(table):
        print(index[1])

    module = input("Enter the id of the module you want to change: ")
    new_module = input(f"Enter the id of the module you would like {staff} to teach: ")

    cur.execute(
        "UPDATE staff_modules set module_id = ? where staff_email = ? and module_id = ?",
        (new_module, staff, module),
    )
    con.commit()

    print(
        f"Staff with email {staff} no longer teaches module {module} and now teaches module {new_module}"
    )


# These are the delete functions for the admin


def delete_student():
    """This function will let the admin delete a student"""

    student = input("Enter the email of the student you want to delete: ")

    cur.execute("DELETE FROM student where student_email = ?", (student,))
    cur.execute("DELETE FROM course_enrollment where student_email = ?", (student,))
    con.commit()

    print(f"Student with the email {student} was deleted from the database. ")


def delete_staff():
    """This will let the admin delete a staff"""

    staff = input("Enter the email of the staff you want to delete: ")

    cur.execute("DELETE FROM staff where staff_email = ?", (staff,))
    cur.execute("DELETE FROM staff_modules where staff_email = ?", (staff,))
    con.commit()

    print(f"Staff with the email {staff} was deleted from the database. ")


def delete_admin():
    """This will let the admin delete an admin"""

    admin = input("Enter the email of the admin you want to delete: ")

    cur.execute("DELETE FROM admin where admin_email = ?", (admin,))
    con.commit()

    print(f"Admin with the email {admin} was deleted from the database. ")


def delete_user():
    """This will let the admin delete a user"""

    # Later you may want to make it to where the user being deleted will
    # also delte the admin/student/staff and all associated data

    user = input("Enter the email of the user you want to delete: ")

    cur.execute("DELETE FROM user where user_email = ?", (user,))
    con.commit()

    print(f"User with the email {user} was deleted from the database. ")


def delete_course():
    """This will let the admin delete a course"""

    course = input("Enter the id of the course you want to delete: ")

    cur.execute("DELETE FROM course where course_id = ?", (course,))
    cur.execute("DELETE FROM course_enrollment where course_id = ?", (course,))
    cur.execute("DELETE FROM course_modules where course_id = ?", (course,))
    con.commit()

    print(f"Course with the id {course} was deleted from the database. ")


def delete_module():
    """This will let an admin delete a module"""

    module = input("Enter the id of the module you want to delete: ")

    cur.execute("DELETE FROM module where module_id = ?", (module,))
    cur.execute("DELETE FROM module_rooms where module_id = ?", (module,))
    cur.execute("DELETE FROM course_modules where module_id = ?", (module,))
    con.commit()

    print(f"Course with the id {module} was deleted from the database. ")


def delete_room():
    """This will let an admin delete a room"""

    room = input("Enter the id of the room you would like to delete: ")

    cur.execute("DELETE FROM room where room_id = ?", (room,))
    cur.execute("DELETE FROM module_rooms where room_id = ?", (room,))
    con.commit()

    print(f"Room with the id {room} was deleted from the database. ")
