#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Simple files functions
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.0
    bash_version       >= 4.4.12
    usage              :  source "$(pwd)/$(dirname $0)/../library/files.sh"
'

#-----------------------------------------------------------------------------------------------------------------------

function change_extension()
{: ' This function return file_name (string) witch changed extension
     :param $1: file name 
     :param $2: new extension (like "html")
     Usage:
         change_extension "index.html"     "htm"  (will return: index.htm)
         change_extension "index.html.old" ""     (will return: index.html)
   '
    local file_name="$1";
    local new_extension="$2";
    if [ -z "${new_extension}" ]; then
        preext=".";
    else 
        preext="";
    fi
    echo "${file_name%${preext}${file_name##*.}}${new_extension}"
}

#-----------------------------------------------------------------------------------------------------------------------
