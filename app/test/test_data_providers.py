import unittest
import urllib2


class DataTest(unittest.TestCase):

    def test_working_url(self):
        url = "https://data.sfgov.org/api/views/px6q-wjh5/rows.csv?accessType=DOWNLOAD"
        response = urllib2.urlopen(url)
        self.assertEqual(response.code, 200)
