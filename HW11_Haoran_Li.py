from prettytable import PrettyTable
def file_reading_gen(filename, field, sep, header = False):
    """
    read file first, then read each line and use generator
    """
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        raise FileNotFoundError(str(filename) + " File Not Found")

    num_line = 1
    if header == True:
        line = file.readline()
        num_line += 1

    while True:
        line = file.readline()
        if not line:
            break
        if line.count(sep)+1 != field:
            raise  ValueError(filename + " has " + str(line.count(sep)+1) + " fields on line " + str(num_line) + " but expected 4")
        line = line.split(sep)
        num_line += 1
        yield (line[i] for i in range(field))

    file.close()

class Major():
    def __init__(self, coursefile):
        self.namefile = coursefile
        self.info = {}

    def analyze_files(self):

        info = {}
        for major, status, course in file_reading_gen(self.namefile, 3, sep='\t', header = True):
            if major not in info:
                info[major] = {"r":[], "e":[]}
            if course.endswith("\n"):
                course = course[:-1]
            if status == "R":
                info[major]["r"].append(course)
            else:
                info[major]["e"].append(course)

        self.info = info

    def pretty_print(self):

        x = PrettyTable()
        x.field_names = ["Major", "Required", "Elective"]
        self.analyze_files()

        for item in self.info:
            x.add_row([item, self.info[item]["r"], self.info[item]["e"]])

        print(x)

class Student():
    """
    student class, include all the info include cwid, name, course enrolled and grade for that course
    """
    def __init__(self, namefile, gradefile, majorfile):
        self.namefile = namefile
        self.gradefile = gradefile
        self.majorfile = majorfile
        self.info = []

    def analyze_files(self):

        info = []
        for cwid, name, major in file_reading_gen(self.namefile, 3, sep='\t', header = True):
            grades = {}
            for ncwid, course, grade, instructor in file_reading_gen(self.gradefile, 4, sep='\t'):
                if cwid == ncwid:
                    if grade in ["A", "A-", "B+", "B", "B-", "C+", "C"]:
                        grades[course] = grade
                if major.endswith("\n"):
                    major = major[:-1]
            info.append([cwid, name, major, grades])

        self.info = info

    def pretty_print(self):

        x = PrettyTable()
        x.field_names = ["Cwid", "Name", "Major", "Completed course", "Remaining Required", "Remaining Elective"]
        major = Major(self.majorfile)
        major.analyze_files()
        self.analyze_files()


        for item in self.info:
            rr = []
            re = []
            sorted_course = sorted(key for key in item[3])

            for c in major.info:
                if c == item[2]:
                    for rc in major.info[c]["r"]:
                        if rc not in sorted_course:
                            rr.append(rc)
                    for ec in major.info[c]["e"]:
                        if ec in sorted_course:
                            re = []
                            break
                        re.append(ec)

            x.add_row([item[0], item[1], item[2], sorted_course, rr, re])

        print(x)

class Instructor():
    """
    instructor class, include all the info of instructor, cwid, name, department, course taught and numbers of enrollment
    """
    def __init__(self, namefile, gradefile):
        self.namefile = namefile
        self.gradefile = gradefile
        self.info = []

    def analyze_files(self):

        info = []
        for cwid, name, major in file_reading_gen("instructors.txt", 3, sep='\t'):
            dic = {}
            for ncwid, course, grade, instructor in file_reading_gen("grades.txt", 4, sep='\t', header = True):
                if cwid == instructor[:5]:
                    if course not in dic:
                        dic[course] = 0
                    dic[course] += 1
                if major.endswith("\n"):
                    major = major[:-1]
            for item in dic:
                info.append([cwid, name, major, item, dic[item]])

        self.info = info

    def pretty_print(self):

        x = PrettyTable()
        x.field_names = ["Cwid", "Name", "Department", "Course", "Students"]
        self.analyze_files()

        for item in self.info:
            x.add_row([item[0], item[1], item[2], item[3], item[4]])

        print(x)
        return x

import sqlite3
class Repository():
    """
    repository class, include school name,  the info of both students and instructors
    """
    def __init__(self, path):
        self.stfile = path + "/students.txt"
        self.gdfile = path + "/grades.txt"
        self.insfile = path + "/instructors.txt"
        self.mjsfile = path + "/majors.txt"
        self.stinfo = []
        self.insinfo = []

    def analyze_files(self):
        st = Student(self.stfile, self.gdfile, self.mjsfile)
        ins = Instructor(self.insfile, self.gdfile)
        st.analyze_files()
        self.stinfo = st.info
        ins.analyze_files()
        self.insinfo = ins.info

    def pretty_print(self):
        mj = Major(self.mjsfile)
        st = Student(self.stfile, self.gdfile, self.mjsfile)
        ins = Instructor(self.insfile, self.gdfile)
        mj.pretty_print()
        st.pretty_print()
        ins.pretty_print()

    def instructor_table_db(self, db_path):
        db = sqlite3.connect(db_path)
        x = PrettyTable()
        x.field_names = ["Cwid", "Name", "Department", "Course", "Students"]
        query = """SELECT i.CWID, i.Name, i.Dept, g.Course, count(g.course) from instructors i
                    JOIN grades g on i.CWID == g.InstructorCWID group by g.Course, i.Name"""
        for item in db.execute(query):
            x.add_row([item[0], item[1], item[2], item[3], item[4]])
        print(x.get_string())
        return x

def main():
    """
    main function, read files and create repository
    """
    repo = Repository("stevens")

    repo.pretty_print()
        
main()
