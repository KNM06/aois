import unittest
from source.Lab3Synthesizer import Lab3Synthesizer


class TestLab3Synthesizer(unittest.TestCase):
    def setUp(self):
        self.synth = Lab3Synthesizer()

    def test_synthesize_ods3(self):
        result = self.synth.synthesize_ods3()
        self.assertIsInstance(result, dict)
        self.assertIn("S", result)
        self.assertIn("P_out", result)
        self.assertIsInstance(result["S"], str)

    def test_synthesize_gray_bcd_adder(self):
        result = self.synth.synthesize_gray_bcd_adder()
        self.assertIsInstance(result, dict)
        for key in ["P_out", "S3", "S2", "S1", "S0"]:
            self.assertIn(key, result)
            self.assertIsInstance(result[key], str)

    def test_synthesize_down_counter(self):
        result = self.synth.synthesize_down_counter()
        self.assertIsInstance(result, dict)
        for key in ["T2", "T1", "T0"]:
            self.assertIn(key, result)
            self.assertIsInstance(result[key], str)
