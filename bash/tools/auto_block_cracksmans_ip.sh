#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Automatically block all cracksmans ip (from logs)
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.0
    bash_version       >= 4.4.12
    usage              :  sudo ./auto_block_cracksmans_ip.sh
'

#-----------------------------------------------------------------------------------------------------------------------

current_folder=$(dirname $0)
if [ "${current_folder}" == "." ]; then current_folder=""
    else                                current_folder="${current_folder}/"
fi

#-----------------------------------------------------------------------------------------------------------------------

source "$(pwd)/${current_folder}../../bash/library/users.sh"
source "$(pwd)/${current_folder}../../bash/library/get_python_variable.sh"
        gpv_filepath="$(pwd)/${current_folder}../../python/library/mylib/variables_sensitive.py"
        gpv EXTERNAL_IP_ADDRESS

CONTINUE_ONLY_IF_WITH_ROOT_PERMISSIONS

#-----------------------------------------------------------------------------------------------------------------------

cp /var/log/apache2/other_vhosts_access.log* . 2> /dev/null
gunzip * 2> /dev/null

ip_addresses=""

for filename in $(ls -lh | grep other_vhosts_access | awk '{print $9}');
do
    for ip_address in $(cat ${filename} | grep password | awk '{print $2}' | sort -u)
    do
        if [ "${ip_address}" != "${EXTERNAL_IP_ADDRESS}" ]; then
            ip_addresses="${ip_addresses}\n${ip_address}"
        fi
    done

    for ip_address2 in $(cat ${filename} | grep " 404 " | awk '{print $2}' | uniq -c | sort -nr | \
    sed -e 's/  /-/g' -e 's/ /_/g' -e 's/-_//g' -e 's/-//g')
    do
        counter=$(echo ${ip_address2} | awk 'BEGIN {FS="_"}{print $1}')
        ip_address=$(echo ${ip_address2} | awk 'BEGIN {FS="_"}{print $2}')
        if [ "${ip_address}" != "${EXTERNAL_IP_ADDRESS}" ]; then
            if [ ${counter} -gt 150 ]; then
                ip_addresses="${ip_addresses}\n${ip_address}"
            fi
        fi
    done
done

ip_addresses="$(echo -e "${ip_addresses}" | sort -u)"
for ip in ${ip_addresses};
do
    if [ $(iptables -L INPUT -v -n | grep ${ip} | wc -l) != "0" ]; then
        echo " [Exist] ${ip}"
    else
        echo " [ADDED] ${ip}"
        iptables -A INPUT -s "${ip}" -j DROP
    fi
done

echo -e "\n Currently added ip's : $(iptables -L INPUT -v -n | wc -l)"
echo -e " Command : iptables -L INPUT -v -n\n$(iptables -L INPUT -v -n)\n"


rm *.log* 2> /dev/null

#-----------------------------------------------------------------------------------------------------------------------
