""" -*- coding: utf-8 -*-

Manage a local file as an object. Store contents in a unique list and ignore commented lines.

Written to handle files that contain only text data, good for when you cannot or will not use a proper SQL database.
Not useful for config files.

Written by a SysAdmin who needed to treat files like databases.

John Hazelwood, 2016
https://github.com/jhazelwo/python-fileasobj

"""
import os
from platform import node
import time
import re
import sys
sys.dont_write_bytecode = True


class FileAsObj(list):
    """
    Manage a file as an object-
            -For when you just can't be bothered to use a real database.

    Each line of a file is added to the list 'self.contents'.
    By default lines that start with a # are ignored.
    By default data in self.contents is unique.
    Lines are stored in the order they appear in the file.
    """

    def __init__(self, filename=None, verbose=False):
        """
        You may specify the file to read() during instantiation.

        verbose - BE CAREFUL! If you enable verbose all of the lines in your file will be added to self.contents.
            This includes comments and duplicate lines. If you rely on this classes' .grep() or .egrep() methods
            be sure you understand that comments can be returned as a valid result!

        """
        self.birthday = (
            float(time.time()),
            str(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))
            )
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
        self.log('init(filename={0}, verbose={1}):'.format(filename, verbose))
        #
        # The list where contents of the file are stored
        self.contents = list()
        #
        # Accept filename during instantiation, default is None.
        self.filename = filename
        #
        # Declare current state is original data from self.filename.
        self.virgin = True
        #
        # If you gave me a file to read when instantiated, then do so.
        if self.filename is not None:
            self.read(self.filename, verbose)

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

    def read(self, given_file, verbose=False):
        """
        Read given_file to self.contents, ignoring comments and duplicate lines.
        WILL add a line if it starts with a space or tab but has a # later in
        the line.
        """
        self.filename = str.strip(given_file)
        self.log('Read-only opening {0}'.format(self.filename))
        with open(self.filename, 'r') as handle:
            for line in handle:
                line = line.rstrip('\r\n')
                #
                # blank lines that were just \n become None,
                # so make sure this pass of line exists
                if line:
                    if verbose:
                        #
                        # Some crazy person enabled verbose, just
                        # add whatever is in the file to
                        # self.contents.
                        # May whatever god you believe in
                        #   have mercy on your code.
                        self.contents.append(line)
                    elif line[0] is not '#':
                        # Line is not a comment
                        #
                        #
                        # unique the contents of given_file when reading
                        # Ignore lines that have fewer than 2 characters
                        if len(line) > 1 and line not in self.contents:
                            self.contents.append(line)
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

    def add(self, line, unique=True):
        """
        add 'line' to end of contents.
        By default will not create a duplicate line.
        If unique is False will add regardless of contents.
        """
        self.log('Append "{0}" to {1}; unique={2}'.format(line, self.filename, unique))
        if unique is False:
            self.contents.append(line)
            self.virgin = False
            return True
        if line not in self.contents:
            self.contents.append(line)
            self.virgin = False
            return True
        return False

    def rm(self, this):
        """
        Remove all occurrences of 'this' from contents
            where 'this' is an entire line or a list of lines.

        Return true if the file was changed by rm(), False otherwise.

        :param this: string, or list of strings - each string represents an entire line to be removed from file.
        """
        self.log('rm({0}, "{1}"):'.format(self.filename, this))
        if this is False:
            return False
        if isinstance(this, str):
            this = this.split('\n')
        if not isinstance(this, list):
            raise ValueError('Argument given to .rm() not a string or list, was {0}'.format(type(this)))
        #
        for element in this:
            if element in self.contents:
                while element in self.contents:
                    self.log('Removed "{0}" from position {1} of {2}'.format(element,
                                                                             self.contents.index(element),
                                                                             self.filename))
                    self.contents.remove(element)
                    self.virgin = False
            else:
                self.log('"{0}" not found in {1}'.format(element, self.filename))
        #
        if self.virgin is True:
            return False
        return True

    def write(self):
        """
        write self.contents to self.filename
        self.filename was defined during .read()

        There is no self.virgin check because we need to let the caller decide whether or not to write. This is
            useful if you want to force an overwrite of a file that might have been changed on disk even if
            self.contents did not change.

        You can do something like:
        if not stats.virgin:
            #
            #something changed, re-write the file.
            stats.write()
        """
        self.log('Writing {0}'.format(self.filename))
        with open(self.filename, 'w') as handle:
            for this_line in self.contents:
                handle.write(this_line+'\n')
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
        retval = list()
        for line in self.contents:
            if needle in line:
                retval.append(line)
        if retval:
            if len(retval) == 1:
                return str(retval[0])
            else:
                return retval
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
        retval = list()
        for line in self.contents:
            if pattern.search(line):
                retval.append(line)
        if retval:
            if len(retval) == 1:
                return str(retval[0])
            else:
                return retval
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
                    self.virgin = False
                    self.contents.remove(this)
                    self.contents.insert(index, new)
                    self.log('Replaced "{0}" with "{1}" at line {2} of {3}'.format(this,
                                                                                   new,
                                                                                   index,
                                                                                   self.filename))
            else:
                self.log('"{0}" not in {1}'.format(this, self.filename))
        if self.virgin is True:
            return False
        return True

    def save(self):
        """
        Answering a use case where calling this method with .save() instead of .write() is ideal.
        ex: myfile.save()
        """
        return self.write()

    def append(self, this, unique=True):
        """
        Shorcut method
        ex: myfile.append('foo')
        """
        return self.add(this, unique)

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
