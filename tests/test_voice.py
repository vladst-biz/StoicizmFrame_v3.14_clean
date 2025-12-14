# -*- coding: utf-8 -*-
import unittest
from src.voice_adapter import adapt_voice

class TestVoiceAdapter(unittest.TestCase):
    def test_adapt_voice(self):
        result = adapt_voice("input.mp3", "output.mp3")
        self.assertEqual(result, "output.mp3")

if __name__ == "__main__":
    unittest.main()
