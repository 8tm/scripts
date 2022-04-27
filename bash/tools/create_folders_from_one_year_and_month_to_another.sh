#!/bin/bash

function check_number_of_params()
{
    local params=$1
    local number_of_params=$2
    if [ ${params#} -lt ${number_of_params} ]; then
        echo "1"
        return 1
        exit 1
    else
        echo "0"
        return 0
    fi
}

check_number_of_params "$#" 5

for (( rok=2012; rok < 2020; rok++ ));
do
    for (( miesiac=1; miesiac <13; miesiac++ ));
    do
        if [ ${miesiac} -lt 10 ]; then mmiesiac="0${miesiac}";
        else mmiesiac=${miesiac};
        fi;
        echo mkdir ${rok}-${mmiesiac};
   done;
done;

