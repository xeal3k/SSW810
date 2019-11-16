from prettytable import PrettyTable
import unittest
class TestHW11(unittest.TestCase):
    def test_instructor_table_db(self):
        path = "stevens"
        database = "810.db"
        repo = Repository("stevens")
        tb = repo.instructor_table_db(database)
        self.assertEqual(len(tb.get_string()), 569)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity = 2)
