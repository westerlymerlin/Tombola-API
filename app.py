"""
Tombola Web Application

A Flask-based web application for controlling and monitoring a tombola/motor device.
This module provides both a web interface and API endpoints for programmatic control.

Features:
- Web interface for real-time motor control and monitoring
- RESTful API for programmatic access (API key required)
- System monitoring (CPU temperature, threads)
- Access to application and system logs
- Motor control with speed regulation and stop timer functionality

This application is designed to be served by Gunicorn in a production environment.

Author: Gary Twinn
URL: https://github.com/westerlymerlin
"""

import subprocess
from threading import enumerate as enumerate_threads
from flask import Flask, render_template, jsonify, request, Response, send_file, send_from_directory
from app_control import settings, VERSION
from logmanager import logger
from motor_class import MotorClass
from camera_class import video_camera_instance_0


logger.info('Starting Tombola web app version %s', VERSION)
app = Flask(__name__)
tom = MotorClass()

logger.info('Api-Key = %s', settings['api-key'])


def threadlister():
    """Lists threads currently running"""
    appthreads = []
    for appthread in enumerate_threads():
        appthreads.append([appthread.name, appthread.native_id])
    return appthreads

@app.errorhandler(500)
def internal_server_error(_):
    """
    Handles HTTP 500 Internal Server Error responses.

    This function serves a custom 500 error HTML page whenever an Internal Server
    Error occurs in the application. The response's status code is explicitly set
    to 500, ensuring proper error handling and browser recognition of the error.
    """
    response = send_from_directory('static', '500.html')
    response.status_code = 500
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main web page handler, shows status page via the index.html template"""
    if request.method == 'POST':
        # print(request.form)
        if len(request.form) == 0:
            logger.warning('Index page: Invalid Web Post Received - returning 405 to %s',
                           request.headers['X-Forwarded-For'])
            return '<!doctype html><html lang=en><title>405 Method Not Allowed</title>' \
                   '<h1>Method Not Allowed</h1>' \
                   '<p>The method is not allowed for the requested URL.</p>', 405
        logger.debug('Index page: Web Post received')
        tom.parse_control_message(request.form)
    return render_template('index.html', settings=settings, version=VERSION,
                           rpm=tom.requested_rpm, stoptimer=tom.get_stop_time(), threadcount=threadlister())


@app.route('/statusdata', methods=['GET'])
def statusdata():
    """Status data read by javascript on default website"""
    ctrldata = tom.controller_query()  # Query the motor controller for current data
    with open(settings['cputemp'], 'r', encoding='UTF-8') as f:  # Get CPU temperature
        log = f.readline()
    f.close()
    cputemperature = round(float(log) / 1000, 1)
    ctrldata['cpu'] = cputemperature
    return jsonify(ctrldata), 201


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programmatic access - needs request data to be posted in a json file"""
    try:
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == settings['api-key']:  # check for correct API key
                status = tom.parse_control_message(request.json)
                return jsonify(status), 201
            logger.warning('API: access attempt using an invalid Api-Key')
            return 'Api-Key unauthorised', 401
        logger.warning('API: access attempt without an Api-Key')
        return 'Api-Key missing', 401
    except KeyError:
        logger.warning('API: bad json message')
        return "badly formed json message", 400

@app.route('/VideoFeed0')
def video_feed0():
    """The image feed read by the browser for camera 0"""
    return Response(video_camera_instance_0.mpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pylog')  # display the application log
def showplogs():
    """Displays the application log file via the logviewer.html template"""
    with open(settings['logfilepath'], 'r', encoding='UTF-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logviewer.html', rows=logs, log='Tombola log', version=VERSION)


@app.route('/guaccesslog')  # display the gunicorn access log
def showgalogs():
    """Displays the gunicorn access log file via the logviewer.html template"""
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r', encoding='UTF-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logviewer.html', rows=logs, log='gunicorn access log', version=VERSION)


@app.route('/guerrorlog')  # display the gunicorn error log
def showgelogs():
    """Displays the gunicorn error log file via the logviewer.html template"""
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r', encoding='UTF-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logviewer.html', rows=logs, log='gunicorn error log', version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """Displays the last 2000 lines if the system log file via the logviewer.html template"""
    log = subprocess.Popen('/bin/journalctl -n 2000', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logviewer.html', rows=logs, log='system log', version=VERSION)

@app.route('/documentation')
def download_manual():
    """
    Handles the request to download the application's manual.

    This function serves the PDF manual of the application as a downloadable
    attachment. The manual file's name is retrieved from the application
    settings and provided as the download name.
    """
    return send_file('README.pdf', download_name='tombola-api.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run()
