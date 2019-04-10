#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Common library for functions related with users.
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.0
    bash_version       >= 4.4.12
    usage              :  source "$(pwd)/$(dirname $0)/../library/users.sh"
'

#-----------------------------------------------------------------------------------------------------------------------

function check_email()
{
: ' Function return nothing or converted to lower case email.'    
    email=${1,,} # To reduce regex length - it check only for lower case letters (without [A-Z])
    regex="^[a-z0-9!#\$%&'*+/=?^_\`{|}~-]+(\.[a-z0-9!#$%&'*+/=?^_\`{|}~-]+)*@([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]([a-z0-9-]*[a-z0-9])?\$"
    if [[ ${email} =~ ${regex} ]] ; then
        echo "${email}"
    fi
}

#-----------------------------------------------------------------------------------------------------------------------

function CONTINUE_ONLY_IF_WITH_ROOT_PERMISSIONS()
{
    if [ "$(whoami)" != "root" ]; then
        echo "Please run with sudo or as a root!";
        exit 1
    fi
}

#-----------------------------------------------------------------------------------------------------------------------

function CONTINUE_ONLY_IF_WITH_USER_PERMISSIONS()
{
    if [ "$(whoami)" == "root" ]; then
        echo "Please run as a normal user!";
        exit 1
    fi
}

#-----------------------------------------------------------------------------------------------------------------------
