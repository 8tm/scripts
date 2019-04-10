#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Tool - send email about lost connections"""

__author__ = "Tadeusz Miszczyk"
__version__ = "1.0.0"

# ----------------------------------------------------------------------------------------------------------------------

import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../library/')

import mylib.email
import mylib.network
import mylib.templates
import mylib.variables_sensitive

# ----------------------------------------------------------------------------------------------------------------------


def get_lost_services(services):
    dead_services = []
    for server in services:
        for port in services[server]:
            if not mylib.network.check_connection(server, port):
                dead_services.append("<b>{0}</b>:{1}".format(server, port))
    return dead_services

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    lost_services = get_lost_services(mylib.variables_sensitive.SERVICES)
    print("Checked all services!")
    email_title = "{0} service!".format(len(lost_services))

    if lost_services:
        zm = {'title': "",
              'services': "{0}<br><br>".format("<br><br>".join([service for service in lost_services]))}

        mylib.email.send([mylib.variables_sensitive.EMAIL_LOGIN],
                         "SERVICES - {0} service(s) lost!".format(len(lost_services)),
                         "",
                         mylib.templates.Email("lost_services").report(**zm),
                         [])

# ----------------------------------------------------------------------------------------------------------------------
