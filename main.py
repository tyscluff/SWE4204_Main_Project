# Author: Tyson Cluff
# FoS4204

# The purpose of this program is to allow users to create, view, update,
# and delete data related to students, lecturers, courses, and modules at
# an imaginary university. There will be three kinds of users, student,
# staff, and adminstrator. Each user will be given different kinds of
# authorization for what they are allowed to do in the program.


# Import my dependecies
import sqlite3
import bcrypt
import getpass

# Import my functions
from admin_func import *
from login_func import *
from user_options_fun import *

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


create_user_table()


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


create_student_table()


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


create_staff_table()


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


create_admin_table()


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


create_course_table()


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


create_module_table()


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


create_room_table()

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


create_course_modules_table()


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


create_staff_modules_table()


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


create_module_rooms_table()

# This is going to be the start of the user interaction with the program

# This will greet the user and explain the program


def greeting():
    """Greet the user"""
    print(
        """Hi welcome the University of Mordor records system.
You will be able to user your university login to interact
with records related to your role in the university!"""
    )


# function to give user options based on account_type


def user_options(account_type: str, user_email: str):
    """This lets the user see and select what they want to do in the program"""
    if account_type == "student":
        while True:
            is_student(user_email)
            go_again = input(
                "Would you like to view more records? Enter 1 to go again or 2 to end: "
            )
            while go_again not in ["1", "2"]:
                go_again = input(
                    "You must enter 1 to use the program again or 2 to end: "
                )
            if go_again == "2":
                print("Thanks for using! Bye bye")
                exit()

    elif account_type == "staff":
        while True:
            is_staff(user_email)
            go_again = input(
                "Would you like to view more records? Enter 1 to go again or 2 to end: "
            )
            while go_again not in ["1", "2"]:
                go_again = input(
                    "You must enter 1 to use the program again or 2 to end: "
                )
            if go_again == "2":
                print("Thanks for using! Bye bye")
                exit()
    elif account_type == "admin":
        while True:
            is_admin()
            go_again = input(
                "Would you like to view more records? Enter 1 to go again or 2 to end: "
            )
            while go_again not in ["1", "2"]:
                go_again = input(
                    "You must enter 1 to use the program again or 2 to end: "
                )
            if go_again == "2":
                print("Thanks for using! Bye bye")
                exit()


# Order of the functions

greeting()

user = login_user()

user_email = user[0][0]
user_password = user[0][1]
user_account_type = user[0][2]

user_options(user_account_type, user_email)

con.close()
