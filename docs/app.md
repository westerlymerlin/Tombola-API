# None

<a id="app"></a>

# app

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

Author: Gary Twinnington
URL: https://github.com/garytwinnington/tombola-py-web-app

<a id="app.subprocess"></a>

## subprocess

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.settings"></a>

## settings

<a id="app.VERSION"></a>

## VERSION

<a id="app.MotorClass"></a>

## MotorClass

<a id="app.logger"></a>

## logger

<a id="app.app"></a>

#### app

<a id="app.tom"></a>

#### tom

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Lists threads currently running

<a id="app.index"></a>

#### index

```python
@app.route('/', methods=['GET', 'POST'])
def index()
```

Main web page handler, shows status page via the index.html template

<a id="app.statusdata"></a>

#### statusdata

```python
@app.route('/statusdata', methods=['GET'])
def statusdata()
```

Status data read by javascript on default website

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API Endpoint for programatic access - needs request data to be posted in a json file

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Displays the application log file via the logviewer.html template

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

Displays the gunicorn access log file via the logviewer.html template

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

Displays the gunicorn error log file via the logviewer.html template

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Displays the last 2000 lines if the system log file via the logviewer.html template

