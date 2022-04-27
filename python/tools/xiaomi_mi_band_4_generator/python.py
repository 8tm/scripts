#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script parse rfconfig.jsonpickle to get rel5.1 repository links and branches.
"""
__author__ = 'Tadeusz Miszczyk'
__copyright__ = "Copyright 2017, Nokia, RF SCM"
__version__ = "1.0.0"
__maintainer__ = "Tadeusz Miszczyk"
__email__ = "tadeusz.miszczyk@nokia.com"

import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../../ci')

import common.variables

def get_args():
    """
    function for parsing cli arguments
    returns args - object containing arguments
    """
    parser = argparse.ArgumentParser(description="This script parse rfconfig.jsonpickle to get components and branches"
                                     " from REL5.1 repository")
    parser.add_argument("--path", required=True, help="Path where download and save files")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    export_components_list_to_csv(args.path)

