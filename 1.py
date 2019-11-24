from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

"""
the instructors page, use sql to get the data from hw 11
"""
@app.route('/instructors')
def instructor():
    db = sqlite3.connect("810.db")
    query = """SELECT i.CWID, i.Name, i.Dept, g.Course, count(g.course) from instructors i
                    JOIN grades g on i.CWID == g.InstructorCWID group by g.Course, i.Name"""
    data = [{'cwid': cwid, 'name': name, 'department': department, 'course': course, 'students': students}
            for cwid, name, department, course, students in db.execute(query)]
    return render_template('ins.html',
                            my_header = "Stevens Repository",
                            table_title = "Course and student counts",
                            instructors = data)

app.run(debug = True)
