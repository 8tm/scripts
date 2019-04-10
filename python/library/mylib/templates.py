#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Templates module """

__author__ = 'Tadeusz Miszczyk'
__version__ = "1.0.0"

# ----------------------------------------------------------------------------------------------------------------------

import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../library/')
import mylib.variables

# ----------------------------------------------------------------------------------------------------------------------


class Email():

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, template_name):
        self.template_name = template_name
        self.path = mylib.variables.EMAIL_TEMPLATES

    # ------------------------------------------------------------------------------------------------------------------

    def content(self):
        with open(self.path.format(self.template_name), "r", encoding="utf-8") \
                as email_template:
            message = str(email_template.read().replace('\n', ''))
        return message

    # ------------------------------------------------------------------------------------------------------------------

    def report(self, **params):
        with open(self.path.format(self.template_name), "r", encoding="utf-8") \
                as email_template:
            message = str(email_template.read().replace('\n', ''))
        for value in params:
            message = message.replace("__{0}__".format(value), params[value])
        return message

    # ------------------------------------------------------------------------------------------------------------------
