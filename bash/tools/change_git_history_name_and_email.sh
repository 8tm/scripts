#!/bin/bash
# -*- coding: utf-8 -*-
: '
    description        :  Script can change all emails and names to new one.
    author & copyright :  Tadeusz Miszczyk
    version            :  1.1.1
    bash_version       >= 4.4.12
    usage              :  ./script_name.sh "old_email@gmail.com" "new_email@gmail.com" "New user name"
'

#-----------------------------------------------------------------------------------------------------------------------

source "$(pwd)/$(dirname $0)/../library/users.sh"

#-----------------------------------------------------------------------------------------------------------------------

function usage()
{
: ' Function return help about program usage.
    It need 3 parameters : 
        1) OLD email address
        2) NEW email address
        3) name
'

    echo -e "\n Usage instruction : 
     script_name.sh \"old_email\" \"new_email\" \"name\"\n"
}

#-----------------------------------------------------------------------------------------------------------------------

function main()
{
: 'From $(git help filter-branch) and from $(git help git-commit-tree) we know we can change :
 + GIT_AUTHOR_NAME
 + GIT_AUTHOR_EMAIL
 - GIT_AUTHOR_DATE
 + GIT_COMMITTER_NAME
 + GIT_COMMITTER_EMAIL
 - GIT_COMMITTER_DATE
   but for this script i need only to change name and email of author and commiter'

    email_old="$(check_email $1)"
    email_new="$(check_email $2)"
    name="$3"

    # If params are not empty (valid emails)
    if [ ! -z ${email_old} ] && [ ! -z ${email_new} ] ; then
        git filter-branch -f --env-filter '
            if [ "$GIT_COMMITTER_EMAIL" = "'"${email_old}"'" ] ; then
                export GIT_COMMITTER_NAME="'"${name}"'"
                export GIT_COMMITTER_EMAIL="'"${email_new}"'"
            fi
            if [ "$GIT_AUTHOR_EMAIL" = "'"${email_old}"'" ] ; then
                export GIT_AUTHOR_NAME="'"${name}"'"
                export GIT_AUTHOR_EMAIL="'"${email_new}"'"
            fi
        ' --tag-name-filter cat -- --branches --tags
    fi
}

#-----------------------------------------------------------------------------------------------------------------------

if [ $# -ne 3 ] ; then
    usage;  # Show usage information
    exit 1; # Exit with error
else
    # run main function with old_email new_email name
    main "$1" "$2" "$3"
fi

#-----------------------------------------------------------------------------------------------------------------------
