#!/bin/bash

# CICD Script to check if there is a new version in github and auto-deploy it

echo -e "\033[0;33m **** fetching the master branch from github **** \033[0m"
cd /home/tompi/github/UCL-tombola-API/
git fetch origin master
echo -e "\033[0;33m **** checking if a newer version of the app is available in github **** \033[0m"
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo -e "\033[0;32m ******** app is up-to-date so nothing to do - exiting ******** \033[0m"
elif [ $LOCAL = $BASE ]; then
    echo -e "\033[0;31m **** newer version in github so I will update the app **** \033[0m"
    git pull origin master
    cd /home/tompi
    echo -e "\033[0;33m **** stopping gunicorn and python app **** \033[0m"
    sudo systemctl stop gunicorn.service
    echo -e "\033[0;33m **** gunicorn and python stopped **** \033[0m"
    echo -e "\033[0;33m **** copying files from cloned github repo **** \033[0m"
    cp -r /home/tompi/github/UCL-tombola-API/*  /home/tompi/
    echo -e "\033[0;33m **** all files copied **** \033[0m"
    echo -e "\033[0;33m **** setting flags on bin folder **** \033[0m"
    chmod 755 /home/tompi/bin/*.sh
    echo -e "\033[0;33m **** restarting gunicorn and python **** \033[0m"
    sudo systemctl start gunicorn.service
    echo -e "\033[0;33m **** gunicorn started **** \033[0m"
    echo -e "\033[0;32m ******** new deployment has completed - please test ******** \033[0m"
else
    echo -e "\033[0;31m There was a problem so please check and manually update \033[0m"
fi

