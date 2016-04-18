""" -*- coding: utf-8 -*-
Unit tests for FileAsObj.
Testing saves lives!

Feel free to change TESTFILE path or name as needed but leave TESTCONTENTS as it is.

Be sure fileasobj is in your Python path.

Hint:
# PYTHONPATH=`pwd` python3 tests/tests_fileasobj.py

"""
import unittest
from fileasobj import FileAsObj

TESTFILE = '/tmp/test_fileasobj.txt'

TESTCONTENTS = """#/etc/hosts
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
Checking for __contains__ functionality.
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

    def test_file_not_found(self):
        """
        Fail if trying to instance class for file that does not exist.
        This tests the shortcut method in __init__.
        """
        with self.assertRaises(IOError):
            FileAsObj('/this/file/does/not/exist/')

    def test_simple(self):
        """ Instance an empty test file and check instance type matches. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        self.assertIsInstance(test_file, FileAsObj)

    def test_save_no_changes(self):
        """ Instance an empty test file and save to disk. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        self.assertTrue(test_file.save())

    def test_save_with_changes(self):
        """ Instance an empty test file, overwrite its contents and save to disk. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertEqual(TESTCONTENTS, str(test_file))
        self.assertTrue(test_file.save())

    def test_iter(self):
        """ Test __iter__ method. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        for this in test_file:
            self.assertIsNotNone(this)

    def test_birthday(self):
        """ Ensure object has non-empty attribute `birthday` """
        test_file = FileAsObj()
        self.assertIsNotNone(test_file.birthday)

    def test_contains(self):
        """ Test __contains__ method. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue('Checking for __contains__ functionality.' in test_file)

    def test_not_contains(self):
        """ Test __contains__ method. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue('95bf5dd7096c3552063e4187b4194b1f' not in test_file)

    def test_egrep_char_list(self):
        """ Test egrep with valid selector regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('h[o0]stname'))

    def test_egrep_word(self):
        """ Test egrep with a word """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('bird'))

    def test_bad_regex(self):
        """ Test egrep with invalid regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        try:
            test_file.egrep('*rd')
        except Exception as error:
            self.assertEqual('nothing to repeat', str(error))

    def test_good_regex(self):
        """ Test egrep with valid wildcard regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('.*rd'))

    def test_egrep_char_range(self):
        """ Test egrep with valid range regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('[a-z]ird'))

    def test_egrep_word_list(self):
        """ Test egrep with valid choice regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('(host|bird)'))

    def test_egrep_string_end(self):
        """ Test egrep with valid regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('tld$'))

    def test_egrep_string_start(self):
        """ Test egrep with valid regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.egrep('^10.*'))

    def test_add_with_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        test_file.unique = True
        self.assertTrue(test_file + 'uniq')
        self.assertFalse(test_file + 'uniq')
        self.assertFalse(test_file + 'uniq')
        self.assertTrue(test_file.contents == ['uniq'])

    def test_append_with_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        test_file.unique = True
        self.assertTrue(test_file.append('uniq'))
        self.assertFalse(test_file.append('uniq'))
        self.assertFalse(test_file.append('uniq'))
        self.assertTrue(test_file.contents == ['uniq'])

    def test_add_not_unique(self):
        """ Test content integrity not using `unique` """
        test_file = FileAsObj()
        test_file.unique = False
        self.assertTrue(test_file.add('no uniq'))
        self.assertTrue(test_file.add('no uniq'))
        self.assertTrue(test_file.add('no uniq'))
        self.assertTrue(test_file.contents == ['no uniq', 'no uniq', 'no uniq'])

    def test_subtract(self):
        """ Test __sub__ method """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file - '#comment')

    def test_subtract_fail(self):
        """ Test __sub__ method fails """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertFalse(test_file - 'this string does not exist in file!')

    def test_remove_multi(self):
        """ Test deleting multiple lines """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.rm(test_file.grep('#')))

    def test_replace_whole_line(self):
        """ Test substitute a line """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        old = '172.19.18.17    freebird.example.com'
        new = '172.19.18.17    freebird.example.com  # Added 1976.10.29 -jh'
        self.assertTrue(test_file.replace(old, new))

    def test_replace_regex(self):
        """ Test substitute lines using a valid regex """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        old = test_file.egrep('^[ ]+#.*')
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        self.assertFalse(test_file.egrep('^[ ]+#.*'))

    def test_replace_list(self):
        """ Test substitute lines using a list of strings """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        old = ['#', '# ', '#1']
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        for this in old:
            self.assertFalse(test_file.check(this))

    def test_count_comment_empty(self):
        """ Test __len__ method """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertEqual(len(test_file.grep('#')), 18)

    def test_string(self):
        """ Test __str__ method """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
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

    def test_add_list(self):
        """ Test adding a 3 element list with .add() """
        test_file = FileAsObj()
        test_list = ['simultaneous', 'money shot', 'remedy']
        test_file.add(test_list)
        self.assertTrue(test_file.changed)
        self.assertTrue(test_file.contents == test_list)
        self.assertTrue(str(test_file) == '\n'.join(test_list))

    def test_sorted_attr(self):
        """ Test self.sorted """
        test_file = FileAsObj()
        test_file.sorted = True
        test_file.add('3')
        test_file.add('2')
        test_file.add('1')
        self.assertTrue(test_file.contents == ['1', '2', '3'])


if __name__ == '__main__':
    unittest.main()
