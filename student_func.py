import sqlite3
from utility_func import strip_tuple

# This is the two view queries for the student to use


# I'm opening my connection to the database
con = sqlite3.connect("UoM.db")
cur = con.cursor()


def view_courses_for_students(student_email):
    """This will let a student see the courses they're enrolled in"""
    cur.execute(
        "SELECT course_id from course_enrollment where student_email = ?",
        (student_email,),
    )
    table = cur.fetchall()
    print("You are enrolled in the following courses: ")
    for index in enumerate(table):
        print(strip_tuple(index[1]))


def view_modules_for_students(student_email):
    """This will let a student see the modules they're enrolled in and info on the module"""
    cur.execute(
        "SELECT course_id from course_enrollment where student_email = ?",
        (student_email,),
    )
    table = cur.fetchall()
    for index in enumerate(table):

        course_stripped = strip_tuple(index[1])

        print(
            f"You are enrolled in {course_stripped} course. {course_stripped} contains the following modules: "
        )

        cur.execute(
            """SELECT module.module_id, module.module_name, module.module_day,
                    module.event_type, module.start_time, module.end_time
                    from module
                    inner join course_modules
                    on module.module_id = course_modules.module_id
                    where course_modules.course_id = ? """,
            (course_stripped,),
        )

        mod = cur.fetchall()

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
