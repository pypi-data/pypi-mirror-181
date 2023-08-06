from project.celebrities_births import Date
from hypothesis import given
import hypothesis.strategies as st
import unittest

class Test_celebities_birth(unittest.TestCase):
    
    def setUp(self):
        self.date = Date(5,8,2014)
        
    @given(st.integers().filter(lambda x: x > 1900 and x < 2100))
    def test_is_leap_year(self, yyyy):
        expected_value = yyyy % 4 == 0
        actual_value = self.date.is_leap_year(yyyy)
        self.assertEqual(expected_value,actual_value)
        
    def test_from_string(self):
        date_1 = "25-5-2004"
        expected_value = 5
        self.assertEqual(expected_value,Date.from_string(date_1).month)
        
unittest.main(argv= [""], verbosity= 2, exit=False)
    