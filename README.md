File as (Python) Object
===============

Manage a local file as an object. Store contents in a unique list and optionally ignore commented lines.

Written to handle files that contain only text data, good for when you cannot (or will not) use a database.

Typically this module is not appropriate for config files. (Your mileage may vary)


### Installation:

`pip install fileasobj`


### Usage:

* See docs/examples.py for lots of useful examples.

```
# This example adds a line to /etc/hosts

from fileasobj import FileAsObj

my_file = FileAsObj('/etc/hosts', verbose=True)
my_file.add('192.168.0.1  example.org')
my_file.save()

```  


### Methods:

* .grep    Find first occurrence of substring in file
* .egrep   Regex-find first occurrence of substring in file (Remember to use ' .* ', not just ' * ')
* .add     Add given line to end of file
* .rm      Remove a line from file, give entire matching line.
* .check   Return line if line is in file, else return False
* .read    Read file into self.contents as list
* .write   Save list to file overriding file on disk
* .replace Replace a whole line (old, new)

Shortcut methods also exist, check examples.py for usage.

### Attributes:

* log - A string log of all methods run on object including any non-fatal errors
* verbose - BOOLEAN, if true file is .read() verbatim, comments and short lines are NOT ignored and duplicate lines are 
preserved. Please remember that .rm() and .replace() will work on duplicate lines.
* changed - BOOLEAN, whether the current state if different from what was .read() from disk.
* linesep - STRING, override the default line separator during .write().

### An ever-so-slightly-non-apocryphal non-minor version history:
 
 * 2016.04.17 - Conversion and deploy to pypi. FileAsList removed.
 * 2015.01.28 - Added shortcut methods, removed exception catching. Added local Log() class.
 * 2015.01.27 - .replace() now accepts list for param 'old'.
 * 2014.12.02 - Search methods can now return lists and .rm works on lists
 * 2014.09.09 - Added .replace(), removed .dump() and .inventory()
 * 2014.08.14 - Finally added __ str__
 * 2014.08.11 - Tab fixes and print changes to comply with py3.
 * 2014.06.20 - Added [e]grep, dump and verbose; some code correction
 * 2012.08.15 - Full conversion to portability, added .read()
 * 2012.07.20 - Initial public release.


### Testing:

I write in Python 3.4x and occasionally do testing in 2.6 and 2.7. This module /should/ work with anything between 2.6
 and 3.4+ but no promises.

`./tests/test_fileasobj.py` is a standard unit test.


### Devel / TODO:

* Deploy 1.1.0 to pypi
* In an up-coming release (Version 2.x) the `verbose` parameter will be replaced by a `unique` attribute.
* Will add a `sorted` attribute keep file sort-ed.
* A .sort() shortcut method will be added to sort self.contents in place.
* self.birthday will be changed from a tuple to string containing epoch time in gmt.
