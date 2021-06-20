from main import *
import unittest

class Tests(unittest.TestCase):

    def test_start(self):
        chunker = Chunker("SEASTATE NO[ ]{2,}[0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
        result = chunker.start("SEASTATE NO   15")
        self.assertTrue(result)

    def test_stop(self):
        chunker = Chunker("SEASTATE NO[ ]{2,}[0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
        result = chunker.finish("       MAXIMUM BASE SHEAR         = 1.4244E+05  AT PHASE =   10.0")
        self.assertTrue(result)

    def test_getChunks(self):
        chunker = Chunker("SEASTATE NO[ ]{2,}[0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
        chunker.processFile()
        result = chunker.getChunks()
        self.assertEqual(18, len(result))

    def test_processLine(self):
        dataExtractor = TextDataExtractor(" ", "^\s*\S+(?:\s+\S+){7,7}\s*$")
        dataExtractor.processLine("         23    110.0     -1.2629E+04     1.0099E+04    -1.4177E+04    -4.4921E+08    -1.0126E+09    -3.2000E+08")
        print("hey")

   
if __name__ == '__main__':
    unittest.main()
