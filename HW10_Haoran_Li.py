#!/usr/bin/env python
# coding: utf-8

# In[26]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


# In[27]:


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


# In[32]:


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
        
a = Major("majors.txt")
a.pretty_print()    


# In[50]:


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
        for cwid, name, major in file_reading_gen(self.namefile, 3, sep='\t'):
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
                
a = Student("students.txt", "grades.txt", "majors.txt")
a.analyze_files()
a.pretty_print()


# In[57]:


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
            for ncwid, course, grade, instructor in file_reading_gen("grades.txt", 4, sep='\t'):
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
        
a = Instructor("students.txt", "grades.txt")
a.analyze_files()
a.pretty_print()


# In[48]:


class Repository():
    """
    repository class, include school name,  the info of both students and instructors
    """
    def __init__(self, university, stfile, gdfile, insfile, mjsfile):
        self.university = university
        self.stfile = stfile
        self.gdfile = gdfile
        self.insfile = insfile
        self.mjsfile = mjsfile
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


# In[49]:


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
        
    mjsfile = input("enter major file ")
    try: 
        file = open(insfile, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")
    
    repo = Repository(school_name, stfile, gdfile, insfile, mjsfile)
    
    repo.pretty_print()
    
    
main()


# In[64]:


from prettytable import PrettyTable
import unittest
class TestHW9(unittest.TestCase):
    def test_student(self):
        stfile = "students.txt"
        gdfile = "grades.txt"
        majorfile = "majors.txt"
        st = Student(stfile, gdfile, majorfile)
        st.analyze_files()
        self.assertEqual(len(st.info), 10)
        self.assertEqual(st.info[0][0], "10103")
    
    def test_instructor(self):
        insfile = "instructors.txt"
        gdfile = "grades.txt"
        ins = Instructor(insfile, gdfile)
        ins.analyze_files()
        self.assertEqual(len(ins.info), 12)
        self.assertEqual(ins.info[0][0], "98765")
        self.assertEqual(ins.info[1][1], "Einstein, A")
        
    def test_major(self):
        majorfile = "majors.txt"
        mj = Major(majorfile)
        mj.analyze_files()
        self.assertEqual(len(mj.info), 2)
        self.assertEqual(len(mj.info["SFEN"]["r"]), 4)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity = 2)


# In[ ]:




