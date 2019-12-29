#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Add new virtual host to server
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.1
    bash_version       >= 4.4.12
    usage              :  sudo ./add_virtual_host.sh subdomain.domain.com
'

#-----------------------------------------------------------------------------------------------------------------------

current_folder=$(dirname $0)
if [ "${current_folder}" == "." ]; then current_folder=""
    else                                current_folder="${current_folder}/"
fi

#-----------------------------------------------------------------------------------------------------------------------

source "$(pwd)/${current_folder}../../bash/library/users.sh"
source "$(pwd)/${current_folder}../../bash/library/host.sh"
source "$(pwd)/${current_folder}../../bash/library/get_python_variable.sh"
        gpv_filepath="$(pwd)/${current_folder}../../python/library/mylib/variables_sensitive.py"
        gpv EXTERNAL_SERVER_EMAIL

CONTINUE_ONLY_IF_WITH_ROOT_PERMISSIONS

#-----------------------------------------------------------------------------------------------------------------------

virtual_host="$1"

if [ -z "${virtual_host}" ]; then
    echo "Add domain name as a first param."
    exit 1
fi

#-----------------------------------------------------------------------------------------------------------------------

index_path="/var/www/${virtual_host}/public_html/index.html"
index_html="
<html>
    <head>
        <title>${virtual_host}</title>
    </head>
    <body>
        <h1>(www.)${virtual_host} - virtual host created.</h1>
    </body>
</html>
"
virtual_host_config="
<VirtualHost *:80>
    ServerAdmin ${EXTERNAL_SERVER_EMAIL}
    DocumentRoot $(dirname $index_path)
    ServerName ${virtual_host}
    ServerAlias www.${virtual_host}
    ServerAlias *.${virtual_host}
    ErrorLog ${APACHE_LOG_DIR}/${virtual_host}.error.log
    CustomLog ${APACHE_LOG_DIR}/${virtual_host}.access.log combined
</VirtualHost>
"

#-----------------------------------------------------------------------------------------------------------------------

mkdir -p "$(dirname $index_path)" && echo "${index_html}" > "${index_path}"
chown -R www-data:www-data "$(dirname $index_path)"
chmod -R 755 "$(dirname $index_path)"

echo "${virtual_host_config}" > "/etc/apache2/sites-available/${virtual_host}.conf"

a2ensite ${virtual_host}
service apache2 reload

#-----------------------------------------------------------------------------------------------------------------------

add_new_host "127.0.0.1" "${virtual_host}"
add_new_host "127.0.0.1" "www.${virtual_host}"

add_new_certificate "${virtual_host}"

#-----------------------------------------------------------------------------------------------------------------------
