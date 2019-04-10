#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" System module """

__author__ = 'Tadeusz Miszczyk'
__version__ = "1.0.0"

# ----------------------------------------------------------------------------------------------------------------------

import datetime
import errno
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

# ----------------------------------------------------------------------------------------------------------------------


def monitor_object():
    """ Monitor object
    :return: Returns monitor object
    """
    win = Gtk.Window()
    win.set_keep_above(True)
    return win

# ----------------------------------------------------------------------------------------------------------------------


def get_monitors_number(monitor_object):
    """ Returns monitor count
    :param monitor_object: monitor object returned from monitor_object()
    :return:
    """
    scr = monitor_object.get_screen()
    return scr.get_n_monitors()

# ----------------------------------------------------------------------------------------------------------------------


def get_monitor_size(monitor_object, monitor_id):
    """ Get width and height of monitor_id
    :param monitor_object: monitor object returned from monitor_object()
    :param monitor_id: (int) id of monitor
    :return: (str) like 1920x1080
    """
    scr = monitor_object.get_screen()
    width = scr.get_monitor_geometry(monitor_id).width
    height = scr.get_monitor_geometry(monitor_id).height
    return "{0}x{1}".format(width, height)

# ----------------------------------------------------------------------------------------------------------------------


def run_command(command):
    """ Run command
    :param command: (str) bash command to run
    :return: output with output and errors
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate()
    return output, errors

# ----------------------------------------------------------------------------------------------------------------------


def is_locked(locker_name):
    """ Check if workstation is locked
    :param locker_name: locker app name
    :return: boolean status of process
    """
    try:
        proc = subprocess.check_output("ps aux | grep %s | grep -v grep | awk '{print $2}'" % locker_name, shell=True)
    except subprocess.CalledProcessError:
        proc = b''

    if proc == b'':
        return False
    else:
        return True

# ----------------------------------------------------------------------------------------------------------------------


def create_symlink(source, destination, forced=False):
    """ Create symlink
    :param source: Path to file
    :param destination: Path to new link
    :return: boolean status of operation
    """
    try:
        os.symlink(source, destination)
    except OSError as err:
        if err.errno == errno.EEXIST and forced:
            os.remove(destination)
            os.symlink(source, destination)
            return True
        else:
            return False

# ----------------------------------------------------------------------------------------------------------------------


def get_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ----------------------------------------------------------------------------------------------------------------------
