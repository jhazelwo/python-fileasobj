""" -*- coding: utf-8 -*-
Feel free to change TestFile path or name as needed but leave TestContains as it is.

Be sure fileasobj is in your Python path.

Hint:
# PYTHONPATH=`pwd` python3 tests/tests_fileasobj.py

"""
import unittest
from fileasobj import FileAsObj

TestFile = '/tmp/test_fileasobj.txt'

TestContains = """#/etc/hosts
# This is a test hosts file
#
#1
127.0.0.1 localhost.localdomain localhost

10.0.0.1 web01 web01.example.com

172.19.18.17    freebird.example.com

#comment

    #spaced comment
    # la deed da


192.168.192.168 h0stname.example.tld    h0stname
10.10.10.10     hostname.example.tld    hostname

10.2.3.4    mail01 mail01.example.tld
10.2.9.4    webmail01 webmail01.example.tld
10.2.5.2    www01   www01.example.tld
#172.8.8.8    www01   www01.example.tld
#
Checking for __contains__ functionality 123
#

# A bunch of duplicate empty comment lines....
#
#
#
#
#
#
#
"""


class TestAll(unittest.TestCase):

    def test_001_file_not_found(self):
        """
        Fail if trying to instance class for file that does not exist.
        This tests the shortcut method in __init__.
        """
        with self.assertRaises(IOError):
            FileAsObj('/this/file/does/not/exist/')

    def test_002_simple(self):
        """ Instance an empty test file and check instance type matches. """
        test_file = FileAsObj()
        test_file.filename = TestFile
        self.assertIsInstance(test_file, FileAsObj)

    def test_003_save_no_changes(self):
        """ Instance an empty test file and save to disk. """
        test_file = FileAsObj()
        test_file.filename = TestFile
        self.assertTrue(test_file.save())

    def test_004_save_with_changes(self):
        """ Instance an empty test file, overwrite its contents and save to disk. """
        test_file = FileAsObj()
        test_file.filename = TestFile
        test_file.contents = TestContains.split('\n')
        self.assertEqual(TestContains, str(test_file))
        self.assertTrue(test_file.save())

    def test_iter(self):
        """ Test __iter__ method. """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        for this in test_file:
            self.assertIsNotNone(this)

    def test_birthday(self):
        """ Ensure object has non-empty attribute `birthday` """
        test_file = FileAsObj()
        self.assertIsNotNone(test_file.birthday)

    def test_contains(self):
        """ Test __contains__ method. """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue('Checking for __contains__ functionality 123' in test_file)

    def test_not_contains(self):
        """ Test __contains__ method. """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue('a7s6d9f7a6sd9f76asf9a8d7s89d6f967adfsadf' not in test_file)

    def test_egrep_char_list(self):
        """ Test egrep with valid selector regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('h[o0]stname'))

    def test_egrep_word(self):
        """ Test egrep with a word """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('bird'))

    def test_bad_regex(self):
        """ Test egrep with invalid regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        try:
            test_file.egrep('*rd')
        except Exception as error:
            self.assertEqual('nothing to repeat', str(error))

    def test_good_regex(self):
        """ Test egrep with valid wildcard regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('.*rd'))

    def test_egrep_char_range(self):
        """ Test egrep with valid range regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('[a-z]ird'))

    def test_egrep_word_list(self):
        """ Test egrep with valid choice regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('(host|bird)'))

    def test_egrep_string_end(self):
        """ Test egrep with valid regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('tld$'))

    def test_egrep_string_start(self):
        """ Test egrep with valid regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.egrep('^10.*'))

    def test_add_with_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        self.assertTrue(test_file + 'using __add__ three times, force unique')
        self.assertFalse(test_file + 'using __add__ three times, force unique')
        self.assertFalse(test_file + 'using __add__ three times, force unique')

    def test_append_with_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        self.assertTrue(test_file.append('using __add__ three times, force unique'))
        self.assertFalse(test_file.append('using __add__ three times, force unique'))
        self.assertFalse(test_file.append('using __add__ three times, force unique'))

    def test_add_not_unique(self):
        """ Test content integrity not using `unique` """
        test_file = FileAsObj()
        self.assertTrue(test_file.add('using __add__ three times, force unique', unique=False))
        self.assertTrue(test_file.add('using __add__ three times, force unique', unique=False))
        self.assertTrue(test_file.add('using __add__ three times, force unique', unique=False))

    def test_subtract(self):
        """ Test __sub__ method """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file - '#comment')

    def test_subtract_fail(self):
        """ Test __sub__ method fails """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertFalse(test_file - 'this string does not exist in file!')

    def test_remove_multi(self):
        """ Test deleting multiple lines """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(test_file.rm(test_file.grep('#')))

    def test_replace_whole_line(self):
        """ Test substitute a line """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        old = '172.19.18.17    freebird.example.com'
        new = '172.19.18.17    freebird.example.com  # Added 1976.10.29 -jh'
        self.assertTrue(test_file.replace(old, new))

    def test_replace_regex(self):
        """ Test substitute lines using a valid regex """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        old = test_file.egrep('^[ ]+#.*')
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        self.assertFalse(test_file.egrep('^[ ]+#.*'))

    def test_replace_list(self):
        """ Test substitute lines using a list of strings """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        old = ['#', '# ', '#1']
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        for this in old:
            self.assertFalse(test_file.check(this))

    def test_count_comment_empty(self):
        """ Test __len__ method """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertEqual(len(test_file.grep('#')), 18)

    def test_string(self):
        """ Test __str__ method """
        test_file = FileAsObj()
        test_file.contents = TestContains.split('\n')
        self.assertTrue(str(test_file))

    def test_string_log_str(self):
        """ Test __str__ method of log subclass """
        test_file = FileAsObj()
        self.assertTrue(str(test_file.log))

    def test_string_log_call(self):
        """ Test __call__ method of log subclass """
        test_file = FileAsObj()
        self.assertIsNone(test_file.log('test'))

    def test_string_log_has_tag(self):
        """ Test tag attribute of log subclass """
        test_file = FileAsObj()
        self.assertTrue(str(test_file.log.tag))


if __name__ == '__main__':
    unittest.main()
