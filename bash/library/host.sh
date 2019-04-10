#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Some simple server functions
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.0
    bash_version       >= 4.4.12
    usage              :  source "$(pwd)/$(dirname $0)/../library/host.sh"
'

#-----------------------------------------------------------------------------------------------------------------------

function add_new_host()
{   # $1 : host_address
    # $2 : host_name
    local host_address; host_address="$1";
    local host_name; host_name="$2";
    echo -e "${host_address}\t${host_name}" >> /etc/hosts
}

#-----------------------------------------------------------------------------------------------------------------------
