#!/bin/bash

# script to restart the services

echo "
**** stoping gunicorn and python app ****
"
sudo systemctl stop gunicorn.service

echo "
**** stopping nginx ****
"
sudo systemctl stop nginx

echo "
**** staring nginx ****
"
sudo systemctl start nginx

echo "
**** starting gunicorn and python app ****
"
sudo systemctl start gunicorn.service

echo "
******** restart completed ********
"
