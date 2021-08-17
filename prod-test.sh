#!/bin/bash
sleep 10
EXITSTATUS=0

# website data
URL="https://blobber.tech"
PAGES="/ /dashboard /login /register /faq /about"
METHODS="GET POST"

# Testing endpoints with request methods
echo ${cyan}Testing endpoints with request methods${reset_color}
for PAGE in $PAGES; do
for METHOD in $METHODS; do

GETVAR=$(curl -LI $URL$PAGE -o /dev/null -w '%{http_code}\n' -s -X $METHOD) 
STATCAT=${GETVAR:0:1}
if [[ $STATCAT == 2 ]]; then
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${green}'SUCCESS'${reset_color}
elif [[ $GETVAR == 400 ]]; then
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${purple}"Bad Request"${reset_color}
elif [[ $GETVAR == 405 ]]; then 
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${yellow}'METHOD NOT ALLOWED'${reset_color}
else
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${red}'ERROR'${reset_color}
EXITSTATUS=1
fi
done
done

# Function to post endpoints
testing_endpoint () {
GETVAR=$1
if [[ $GETVAR == $2 ]]; then
echo $GETVAR ${green}'SUCCESS'${reset_color}
else
echo $GETVAR ${red}'ERROR'${reset_color}
EXITSTATUS=2
fi
}

echo ${cyan}Posting to /login endpoint with register user and empty password${reset_color}
testing_endpoint "$(curl -sX POST -d "username=test" -o /dev/null -w '%{http_code}\n' $URL'/login')" "400"

echo Posting to /register endpoint with usr test, pw test pw test
testing_endpoint "$(curl -sX POST -d "username=test&password=test&password2=test" -o /dev/null -w '%{http_code}\n' $URL'/register')" "400"


echo 'EXIT STATUS = '$EXITSTATUS
exit $EXITSTATUS

