import unittest

from ingestion import change_date


class Timetest(unittest.TestCase):

    def test_time_molding(self):
        data = change_date("Mo-Fr:10AM-2PM")
        for key in data:
            if key not in ["Sa", "Su"]:
                self.assertTrue(data[key]["morning"])
                self.assertTrue(data[key]["afternoon"])
                self.assertFalse(data[key]["evening"])
                self.assertFalse(data[key]["late_night"])
            else:
                self.assertEqual(data[key], None)
        data = change_date("Fr/Sa/Su:6AM-10AM/9PM-11PM")
        for key in data:
            if key in ["Fr", "Sa", "Su"]:
                self.assertTrue(data[key]["morning"])
                self.assertFalse(data[key]["afternoon"])
                self.assertTrue(data[key]["evening"])
                self.assertTrue(data[key]["late_night"])
            else:
                self.assertEqual(data[key], None)
