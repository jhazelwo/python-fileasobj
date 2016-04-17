File as (Python) Object
===============
Manage a local file as an object. Store contents in a unique list and ignore commented lines.
Written to handle files that contain only text data, good for when you cannot or will not use a proper SQL database.

* Not useful for config files.
* Written by a SysAdmin who needed to treat files like databases.

### quick and dirty examples
`from fileasobj import FileAsObj`  

* Read /data/input.txt  

`my_file = FileAsObj(os.path.join(os.sep,'data','input.txt'))`  

* Read /etc/hosts verbatim (retain comments)  

`my_file = FileAsObj(os.path.join(os.sep,'etc','hosts'), verbose=True)`  

* Find (and show) the lines containing localhost in /etc/hosts  
```
    my_file = FileAsObj(os.path.join(os.sep,'etc','hosts'), verbose=True)  
    print(my_file.grep('localhost'))
```  

* Check for string in file  
```
    my_file = FileAsObj(os.path.join(os.sep,'etc','hosts'), verbose=True)  
    if 'localhost' in my_file: do(stuff)  
```

### Methods:
* .grep    find first occurrence of substring in file
* .egrep   regex-find first occurrence of substring in file (Remember to use '.*', not just '*')
* .add     Add given line to end of file
* .rm      Remove a line from file, give entire matching line.
* .check   Return line if line is in file, else return False
* .read    Read file into self.contents as list
* .write   Save list to file overriding file on disk
* .replace Replace a whole line (old, new)

### Attributes you usually care about:
* self.log - A string log of all methods run on object including any non-fatal errors
* verbose - BOOLEAN, if true file is .read() verbatim, comments and short lines are NOT ignored and duplicate lines are 
preserved. Please remember that .rm() and .replace() will work on duplicate lines.

### An ever-so-slightly-non-apocryphal non-minor version history:
 * 2016.04.17 - Conversion and deploy to pypi.
 * 2015.01.28 - V5, added shortcut methods, removed exception catching. Added local Log() class.
 * 2015.01.27 - .replace() now accepts list for param 'old'.
 * 2014.12.02 - V4, search methods can now return lists and .rm works on lists
 * 2014.09.09 - V3, added .replace(), removed .dump() and .inventory()
 * 2014.08.14 - Finally added __str__
 * 2014.08.11 - Tab fixes and print changes to comply with py3.
 * 2014.06.20 - V2, added [e]grep, dump and verbose; some code correction
 * 2012.08.15 - Full conversion to portability, added .read()
 * 2012.07.20 - Initial release

### Testing:
* I write in Python 3.4x and occasionally do testing in 2.6 and 2.7. This module /should/ work with anything between 2.6
 and 3.4+ but no promises.
* `./tests/test_fileasobj.py` is a standard unit test.


### TODO:
 * ...
