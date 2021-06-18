from main import *
import unittest

class ChunkerTest(unittest.TestCase):

    def test_start(self):
        chunker = Chunker("SEASTATE NO    [0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
        result = chunker.start("SEASTATE NO    1")
        self.assertTrue(result)

    def test_stop(self):
        chunker = Chunker("SEASTATE NO    [0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
        result = chunker.finish("       MAXIMUM BASE SHEAR         = 1.4244E+05  AT PHASE =   10.0")
        self.assertTrue(result)

    def test_getChunks(self):
        chunker = Chunker("SEASTATE NO    [0-9]", "MAXIMUM BASE SHEAR", "WAJAC.LIS")
        chunker.processFile()
        result = chunker.getChunks()
        print("hey")

if __name__ == '__main__':
    unittest.main()
