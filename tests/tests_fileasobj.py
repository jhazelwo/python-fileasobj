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

TESTFILE = '/tmp/test_fileasobj.txt'  # Change me on Windows

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

# Four empty lines
BLANKFILE = """


"""


class TestInit(unittest.TestCase):
    # def __init__(self, filename=None, logging=True):
    def test_file_not_found(self):
        """
        Fail if trying to instance class for file that does not exist.
        This tests the shortcut method in __init__
        """
        with self.assertRaises(IOError):
            FileAsObj('/this/file/does/not/exist/')

    def test_simple(self):
        """ Instance an empty test file and check instance type matches. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        self.assertIsInstance(test_file, FileAsObj)

    def test_birthday(self):
        """ Ensure object has non-empty attribute `birthday` """
        test_file = FileAsObj()
        self.assertTrue(test_file.birthday)
        self.assertIsInstance(test_file.birthday, str)

    def test_default_params(self):
        test_file = FileAsObj()
        self.assertFalse(test_file.unique)
        self.assertFalse(test_file.sorted)
        self.assertFalse(test_file.changed)
        self.assertIsNone(test_file.filename)
        self.assertTrue(test_file.contents == [])
        self.assertTrue(test_file.linesep == '\n')


class TestLog(unittest.TestCase):
    # class Log(object):
    #     def __init__(self, logging=True):
    #     def __call__(self, this):
    #     def __str__(self):
    def test_logging_disable(self):
        """ Test disabled local log. """
        test_file = FileAsObj(logging=False)
        test_file.log('logging disabled this will not be saved')
        self.assertTrue(str(test_file.log) == '')
        self.assertTrue(test_file.log.trace == '')

    def test_logging_enabled(self):
        """ Test local log enabled by default. """
        test_file = FileAsObj()
        self.assertIsNotNone(str(test_file.log))
        test_file.log('FINDME')
        self.assertTrue('FINDME' in str(test_file.log))
        self.assertTrue('FINDME' in test_file.log.trace)

    def test_string_log_str(self):
        """ Test __str__ method of log subclass. """
        test_file = FileAsObj()
        self.assertTrue(str(test_file.log))

    def test_string_log_call(self):
        """ Test __call__ method of log subclass. """
        test_file = FileAsObj()
        self.assertIsNone(test_file.log('test'))

    def test_string_log_has_tag(self):
        """ Test tag attribute of log subclass. """
        test_file = FileAsObj()
        self.assertTrue(str(test_file.log.tag))


class TestRead(unittest.TestCase):
    # def read(self, given_file):
    def test_blank_file_with_unique(self):
        """ Testing unique on empty lines during .read() """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        test_file.contents = BLANKFILE.split('\n')
        self.assertTrue(test_file.save())
        test_file = FileAsObj()
        test_file.unique = True
        test_file.read(TESTFILE)
        self.assertTrue(test_file.contents == [''])

    def test_blank_file_without_unique(self):
        """ Testing not-unique on empty lines during .read() """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        test_file.contents = BLANKFILE.split('\n')
        self.assertTrue(test_file.save())
        test_file = FileAsObj()
        test_file.unique = False
        test_file.read(TESTFILE)
        self.assertTrue(test_file.contents == ['', '', '', ''])

    def test_unique_failure_during_read(self):
        """ Test wrong attribute type of self.unique during read() """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        test_file.contents = BLANKFILE.split('\n')
        self.assertTrue(test_file.save())
        test_file = FileAsObj()
        test_file.unique = 'this is invalid attr type'
        with self.assertRaises(AttributeError):
            test_file.read(TESTFILE)


class TestCheck(unittest.TestCase):
    # def check(self, line):
    def test_check(self):
        """ Test check method. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.check('# This is a test hosts file'))

    def test_check_not(self):
        """ Test check method. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.check('95bf5dd7096c3552063e4187b4194b1f') == False)


class TestAdd(unittest.TestCase):
    # def add(self, line):
    def test_add_failure_param(self):
        """ Test wrong param type. """
        test_file = FileAsObj()
        with self.assertRaises(ValueError):
            test_file.add(1)
        with self.assertRaises(ValueError):
            test_file.add(True)

    def test_unique_failure(self):
        """ Test unique wrong attribute type. """
        test_file = FileAsObj()
        test_file.unique = 'this is invalid attr type'
        with self.assertRaises(AttributeError):
            test_file.add('.')

    def test_add_string_unique(self):
        """ Test content integrity with unique. """
        test_file = FileAsObj()
        test_file.unique = True
        subject = 'uniq'
        self.assertTrue(test_file.add(subject))
        self.assertFalse(test_file.add(subject))
        self.assertTrue(test_file.contents == [subject])

    def test_add_string_no_unique(self):
        """ Test content integrity without unique. """
        test_file = FileAsObj()
        subject = 'uniq'
        self.assertTrue(test_file.add(subject))
        self.assertTrue(test_file.add(subject))
        self.assertTrue(test_file.contents == [subject, subject])

    def test_add_list_no_unique(self):
        """ Test adding a 3 element list. """
        test_file = FileAsObj()
        subject = ['simultaneous', 'money shot', 'remedy']
        self.assertTrue(test_file.add(subject))
        self.assertTrue(test_file.changed)
        self.assertTrue(test_file.add(subject))
        self.assertTrue(test_file.contents == subject + subject)
        self.assertTrue(str(test_file) == '\n'.join(subject + subject))

    def test_add_list_unique(self):
        """ Test adding a 3 element list. """
        test_file = FileAsObj()
        test_file.unique = True
        subject = ['simultaneous', 'money shot', 'remedy']
        self.assertFalse(test_file.changed)
        self.assertTrue(test_file.add(subject))
        self.assertTrue(test_file.changed)
        self.assertFalse(test_file.add(subject))
        self.assertTrue(test_file.contents == subject)
        self.assertTrue(str(test_file) == '\n'.join(subject))


class TestRm(unittest.TestCase):
    # def rm(self, line):
    def test_rm_failure(self):
        """ Test wrong param type in rm() """
        test_file = FileAsObj()
        with self.assertRaises(ValueError):
            test_file.rm(1)
        with self.assertRaises(ValueError):
            test_file.rm(True)

    def test_remove_multi(self):
        """ Test deleting multiple lines. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertTrue(test_file.rm(test_file.grep('#')))


class TestWrite(unittest.TestCase):
    # def write(self):
    def test_write_no_changes(self):
        """ Instance an empty test file and save to disk. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        self.assertTrue(test_file.write())

    def test_write_with_changes(self):
        """ Instance an empty test file, overwrite its contents and save to disk. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertEqual(TESTCONTENTS, str(test_file))
        self.assertTrue(test_file.write())


class TestSave(unittest.TestCase):
    # def save(self):
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


class TestGrep(unittest.TestCase):
    # def grep(self, needle):
    def test_grep_no_matches(self):
        """ Test grep substring not present in file. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        result = test_file.egrep('substring_not_found')
        self.assertFalse(result)

    def test_grep_match(self):
        """ Test grep substring present in file, 1 match. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        subject = 'localhost'
        result = test_file.egrep(subject)
        self.assertTrue(result)
        self.assertTrue(result == ['127.0.0.1 localhost.localdomain localhost'])

    def test_grep_matches(self):
        """ Test grep substring present in file, multiple match. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        subject = 'www01'
        result = test_file.egrep(subject)
        self.assertTrue(result)
        self.assertTrue(result == ['10.2.5.2    www01   www01.example.tld', '#172.8.8.8    www01   www01.example.tld'])


class TestEgrep(unittest.TestCase):
    # def egrep(self, pattern):
    def test_egrep_char_list(self):
        """ Test egrep with valid character selector regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        subject = 'h[o0]stname'
        result = test_file.egrep(subject)
        self.assertTrue(result)
        self.assertIsInstance(result, list)

    def test_egrep_word(self):
        """ Test egrep with a word. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        result = test_file.egrep('bird')
        self.assertTrue(result)
        self.assertIsInstance(result, list)

    def test_bad_regex(self):
        """ Test egrep with invalid regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        try:
            test_file.egrep('*rd')
        except Exception as error:
            self.assertEqual('nothing to repeat', str(error))

    def test_good_regex(self):
        """ Test egrep with valid wildcard regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        result = test_file.egrep('.*rd')
        self.assertTrue(result)
        self.assertIsInstance(result, list)

    def test_egrep_char_range(self):
        """ Test egrep with valid range regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        self.assertTrue(test_file.egrep('[a-z]ird'))

    def test_egrep_word_list(self):
        """ Test egrep with valid choice regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        result = test_file.egrep('(host|bird)')
        self.assertTrue(result)
        self.assertIsInstance(result, list)

    def test_egrep_string_end(self):
        """ Test egrep with valid regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        result = test_file.egrep('tld$')
        self.assertTrue(len(result) == 4)
        self.assertIsInstance(result, list)

    def test_egrep_string_start(self):
        """ Test egrep with valid regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        result = test_file.egrep('^10.*')
        self.assertTrue(len(result) == 5)
        self.assertIsInstance(result, list)

    def test_egrep_no_matches(self):
        """ Test egrep with valid regex but pattern not in file. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        result = test_file.egrep('^this is not present in file.*')
        self.assertTrue(result is False)
        self.assertIsInstance(result, bool)


class TestReplace(unittest.TestCase):
    # def replace(self, old, new):
    def test_replace_regex(self):
        """ Test substitute lines using a valid regex. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        old = test_file.egrep('^[ ]+#.*')
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        self.assertFalse(test_file.egrep('^[ ]+#.*'))

    def test_replace_list(self):
        """ Test substitute lines using a list of strings. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertFalse(test_file.changed)
        old = ['#', '# ', '#1']
        new = '###'
        self.assertTrue(test_file.replace(old, new))
        self.assertTrue(test_file.changed)
        for this in old:
            self.assertFalse(test_file.check(this))
        self.assertEqual(test_file.check(new), new)

    def test_replace_failure(self):
        """ Test wrong param type in replace() """
        test_file = FileAsObj()
        with self.assertRaises(ValueError):
            test_file.replace(1, '')
        with self.assertRaises(ValueError):
            test_file.replace(True, '')

    def test_replace_whole_line(self):
        """ Test substitute a line. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        old = '172.19.18.17    freebird.example.com'
        new = '172.19.18.17    freebird.example.com  # Added 1976.10.29 -jh'
        self.assertTrue(test_file.replace(old, new))


class TestAppend(unittest.TestCase):
    # def append(self, this):
    def test_append_failure_param(self):
        """ Test wrong param type in append() """
        test_file = FileAsObj()
        with self.assertRaises(ValueError):
            test_file.append(1)
        with self.assertRaises(ValueError):
            test_file.append(True)

    def test_unique_failure(self):
        """ Test wrong attribute type of self.unique during append() """
        test_file = FileAsObj()
        test_file.unique = 'this is invalid attr type'
        with self.assertRaises(AttributeError):
            test_file.append('.')

    def test_append_string_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        test_file.unique = True
        subject = 'uniq'
        self.assertTrue(test_file.append(subject))
        self.assertFalse(test_file.append(subject))
        self.assertTrue(test_file.contents == [subject])

    def test_append_string_no_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        subject = 'uniq'
        self.assertTrue(test_file.append(subject))
        self.assertTrue(test_file.append(subject))
        self.assertTrue(test_file.contents == [subject, subject])

    def test_append_list_no_unique(self):
        """ Test adding a 3 element list with .add() """
        test_file = FileAsObj()
        subject = ['simultaneous', 'money shot', 'remedy']
        self.assertTrue(test_file.append(subject))
        self.assertTrue(test_file.changed)
        self.assertTrue(test_file.append(subject))
        self.assertTrue(test_file.contents == subject + subject)
        self.assertTrue(str(test_file) == '\n'.join(subject + subject))

    def test_append_list_unique(self):
        """ Test adding a 3 element list with .add() """
        test_file = FileAsObj()
        test_file.unique = True
        subject = ['simultaneous', 'money shot', 'remedy']
        self.assertFalse(test_file.changed)
        self.assertTrue(test_file.append(subject))
        self.assertTrue(test_file.changed)
        self.assertFalse(test_file.append(subject))
        self.assertTrue(test_file.contents == subject)
        self.assertTrue(str(test_file) == '\n'.join(subject))


class TestSort(unittest.TestCase):
    # def sort(self, key=None, reverse=False):
    def test_sorted_attr(self):
        """ Test self.sorted attribute. """
        test_file = FileAsObj()
        test_file.sorted = True
        test_file.add('3')
        test_file.add('2')
        test_file.add('1')
        self.assertTrue(test_file.changed)
        self.assertTrue(test_file.contents == ['1', '2', '3'])

    def test_sort_method(self):
        """ Test self.sort() method. """
        test_file = FileAsObj()
        test_file.sorted = False
        test_file.add('3')
        test_file.add('2')
        test_file.add('1')
        self.assertTrue(test_file.changed)
        self.assertIsNone(test_file.sort())
        self.assertTrue(test_file.contents == ['1', '2', '3'])


class TestLen(unittest.TestCase):
    # def __len__(self):
    def test_count_comment_empty(self):
        """ Test __len__ method. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        subject = '#'
        result = test_file.grep(subject)
        self.assertTrue(result)
        self.assertEqual(len(result), 18)


class TestStr(unittest.TestCase):
    # def __str__(self):
    def test_string(self):
        """ Test __str__ method. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        self.assertTrue(str(test_file) == TESTCONTENTS)


class TestSubtraction(unittest.TestCase):
    # def __sub__(self, this):
    def test_subtract(self):
        """ Test __sub__ method. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertFalse(test_file.changed)
        self.assertTrue(test_file - '#comment')
        self.assertTrue(test_file.changed)

    def test_subtract_fail(self):
        """ Test __sub__ method fails. """
        test_file = FileAsObj()
        test_file.contents = TESTCONTENTS.split('\n')
        self.assertFalse(test_file.changed)
        self.assertFalse(test_file - 'this string does not exist in file!')
        self.assertFalse(test_file.changed)


class TestAddition(unittest.TestCase):
    # def __add__(self, this):
    def test_addition_with_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        test_file.unique = True
        subject = 'uniq'
        self.assertTrue(test_file + subject)
        self.assertFalse(test_file + subject)
        self.assertFalse(test_file + subject)
        self.assertTrue(test_file.contents == [subject])

    def test_addition_failure_param(self):
        """ Test wrong param type. """
        test_file = FileAsObj()
        with self.assertRaises(ValueError):
            test_file + 1
        with self.assertRaises(ValueError):
            test_file + True

    def test_addition_unique_failure(self):
        """ Test wrong attribute type of self.unique. """
        test_file = FileAsObj()
        test_file.unique = 'this is invalid attr type'
        with self.assertRaises(AttributeError):
            test_file + '.'

    def test_addition_string_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        test_file.unique = True
        subject = 'uniq'
        self.assertTrue(test_file + subject)
        self.assertFalse(test_file + subject)
        self.assertTrue(test_file.contents == [subject])

    def test_addition_string_no_unique(self):
        """ Test content integrity using `unique` """
        test_file = FileAsObj()
        subject = 'uniq'
        self.assertTrue(test_file + subject)
        self.assertTrue(test_file + subject)
        self.assertTrue(test_file.contents == [subject, subject])

    def test_addition_list_no_unique(self):
        """ Test adding a 3 element list. """
        test_file = FileAsObj()
        subject = ['simultaneous', 'money shot', 'remedy']
        self.assertTrue(test_file + subject)
        self.assertTrue(test_file.changed)
        self.assertTrue(test_file + subject)
        self.assertTrue(test_file.contents == subject + subject)
        self.assertTrue(str(test_file) == '\n'.join(subject + subject))

    def test_addition_list_unique(self):
        """ Test adding a 3 element list with unique. """
        test_file = FileAsObj()
        test_file.unique = True
        subject = ['simultaneous', 'money shot', 'remedy']
        self.assertFalse(test_file.changed)
        self.assertTrue(test_file + subject)
        self.assertTrue(test_file.changed)
        self.assertFalse(test_file + subject)
        self.assertTrue(test_file.contents == subject)
        self.assertTrue(str(test_file) == '\n'.join(subject))


class TestContains(unittest.TestCase):
    # def __contains__(self, this):
    def test_contains(self):
        """ Test __contains__ method. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        subject = 'Checking for __contains__ functionality.'
        self.assertTrue(subject in test_file)

    def test_not_contains(self):
        """ Test __contains__ method. """
        test_file = FileAsObj()
        test_file.add(TESTCONTENTS)
        subject = '95bf5dd7096c3552063e4187b4194b1f'
        self.assertTrue(subject not in test_file)


class TestIter(unittest.TestCase):
    # def __iter__(self):
    def test_iter(self):
        """ Test __iter__ method. """
        test_file = FileAsObj()
        test_file.filename = TESTFILE
        test_file.add(TESTCONTENTS)
        self.assertTrue(test_file.save())
        test_file = FileAsObj(TESTFILE)
        for this in test_file:
            self.assertIsNotNone(this)  # Can be True or False, but not None; empty str is False.
            self.assertIsInstance(this, str)


if __name__ == '__main__':
    unittest.main()
