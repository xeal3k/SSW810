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

