#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Get value from variable in python script (work with Python2.x and Python3.x)
    author & copyright :  Tadeusz Miszczyk
    version            :  1.0.0
    bash_version       >= 4.4.12
    usage              :
------------------- BEGIN CUT -------------------
#!/bin/bash
source "$(pwd)/${current_folder}../../bash/library/get_python_variable.sh"
        gpv_filepath="$(pwd)/${current_folder}../../python/library/mylib/variables.py"

# ----------------- Getting one variable example -----------------
gpv DOWNLOAD_FOLDER_TEMPLATE
echo ${DOWNLOAD_FOLDER_TEMPLATE}

# ----------------- Getting mass variables example -----------------
variables="DOWNLOAD_FOLDER_TEMPLATE SERVER_PORT SERVER_ADDRESS";

for variable in ${variables}
do
    gpv "${variable}"
    if [ "${!variable}" == "" ]; then
        echo -e "\n\Error while trying to access variable !!!!\n\n";
    else
        echo "${variable} : ${!variable}"
    fi
done
-------------------  END  CUT -------------------
'

#-----------------------------------------------------------------------------------------------------------------------

python_script='import sys
import os

file_name = sys.argv[1]
variable_name = sys.argv[2:][0]

directory, module_name = os.path.split(file_name)
module_name = os.path.splitext(module_name)[0]

path = list(sys.path)
sys.path.insert(0, directory)

try:
    module = __import__(module_name)
    variable_value = getattr(module, variable_name, None)
    print(variable_value)
finally:
    sys.path[:] = path
'

#-----------------------------------------------------------------------------------------------------------------------

gpv()
{
    if [ ! -f "${gpv_filepath}" ]; then
        echo -e "Python file not set.\nUsage in bash script:\ngpv_filepath=\"/path/to/python/script/filename.py\"\ngpv_filename was set as : \"${gpv_filepath}\""
        exit 1
    fi

    local varname
    for varname
    do
        read -r -d '' "${varname#*:}"
    done < <(python -c "$python_script" "$gpv_filepath" "${@%%:*}")
}

#-----------------------------------------------------------------------------------------------------------------------

