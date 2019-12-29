#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Some simple server functions
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.1
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

function add_new_certificate()
{   # $1   : domain_name
    # Usage: add_new_certificate shop.domain.com
    local     domain_name;     domain_name="$1";

    echo -e "Adding new certificate for (www.)${domain_name}"
    certbot --apache -d ${domain_name} -d www.${domain_name}

    if [ $(sudo certbot --apache certificates 2> /dev/null | grep ${domain_name} | wc -l) -gt 1 ]; then
        echo "The certificate for the server (www.)${domain_name} has been successfully added";
    else
        echo "Failed to add the certificate for the server (www.)${domain_name}";
    fi
}

