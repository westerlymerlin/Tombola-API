#!/bin/bash

# stop services

echo "
**** stopping Gunicorn and python app ****
"
sudo systemctl stop gunicorn.service

echo "
**** stopping nginx ****
"
sudo systemctl stop nginx

echo "
******** services stopped ********
"
