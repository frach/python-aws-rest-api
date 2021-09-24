from unittest import TestCase

from utils import convert_to_kebab_case, remove_keys_from_dumped_json


class UtilsTestCase(TestCase):
    def test_convert_to_kebab_case_default_character(self):
        self.assertEqual(convert_to_kebab_case('Simple transformation test'), 'simple-transformation-test')
        self.assertEqual(convert_to_kebab_case('Multiple     spaces   test'), 'multiple-spaces-test')
        self.assertEqual(convert_to_kebab_case('     Outside spaces test       '), 'outside-spaces-test')
        self.assertEqual(convert_to_kebab_case('$PECI4! Ch@r4ct3r$ test'), '$peci4!-ch@r4ct3r$-test')

    def test_convert_to_kebab_case_different_character(self):
        self.assertEqual(convert_to_kebab_case('simple test', join_character='{'), 'simple{test')
        self.assertEqual(convert_to_kebab_case('simple test', join_character=' '), 'simple test')

    def test_remove_keys_from_dumped_json(self):
        # Removing existing keys
        self.assertEqual(remove_keys_from_dumped_json('{"a": "b", "c": "d", "e": "f"}', ['c', 'e']), '{"a": "b"}')

        # Removing non-existing keys
        self.assertEqual(remove_keys_from_dumped_json('{"a": "b"}', ['c', 'e']), '{"a": "b"}')

        # Wrong input (dict instead of dumped dict)
        with self.assertRaises(TypeError), self.assertLogs() as logs:
            remove_keys_from_dumped_json({'a': 'b'}, ['a'])

        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].levelname, 'ERROR')
        self.assertEqual(logs.records[0].getMessage(), "Failed to load JSON. Input data: {'a': 'b'}")
