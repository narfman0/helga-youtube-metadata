from unittest import TestCase

from helga_youtube_meta import plugin


class TestResults(TestCase):
    def test_parse_duration(self):
        # mostly just syntax checking *shrugs*
        duration = plugin.parse_duration('P5DT6H')
        self.assertEqual('5', duration[0])
