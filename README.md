File as (Python) Object
===============

Manage a local file as an object. Contents stored in a [list](https://docs.python.org/3/library/stdtypes.html#list).

Written to handle files that contain only text data, good for when you cannot (or will not) use a database.

Typically this module is not appropriate for config files. (Your mileage may vary)


### Installation:

`pip install fileasobj`


### Usage:

* See docs/examples.py for lots of useful examples.

```
# This example adds a line to /etc/hosts

from fileasobj import FileAsObj

my_file = FileAsObj('/etc/hosts')
my_file.add('192.168.0.1  example.org')
my_file.save()

```  

* Depending on your learning style reading tests/tests_fileasobj.py might also be helpful in enabling you to get the most out of this module.

### Methods:

* .grep('string')
    * Find all occurrences of string in file.
    * 1 match is returned as a string, multiple matches returned as a list of strings. Returns False if no matches.
* .egrep('^a?regex.*pattern$')
    * Regex-find all occurrences of substring in file.
    * Uses Python3 standard regex engine https://docs.python.org/3/library/re.html
    * _Remember to use ' .* ', not just ' * '_.
* .add('entire line as string')
    * Add given line to end of file.
    * Also accepts a list of lines.
* .rm('entire line as string')
    * Remove a line from file, give entire matching line.
    * Also accepts a list of lines.
* .check('entire line as string')
    * Return line if line is in file, else return False
* .read('/path/to/file')
    * Read file into self.contents as list
* .save()
    * Writes contents to file overriding file on disk.
    * Alias of .write()
* .replace('existing line to replace', 'line to use as replacement')
    * Replace a whole line.
    * Will accept a list of lines for first parameter.
* .sort()
    * Sort contents in-place using list()'s sort() method.
* .\_\_str\_\_()
    * If you use a string method on your object (_like str() or print()_) the contents will be returned as a multi-line string.
    * ex: `print(my_file)`

Shortcut methods also exist, check examples.py for usage.

### Attributes:

* `filename`
    * String; path to file.
* `sorted`
    * Boolean; whether to naturally sort contents during update methods. Uses list()'s built-in sort() method.
* `unique`
    * Boolean; whether to permit duplicate lines during .read() and update methods.
* `changed`
    * Boolean; whether the current state if different from what was .read() from disk.
    * This is automatically updated during .read() and .write()/.save().
* `contents`
    * List; contents of file.
* `log`
    * A string log of all methods run on object including any non-fatal errors
* `linesep`
    * String; override the default line separator during .write().

### An ever-so-slightly-non-apocryphal non-minor version history:
 
* 2016.04.17 - Conversion and deploy to pypi. FileAsList removed.
* 2015.01.28 - Added shortcut methods, removed exception catching. Added local Log() class.
* 2015.01.27 - .replace() now accepts list for param 'old'.
* 2014.12.02 - Search methods can now return lists and .rm works on lists
* 2014.09.09 - Added .replace(), removed .dump() and .inventory()
* 2014.08.14 - Finally added \_\_str\_\_
* 2014.08.11 - Tab fixes and print changes to comply with py3.
* 2014.06.20 - Added [e]grep, dump and verbose; some code correction
* 2012.08.15 - Full conversion to portability, added .read()
* 2012.07.20 - Initial public release.


### Testing:

I write in Python 3.4 and occasionally do testing and 2.7. This module _should_ work with anything between 2.7
 and 3.4, please let me know if you find a bug.

`./tests/test_fileasobj.py` is a standard unit test.


### Troubleshooting:

If FileAsObj did something you didn't expect then add a `print(my_file.log)` to your code, that will show all of the steps FileAsObj did during its life. 

File an [issue](https://github.com/jhazelwo/python-fileasobj/issues) on this repo if you need help.


### Development & TODO:

* Add as_dict() method: return self.contents as a dictionary, where key is line number and value is line content. Note, there is no use-case for this currently.
