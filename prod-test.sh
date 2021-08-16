#!/bin/bash

EXITSTATUS=0

# website data
URL="https://blobber.tech"
PAGES="/ /dashboard /login /register /faq /about"
METHODS="GET POST DELETE PUT PATCH"

# Testing endpoints with request methods
echo ${cyan}Testing endpoints with request methods${reset_color}
for PAGE in $PAGES; do
for METHOD in $METHODS; do

GETVAR=$(curl -LI $URL$PAGE -o /dev/null -w '%{http_code}\n' -s -X $METHOD) 
STATCAT=${GETVAR:0:1}
if [[ $STATCAT == 2 ]]; then
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${green}'SUCCESS'${reset_color}
elif [[ $GETVAR == 418 ]]; then
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${purple}"I'm a teapot"${reset_color}
elif [[ $GETVAR == 405 ]]; then 
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${yellow}'METHOD NOT ALLOWED'${reset_color}
else
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${red}'ERROR'${reset_color}
EXITSTATUS=1
fi
done
done

echo 'EXIT STATUS = '$EXITSTATUS
exit $EXITSTATUS

