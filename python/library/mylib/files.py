#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Files module """

__author__ = 'Tadeusz Miszczyk'
__version__ = "1.0.0"

# ----------------------------------------------------------------------------------------------------------------------

from contextlib import contextmanager
from hashlib import sha1
from hashlib import md5
from hashlib import sha256
from hashlib import sha512
import hashlib
import os
import shutil
import stat
import tempfile

# ----------------------------------------------------------------------------------------------------------------------

# change it !
def list_dir(path, show_hidden=False):
    try:
        files = os.listdir(path)
    except:
        raise
    else:
        if not show_hidden:
            return [file for file in files if not file.startswith('.')]
        else:
            return files

# ----------------------------------------------------------------------------------------------------------------------


def get_file_size(path):
    return os.stat(path).st_size

# ----------------------------------------------------------------------------------------------------------------------


def checksum(path, sum_type):
    """
    Checksum of a file
    """
    with open(path, 'rb') as handle:
        try:
            data = handle.read()
        except MemoryError as Error:
            #print("MEMORY-ERROR : {0}: ".format(path))
            return "MEMORY-ERROR"
        except (OSError, os.error) as Error:
            #print("OS error")
            #print('errno:', Error.errno)
            #print('err code:', Error.errorcode[Error.errno])
            #print('err message:', os.strerror(Error.errno))
            return "OS-ERROR : {0}: ".format(path)
        except (IOError, os.error) as Error:
            #print("IO error")
            #print('errno:', Error.errno)
            #print('err code:', Error.errorcode[Error.errno])
            #print('err message:', os.strerror(Error.errno))
            return "IO-ERROR : {0}: ".format(path)
        except:
            #print("Unknown ERROR ocured when trrying to open : {0}: ".format(path))
            return "UNKNOWN ERROR : {0}: ".format(path)
    if sum_type == 'sha1':
        sum = sha1(data).hexdigest()
    elif sum_type == 'sha256':
        sum = sha256(data).hexdigest()
    elif sum_type == 'sha512':
        sum = sha512(data).hexdigest()
    elif sum_type == 'md5':
        sum = md5(data).hexdigest()
    else:
        sum = hashlib.sum_type.hexdigest()
    return sum

# ----------------------------------------------------------------------------------------------------------------------


def rmtree(dir):
    """
    Delete files and folder in recursive mode.
    """
    if os.path.exists(dir):
        for path, _, file_names in os.walk(dir):
            for file_name in file_names:
                try:
                    os.chmod(os.path.join(path, file_name), stat.S_IWRITE)
                except OSError:
                    pass
        shutil.rmtree(dir)

# ----------------------------------------------------------------------------------------------------------------------
#    contextmanagers :
#        with func_name(params) as handle:
#            (...)
# ----------------------------------------------------------------------------------------------------------------------


@contextmanager
def chdir(path):
    """
    Go to directory and back after done
    """
    previous_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(previous_path)

# ----------------------------------------------------------------------------------------------------------------------


@contextmanager
def temp():
    """
    Temporary directory in /tmp/ folder, removed after done.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
    finally:
        rmtree(temp_dir)

# ----------------------------------------------------------------------------------------------------------------------
