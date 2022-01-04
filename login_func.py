import sqlite3
import bcrypt
import getpass

# These are the functions for the login process

# I need to add a logout function

# I'm opening my connection to the database
con = sqlite3.connect("UoM.db")
cur = con.cursor()


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


def collect_email():
    """This function will collect the email value for create user"""
    email = input(
        "Please enter the university email of the user you would like to create: "
    )
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

        wrong_attempts = 0

        while correct_password == False and wrong_attempts < 3:
            password = (
                getpass.getpass("Wrong password try again: ").strip().encode("utf-8")
            )
            wrong_attempts += 1

        if wrong_attempts == 3:
            print("You have too many failed attempts to login. Try again later. ")
            exit()

        print(
            f"You were successfully logged in with the email: {user_email}. You have {account_type} access."
        )
    return result
