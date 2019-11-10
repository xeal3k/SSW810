import unittest
from prettytable import PrettyTable

class TestHW9(unittest.TestCase):
    def test_student(self):
        stfile = "students.txt"
        gdfile = "grades.txt"
        st = student(stfile, gdfile)
        st.analyze_files()
        self.assertEqual(len(st.info), 10)
        self.assertEqual(st.info[0][0], "10103")

    def test_instructor(self):
        insfile = "instructors.txt"
        gdfile = "grades.txt"
        ins = instructor(insfile, gdfile)
        ins.analyze_files()
        self.assertEqual(len(ins.info), 12)
        self.assertEqual(ins.info[0][0], "98765")
        self.assertEqual(ins.info[1][1], "Einstein, A")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity = 2)
