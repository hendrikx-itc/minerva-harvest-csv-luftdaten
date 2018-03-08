import parser_aireas as parser
import unittest
import io
import datetime

class ParserTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.data = open("../../test_data/measurements-2018-03-06.csv")
        
    def setUp(self):
        self.parser = parser.Parser(None)

    def test_stupid(self):
        rows = []
        for resultpart in self.parser.load_packages(ParserTest.data, "name"):
            rows += resultpart.rows
            
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ParserTest)

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
