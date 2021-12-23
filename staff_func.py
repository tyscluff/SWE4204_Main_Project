import sqlite3
from utility_func import strip_tuple

# These are the queries someone with staff access can make

# I'm opening my connection to the database
con = sqlite3.connect("UoM.db")
cur = con.cursor()


def view_courses_staff(user_email):
    """This will let a staff see data about courses they're involved in"""

    print("You will now see the courses that you teach modules in: ")

    cur.execute(
        """SELECT DISTINCT course_modules.course_id 
                from course_modules
                inner join staff_modules
                on course_modules.module_id = staff_modules.module_id
                where staff_modules.staff_email = ?""",
        (user_email,),
    )
    table = cur.fetchall()

    print("You teach modules in the following courses: ")
    for index in enumerate(table):
        course = strip_tuple(index[1][0])

        print(course)


def view_modules_staff(user_email):
    """This function will let a staff see data on the modules they are teaching"""

    cur.execute(
        """SELECT module.module_id, module.module_name, module.module_day,
                    module.event_type, module.start_time, module.end_time
                    from module
                    inner join staff_modules
                    on module.module_id = staff_modules.module_id
                    where staff_modules.staff_email = ?""",
        (user_email,),
    )

    mod = cur.fetchall()

    print("You teach the following modules: ")

    for index in enumerate(mod):
        id = strip_tuple(index[1][0])
        name = strip_tuple(index[1][1])
        event_type = strip_tuple(index[1][2])
        start_time = strip_tuple(index[1][3])
        end_time = strip_tuple(index[1][4])

        print(
            f"""
        Module Id: {id}
        Module Name: {name}
        Event Type: {event_type}
        Start Time: {start_time}
        End Time: {end_time}
        """
        )


def view_staff_staff():
    """This will let the staff view info on all the staff"""

    print("You will now see info on all the staff: ")

    cur.execute("SELECT * from staff")
    table = cur.fetchall()

    for index in enumerate(table):
        email = strip_tuple(index[1][0])
        first_name = strip_tuple(index[1][1])
        last_name = strip_tuple(index[1][2])

        print(
            f"""
            Staff Email: {email}
            First Name: {first_name}
            Last Name: {last_name}"""
        )


def view_rooms_staff():
    """This will let the staff view rooms and what module is in them"""

    print("You will now see all rooms and what modules they contain: ")

    cur.execute("SELECT * from module_rooms")
    table = cur.fetchall()

    for index in enumerate(table):
        module = strip_tuple(index[1][0])
        room = strip_tuple(index[1][1])

        print(
            f"""
            Module: {module}
            Room: {room}"""
        )


def view_students_staff(user_email):
    """This will let staff see info on students they teach"""

    cur.execute(
        """SELECT DISTINCT student.student_email, student.first_name,
                student.last_name
                from (((course_enrollment
                inner join student on student.student_email = course_enrollment.student_email)
                inner join course_modules on course_enrollment.course_id = course_modules.course_id)
                inner join staff_modules on course_modules.module_id = staff_modules.module_id)
                where staff_modules.staff_email = ?""",
        (user_email,),
    )
    table = cur.fetchall()

    print("You teach the following students: ")

    for index in enumerate(table):
        email = strip_tuple(index[1][0])
        first_name = strip_tuple(index[1][1])
        last_name = strip_tuple(index[1][2])

        print(
            f"""
            Email: {email}
            First Name: {first_name}
            Last Name: {last_name}"""
        )
