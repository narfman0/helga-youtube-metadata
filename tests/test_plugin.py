import re
from unittest import TestCase

from helga_youtube_meta import plugin


class TestResults(TestCase):
    def test_parse_duration(self):
        # mostly just syntax checking *shrugs*
        duration = plugin.parse_duration('P5DT6H')
        self.assertEqual('5', duration[0])

    def test_match(self):
        # simply test some easy use cases
        regex = re.compile(plugin.MATCH_REGEX)
        def grab(test_string):
            # extract match from string
            return regex.search(test_string).group(1)
        self.assertEqual('abcdef', grab('https://www.youtube.com/watch?v=abcdef'))
        self.assertEqual('abcdef', grab('https://www.youtube.com/watch?time_continue=42&v=abcdef'))
        self.assertEqual('abcdef', grab('https://youtu.be/abcdef'))
        self.assertEqual('abcdef', grab('https://youtu.be/abcdef?t=17s'))
