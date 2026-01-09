import unittest

from progress_track import ticks_to_progress, progress_to_ticks

class ProgressTest(unittest.TestCase):
    def test_ticks_to_progress_1(self):
        return self.assertEqual(ticks_to_progress(5), (1,1))
    
    def test_ticks_to_progress_2(self):
        return self.assertEqual(ticks_to_progress(14), (3,2))
    
    def test_ticks_to_progress_3(self):
        return self.assertEqual(ticks_to_progress(16), (4,0))
    
    def test_ticks_to_progress_4(self):
        return self.assertEqual(ticks_to_progress(19), (4,3))
    
    def test_ticks_to_progress_5(self):
        return self.assertEqual(ticks_to_progress(0), (0,0))
    
    def test_ticks_to_progress_6(self):
        return self.assertEqual(ticks_to_progress(1), (0,1))
    
    def test_ticks_to_progress_7(self):
        return self.assertEqual(ticks_to_progress(2), (0,2))
    
    def test_ticks_to_progress_8(self):
        return self.assertEqual(ticks_to_progress(3), (0,3))
    
    def test_ticks_to_progress_9(self):
        return self.assertEqual(ticks_to_progress(4), (1,0))
    
    def test_progress_to_ticks_1(self):
        assert progress_to_ticks(1) == 4
    
    def test_progress_to_ticks_2(self):
        assert progress_to_ticks(0) == 0

    def test_progress_to_ticks_3(self):
        assert progress_to_ticks(10) == 40