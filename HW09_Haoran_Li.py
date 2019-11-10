from prettytable import PrettyTable
def file_reading_gen(filename, field, sep, header = False):
    """
    read file first, then read each line and use generator
    """
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")

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

class student():
    """
    student class, include all the info include cwid, name, course enrolled and grade for that course
    """
    def __init__(self, namefile, gradefile):
        self.namefile = namefile
        self.gradefile = gradefile
        self.info = []

    def analyze_files(self):

        info = []
        for cwid, name, major in file_reading_gen(self.namefile, 3, sep='\t'):
            grades = {}
            for ncwid, course, grade, instructor in file_reading_gen(self.gradefile, 4, sep='\t'):
                if cwid == ncwid:
                    if grade:
                        grades[course] = grade
            info.append([cwid, name, grades])

        self.info = info

    def pretty_print(self):

        x = PrettyTable()
        x.field_names = ["Cwid", "Name", "Completed course"]
        self.analyze_files()

        for item in self.info:
            x.add_row([item[0], item[1], sorted(key for key in item[2])])

        print(x)

class instructor():
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
            for ncwid, course, grade, instructor in file_reading_gen("grades.txt", 4, sep='\t'):
                if cwid == instructor[:5]:
                    if course not in dic:
                        dic[course] = 0
                    dic[course] += 1
            #print(dic)
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

class repository():
    """
    repository class, include school name,  the info of both students and instructors
    """
    def __init__(self, university, stfile, gdfile, insfile):
        self.university = university
        self.stfile = stfile
        self.gdfile = gdfile
        self.insfile = insfile
        self.stinfo = []
        self.insinfo = []

    def analyze_files(self):
        st = student(self.stfile, self.gdfile)
        ins = instructor(self.insfile, self.gdfile)
        st.analyze_files()
        self.stinfo = st.info
        ins.analyze_files()
        self.insinfo = ins.info

    def pretty_print(self):
        st = student(self.stfile, self.gdfile)
        ins = instructor(self.insfile, self.gdfile)
        st.pretty_print()
        ins.pretty_print()

def main():
    """
    main function, read files and create repository
    """
    school_name = input("Enter school name: ")

    stfile = input("enter student file ")
    try:
        file = open(stfile, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")

    gdfile = input("enter grade file ")
    try:
        file = open(gdfile, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")

    insfile = input("enter instructor file ")
    try:
        file = open(insfile, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")

    repo = repository(school_name, stfile, gdfile, insfile)

    repo.pretty_print()

main()
