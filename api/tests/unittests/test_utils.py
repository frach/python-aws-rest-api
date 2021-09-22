from unittest import TestCase

from utils import convert_to_kebab_case


class UtilsTestCase(TestCase):
    def test_convert_to_kebab_case_default_character(self):
        self.assertEqual(convert_to_kebab_case('Simple transformation test'), 'simple-transformation-test')
        self.assertEqual(convert_to_kebab_case('Multiple     spaces   test'), 'multiple-spaces-test')
        self.assertEqual(convert_to_kebab_case('     Outside spaces test       '), 'outside-spaces-test')
        self.assertEqual(convert_to_kebab_case('$PECI4! Ch@r4ct3r$ test'), '$peci4!-ch@r4ct3r$-test')

    def test_convert_to_kebab_case_different_character(self):
        self.assertEqual(convert_to_kebab_case('simple test', join_character='{'), 'simple{test')
        self.assertEqual(convert_to_kebab_case('simple test', join_character=' '), 'simple test')
