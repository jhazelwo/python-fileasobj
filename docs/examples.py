""" -*- coding: utf-8 -*-
docs/examples.py

Extensive examples for FileAsObj
"""
from fileasobj import FileAsObj


def example_read_exists():
    """
    Reading a file that already exists.
    This will raise an exception if the file does not exist.
    """
    my_file = FileAsObj('/tmp/example_file.txt')


def example_file_create():
    """
    Creating an object for a file that does NOT exist but we wish to create.
    If the file exists this will truncate it.
    """
    my_file = FileAsObj()
    my_file.filename = '/tmp/a_file.txt'
    my_file.save()


def example_read_catch_errors():
    """ Reading a file and catch errors. """
    try:
        my_file = FileAsObj()
        my_file.read('/tmp/example_file.txt')
    except Exception as msg:
        print(msg)


def example_search_file_with_regex():
    """ Find mail servers in a hosts file that have IPs starting with 172. """
    my_file = FileAsObj('/etc/hosts')
    result = my_file.egrep('^172.*mail[0-9]')
    print(result)


def example_search_for_whole_line_using_contains():
    """ Find a complete line in file. """
    my_file = FileAsObj('/etc/hosts')
    if '127.0.0.1 localhost' in my_file:
        return True


def example_search_for_whole_line_using_check():
    """ Shorter version, find a complete line in file. """
    my_file = FileAsObj('/etc/hosts')
    return my_file.check('127.0.0.1 localhost')


def example_search_for_word_using_grep():
    """ Find a complete line in file. """
    my_file = FileAsObj('/etc/hosts')
    if my_file.grep('localhost'):
        return True


def example_add_line_to_file():
    """ Different methods to append a given line to the file, all work the same. """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.add('foo')
    my_file.append('bar')
    # Add a new line to my_file that contains the word 'lol' and print True|False if my_file was changed.
    print(my_file + 'lol')
    # Add line even if it already exists in the file.
    my_file.unique = False
    my_file.add('foo')


def example_add_list_of_lines_to_file():
    """
    Add a list() of strings, each on its own line.
    Same as the previous example you can use .append() or '+'.
    """
    my_file = FileAsObj('/tmp/example_file.txt')
    lines_to_add = ['simultaneous', 'money shot', 'remedy']
    my_file.add(lines_to_add)


def example_print_match_count():
    """ Print number of lines in the file (as it exists in memory) """
    my_file = FileAsObj('/tmp/example_file.txt')
    print(len(my_file))


def example_remove_lines_matching_substring():
    """ Remove all lines that CONTAIN 'bad string' """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.rm(my_file.grep('bad string'))
    my_file.save()


def example_remove_lines_matching_string():
    """ Remove all lines that ARE '# T0DO: remove this line.' (This matches an entire line.) """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.rm('# T0DO: remove this line.')
    my_file.save()


def example_remove_lines_matching_string_with_sub():
    """ Remove all lines that ARE "# T0DO: remove this line." using __sub__ shortcut. (This matches an entire line.) """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file - '# T0DO: remove this line.'
    my_file.save()


def example_remove_lines_matching_string_with_print():
    """ Remove all lines that ARE "# T0DO: remove this line." and print(True|False) if my_file was changed. """
    my_file = FileAsObj('/tmp/example_file.txt')
    print(my_file.rm('# T0DO: remove this line.'))
    my_file.save()


def example_get_lines_matching_substring():
    """ Get all lines that contain a # anywhere in the line. """
    my_file = FileAsObj('/tmp/example_file.txt')
    result = my_file.grep('#')
    return result


def example_print_lines_matching_substring():
    """ Print all lines that contain a # anywhere in the line. """
    my_file = FileAsObj('/tmp/example_file.txt')
    print(my_file.grep('#'))


def example_write_file_to_disk_if_changed():
    """ Try to remove all comments from a file, and save it if changes were made. """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.rm(my_file.egrep('^#'))
    if my_file.changed:
        my_file.save()


def example_show_files_change_log():
    """
    All actions that FileAsObj takes are logged internally in the log sub-class, this is required by some audits.
    You can view the log by calling __str__ on the sub-class. This example uses print()
    """
    my_file = FileAsObj('/tmp/example_file.txt')
    # ...any code that changes the file here...
    print(my_file.log)


def example_manually_update_change_log():
    """  You can inject an arbitrary message to the log sub-class by calling it. """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.log('A manual log entry.')


def example_sort_in_place():
    """ To sort contents in place after the file is read. """
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.sort()


def example_sort_during_read():
    """
    To sort contents during read().
    The .sorted attribute is checked every time contents are modified.
    Whenever a change occurs if sorted is True the contents are sorted with self.sort().
    """
    my_file = FileAsObj()
    my_file.sorted = True
    my_file.read('/tmp/example_file.txt')


def example_all():
    """
    Use a bunch of methods on a file.
    """
    my_file = FileAsObj()
    my_file.filename = '/tmp/example_file.txt'
    my_file.add('# First change!')
    my_file.save()
    my_file = FileAsObj('/tmp/example_file.txt')
    my_file.unique = True
    my_file.sorted = True
    my_file.add('1')
    my_file.add('1')
    my_file.add('2')
    my_file.add('20 foo')
    my_file.add('200 bar')
    my_file.add('# Comment')
    my_file.unique = False
    my_file.add('# Comment')
    my_file.add('# Comment')
    my_file.unique = True
    my_file.rm(my_file.egrep('^#.*'))
    my_file.rm(my_file.grep('foo'))
    my_file.replace(my_file.egrep('^2'), 'This line was replaced.')
    print(my_file)
    print(my_file.log)
