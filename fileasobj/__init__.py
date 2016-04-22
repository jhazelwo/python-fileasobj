""" -*- coding: utf-8 -*-
https://github.com/jhazelwo/python-fileasobj
(c) John Hazelwood, 2011-2016
"""
import os
from platform import node
import time
import re
import sys
sys.dont_write_bytecode = True

__version__ = '2.0.0'


class FileAsObj(object):
    """
    Manage a file as an object-
            -For when you just can't be bothered to use a real database.

    Each line of a file is added to the list 'self.contents'.
    By default lines are stored in the order they appear in the file.
    """

    def __init__(self, filename=None, logging=True):
        """
        You may specify the file to read() during instantiation.
        """
        self.birthday = str(int(time.time()))
        #
        # Used during .write(), override only if absolutely necessary.
        self.linesep = '\n'
        #
        # Create a local log object to track actions.
        self.log = self.Log(logging=logging)
        self.log('init(filename={0}):'.format(filename))
        #
        # The list where contents of the file are stored
        self.contents = list()
        #
        # Accept filename during instantiation, default is None.
        self.filename = filename
        #
        # Declare current state is original data from self.filename.
        # This is set to False during .read() and .write()/.save()
        # Any method that alters self.contents changes this to True.
        self.changed = False
        #
        # Automatically sort file on read()
        self.sorted = False
        #
        # Ensure file contents are always unique.
        self.unique = False
        #
        # If you gave me a file to read when instantiated, then do so.
        if self.filename is not None:
            self.read(self.filename)

    class Log(object):
        """
        Track and report steps taken in this app.
        'tag' is "name[pid]", similar to the -t argument used in `/bin/logger`
        """
        def __init__(self, logging=True):
            """ Create new log. """
            arg0 = str(os.path.basename(sys.argv[0])).replace('.py', '')
            if len(arg0) < 3 or len(arg0) > 255:
                arg0 = 'Python'  # If arg zero is invalid, name me Python
            self.trace = ''
            self.tag = '{0}[{1}]'.format(arg0, os.getpid())
            self.logging = logging

        def __call__(self, this):
            """ Add 'this' to my log. """
            if self.logging is True:
                self.trace += '{Now} {Host} {Proc} {Event}\n'.format(
                    Now=time.strftime('%c', time.localtime()),
                    Host=node(),
                    Proc=self.tag,
                    Event=this,
                )

        def __str__(self):
            """ Return my log as multi-line string. """
            return self.trace

    def read(self, given_file):
        """
        Read given_file to self.contents
        Will ignoring duplicate lines if self.unique is True
        Will sort self.contents after reading file if self.sorted is True
        """
        if self.unique is not False and self.unique is not True:
            raise AttributeError('Attribute self.unique is not True or False.')
        self.filename = str.strip(given_file)
        self.log('Read-only opening {0}'.format(self.filename))
        with open(self.filename, 'r') as handle:
            for line in handle:
                line = line.rstrip('\r\n')
                if line is None:
                    line = ''  # Blank lines that were just \n become None so convert them to empty string.
                if self.unique is False or line not in self.contents:
                    self.contents.append(line)
        if self.sorted:
            self.sort()
        self.log('Read {0} lines.'.format(len(self.contents)))
        return True

    def check(self, line):
        """
        Find first occurrence of 'line' in file.

        This searches each line as a whole, if you want to see if a substring is in a line, use .grep() or .egrep()

        If found, return the line; this makes it easier to chain methods.

        :param line: String; whole line to find.
        :return: String or False.
        """
        if line in self.contents:
            return line
        return False

    def add(self, line):
        """
        Append 'line' to contents
            where 'line' is an entire line or a list of lines.

        If self.unique is False it will add regardless of contents.

        Multi-line strings are converted to a list delimited by new lines.

        :param line: String or List of Strings; arbitrary string(s) to append to file contents.
        :return: Boolean; whether contents were changed during this method call.
        """
        if self.unique is not False and self.unique is not True:
            raise AttributeError('Attribute self.unique is not True or False.')
        self.log('add("{0}"); unique={1}'.format(line, self.unique))
        if line is False:
            return False
        if isinstance(line, str):
            line = line.split('\n')
        if not isinstance(line, list):
            raise ValueError('Argument given to .add() not a string or list, was {0}'.format(type(line)))
        local_changes = False
        for this in line:
            if self.unique is False or this not in self.contents:
                self.contents.append(this)
                self.changed = local_changes = True
        if self.sorted and local_changes:
            self.sort()
        return local_changes

    def rm(self, line):
        """
        Remove all occurrences of 'line' from contents
            where 'line' is an entire line or a list of lines.

        Return true if the file was changed by rm(), False otherwise.

        Multi-line strings are converted to a list delimited by new lines.

        :param line: String, or List of Strings; each string represents an entire line to be removed from file.
        :return: Boolean, whether contents were changed.
        """
        self.log('rm({0})'.format(line))
        if line is False:
            return False
        if isinstance(line, str):
            line = line.split('\n')
        if not isinstance(line, list):
            raise ValueError('Argument given to .rm() not a string or list, was {0}'.format(type(line)))
        local_changes = False
        for this in line:
            if this in self.contents:
                while this in self.contents:
                    self.log('Removed "{0}" from position {1}'.format(this, self.contents.index(this)))
                    self.contents.remove(this)
                    self.changed = local_changes = True
            else:
                self.log('"{0}" not found in {1}'.format(this, self.filename))
        if self.sorted and local_changes:
            self.sort()
        return local_changes

    def write(self):
        """
        write self.contents to self.filename
        self.filename was defined during .read()

        There is no self.changed check because we need to let the caller decide whether or not to write. This is
            useful if you want to force an overwrite of a file that might have been changed on disk even if
            self.contents did not change.
        """
        self.log('Writing {0}'.format(self.filename))
        with open(self.filename, 'w') as handle:
            for this_line in self.contents:
                handle.write(this_line+self.linesep)
        self.changed = False
        return True

    def grep(self, needle):
        """
        Search all lines in file for substring 'needle'.
            equiv to: `grep "needle" ./file`

        Return matching lines as a List of Strings.
        If no matches returns False

        :param needle: String; word or phrase to search for.
        :return: List of Strings, or False.
        """
        result = []
        for line in self.contents:
            if needle in line:
                result.append(line)
        if result:
            return result
        return False

    def egrep(self, pattern):
        """
        REGEX search for pattern in file
            equiv to: `egrep "^asdf.*[0-9]+$" ./file`

        Return matching lines as a List of Strings.
        If no matches returns False

        :param pattern: String; regex pattern to search for.
        :return: List of Strings, or False.
        """
        pattern = re.compile(pattern)
        result = []
        for line in self.contents:
            if pattern.search(line):
                result.append(line)
        if result:
            return result
        return False

    def replace(self, old, new):
        """
        Replace all lines of file that match 'old' with 'new'

        Will replace duplicates if found.

        :param old: String, List of Strings, a multi-line String, or False; what to replace.
        :param new: String; what to use as replacement.

        :return: Boolean; whether contents changed during method call.
        """
        self.log('replace("{0}", "{1}")'.format(old, new))
        if old is False:
            return False
        if isinstance(old, str):
            old = old.split('\n')
        if not isinstance(old, list):
            raise ValueError('Argument "old" not a string, list or False, was {0}'.format(type(old)))
        local_changes = False
        for this in old:
            if this in self.contents:
                while this in self.contents:
                    index = self.contents.index(this)
                    self.changed = local_changes = True
                    self.contents.remove(this)
                    self.contents.insert(index, new)
                    self.log('Replaced "{0}" with "{1}" at line {2}'.format(this, new, index))
            else:
                self.log('"{0}" not in {1}'.format(this, self.filename))
        return local_changes

    def save(self):
        """ Alias method, some use-cases prefer .save() over .write(). """
        return self.write()

    def append(self, this):
        """ Alias method, some use-cases prefer .append() over .add(). """
        return self.add(this)

    def sort(self, key=None, reverse=False):
        """
        Sort contents using sort() method available to list()
        :return: None (because list().sort() doesn't return anything)
        """
        self.contents.sort(key=key, reverse=reverse)
        self.log('Contents sorted.')
        return None

    def __len__(self):
        """ Return line count of file in memory. """
        return len(self.contents)

    def __str__(self):
        """ Return file in memory contents as a multi-line string. """
        return '\n'.join(self.contents)

    def __sub__(self, this):
        """ Shortcut method, allow line removal by subtraction. """
        return self.rm(this)

    def __add__(self, this):
        """ Shortcut method, allow line appending by addition. """
        return self.add(this)

    def __contains__(self, this):
        """ Shortcut method to check for a line in the file. """
        return self.check(this)

    def __iter__(self):
        """ Shortcut method to iterate over file contents. """
        return self.contents.__iter__()
