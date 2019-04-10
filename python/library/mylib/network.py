#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Network module """

__author__ = 'Tadeusz Miszczyk'
__version__ = "1.1.0"

# ----------------------------------------------------------------------------------------------------------------------

import socket

import certifi
import requests
import urllib3
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------


def my_external_ip_address():
    # TODO - check if there is an active internet connection
    return requests.get("http://checkip.dyndns.org").text.split(': ', 1)[1].split('</body></html>', 1)[0]

# ----------------------------------------------------------------------------------------------------------------------


def my_internal_ip_address():
    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

# ----------------------------------------------------------------------------------------------------------------------


def get_hostname(long=False):
    return socket.getfqdn() if long else socket.gethostname()

# ----------------------------------------------------------------------------------------------------------------------


def get_website_source_code(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    resources = http.request('GET', url)
    return BeautifulSoup(resources.data.decode('utf-8'), 'html.parser')

# ----------------------------------------------------------------------------------------------------------------------


def check_connection(address, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if connection.connect_ex((address, port)) == 0:
        connected = True
    else:
        connected = False
    connection.close()
    return connected

# ----------------------------------------------------------------------------------------------------------------------

