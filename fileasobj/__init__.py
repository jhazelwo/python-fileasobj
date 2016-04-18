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

    def __init__(self, filename=None):
        """
        You may specify the file to read() during instantiation.
        """
        self.birthday = str(int(time.time()))
        #
        # Used during .write(), override only if absolutely necessary.
        self.linesep = '\n'
        #
        # Name of file this is running as
        arg0 = str(os.path.basename(sys.argv[0])).replace('.py', '')
        if len(arg0) < 3 or len(arg0) > 255:
            #
            # If arg zero is invalid, name me Python
            arg0 = 'Python'
        #
        # Create a local log object to track actions.
        self.log = self.Log(tag='{0}[{1}]'.format(arg0, os.getpid()))
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
        def __init__(self, tag):
            """ Create new log """
            self.trace = ''
            self.tag = tag

        def __call__(self, this):
            """ Add 'this' to my log """
            self.trace = '{OG}{Now} {Host} {Proc} {Event}\n'.format(
                OG=self.trace,
                Now=time.strftime('%c', time.localtime()),
                Host=node(),
                Proc=self.tag,
                Event=this,
            )

        def __str__(self):
            """ Return my log as multi-line string """
            return self.trace

    def read(self, given_file):
        """
        Read given_file to self.contents
        Will ignoring duplicate lines if self.unique is True
        """
        self.filename = str.strip(given_file)
        self.log('Read-only opening {0}'.format(self.filename))
        with open(self.filename, 'r') as handle:
            for line in handle:
                line = line.rstrip('\r\n')
                # Blank lines that were just \n become None so make sure this pass of line exists
                if line is not None:
                    if self.unique is not False and self.unique is not True:
                        raise AttributeError('Attribute self.unique is not True or False')
                    if self.unique is False:
                        self.contents.append(line)
                    elif self.unique is True and line not in self.contents:
                        self.contents.append(line)
        if self.sorted:
            self.sort()
        self.log('Read {0} lines'.format(len(self.contents)))
        return True

    def check(self, this):
        """
        check existing contents of file for a string

        This searches each line as a whole, if you want to see if a substring is in a line, use .grep() or .egrep()

        If found, return the needle; makes it easier for some code to delete more efficiently.
        """
        if this in self.contents:
            return this
        return False

    def add(self, this):
        """
        Append 'this' to contents
            where 'this' is an entire line or a list of lines.

        If self.unique is False it will add regardless of contents.

        Multi-line strings are converted to a list delimited by new lines.

        :param this: String or List of Strings. Arbitrary string(s) to append to file contents.
        :return: Boolean. Whether contents were changed during this method call.
        """
        self.log('Append "{0}" to {1}; unique={2}'.format(this, self.filename, self.unique))
        local_changes = False

        if this is False:
            return False
        if isinstance(this, str):
            this = this.split('\n')
        if not isinstance(this, list):
            raise ValueError('Argument given to .add() not a string or list, was {0}'.format(type(this)))

        for element in this:
            if self.unique is False:
                self.contents.append(element)
                self.changed = local_changes = True
            elif self.unique is True and element not in self.contents:
                self.contents.append(element)
                self.changed = local_changes = True
        if self.sorted and local_changes:
            self.sort()
        return local_changes

    def rm(self, this):
        """
        Remove all occurrences of 'this' from contents
            where 'this' is an entire line or a list of lines.

        Return true if the file was changed by rm(), False otherwise.

        Multi-line strings are converted to a list delimited by new lines.

        :param this: string, or list of strings - each string represents an entire line to be removed from file.
        :return: Boolean, whether contents were changed.
        """
        self.log('rm({0}, "{1}"):'.format(self.filename, this))
        if this is False:
            return False
        if isinstance(this, str):
            this = this.split('\n')
        if not isinstance(this, list):
            raise ValueError('Argument given to .rm() not a string or list, was {0}'.format(type(this)))
        #
        local_changes = False
        for element in this:
            if element in self.contents:
                while element in self.contents:
                    self.log('Removed "{0}" from position {1} of {2}'.format(element,
                                                                             self.contents.index(element),
                                                                             self.filename))
                    self.contents.remove(element)
                    self.changed = local_changes = True
            else:
                self.log('"{0}" not found in {1}'.format(element, self.filename))
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
        No regex support here.
        eq: `grep "needle" ./file`
        If 1 match, return line as string.
        If multiple matches return lines as list of strings.
        If no matches return False
        """
        r = list()
        for line in self.contents:
            if needle in line:
                r.append(line)
        if r:
            if len(r) == 1:
                return str(r[0])
            else:
                return r
        # all-else
        return False

    def egrep(self, pattern):
        """
        REGEX search for pattern in file
        eq: `egrep "^asdf.*[0-9]+$" ./file`
        If 1 match, return line as string.
        If multiple matches return lines as list of strings.
        If no matches return False
        """
        pattern = re.compile(pattern)
        r = list()
        for line in self.contents:
            if pattern.search(line):
                r.append(line)
        if r:
            if len(r) == 1:
                return str(r[0])
            else:
                return r
        # all-else
        return False

    def replace(self, old, new):
        """
        Replace all lines of file that match 'old' with 'new'

        Will replace duplicates if found.

        :param old: False, list of strings, or string.
        :param new: string
        """
        self.log('Replace "{0}" with "{1}" in {2}'.format(old, new, self.filename))
        if old is False:
            return False
        if isinstance(old, str):
            old = old.split('\n')
        if not isinstance(old, list):
            raise ValueError('Argument "old" not a string, list or False, was {0}'.format(type(old)))
        for this in old:
            if not isinstance(this, str):
                raise ValueError('{0} is not a string'.format(this))
            if this in self.contents:
                while this in self.contents:
                    index = self.contents.index(this)
                    self.changed = True
                    self.contents.remove(this)
                    self.contents.insert(index, new)
                    self.log('Replaced "{0}" with "{1}" at line {2} of {3}'.format(this,
                                                                                   new,
                                                                                   index,
                                                                                   self.filename))
            else:
                self.log('"{0}" not in {1}'.format(this, self.filename))
        return self.changed

    def save(self):
        """
        Answering a use case where calling this method with .save() instead of .write() is ideal.
        ex: myfile.save()
        """
        return self.write()

    def append(self, this):
        """
        Shorcut method
        ex: myfile.append('foo')
        """
        return self.add(this)

    def sort(self, key=None, reverse=False):
        """
        Sort contents using sort() method available to list()
        :return: None (because list().sort() doesn't return anything)
        """
        self.contents.sort(key=key, reverse=reverse)
        self.log('Contents sorted')
        return None

    def __len__(self):
        """
        Return line count of file in memory.
        ex: len(myfile)
        """
        return len(self.contents)

    def __str__(self):
        """
        Return file in memory contents as a multi-line string.
        ex: print(myfile)
        """
        return '\n'.join(self.contents)

    def __sub__(self, this):
        """
        Shortcut method
        ex: myfile - 'string to remove'
        """
        return self.rm(this)

    def __add__(self, this):
        """
        Shortcut method
        ex: myfile + 'string to append to end of myfile.contents'
        """
        return self.add(this)

    def __contains__(self, this):
        """
        Shortcut method
        ex: if 'this' in myfile: do(stuff)
        """
        return self.check(this)

    def __iter__(self):
        return self.contents.__iter__()
