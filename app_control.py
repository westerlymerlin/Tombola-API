"""
Settings Management Module

This module handles application configuration settings with JSON persistence.
It provides functionality to read, write, and initialize application settings
from a settings.json file with fallback to defaults when settings are missing.

Features:
- Automatic creation of settings.json if not present
- Default values for all settings
- Persistence of settings to JSON format
- Automatic detection and addition of new settings
- Timestamp tracking of settings modifications

Usage:
    import from app_control import settings, writesettings

"""

import random
import json
from datetime import datetime


VERSION = '1.8.2'


def writesettings():
    """
    Updates the 'LastSave' field in the settings dictionary with the current datetime
    and writes the updated settings dictionary to a JSON file.
    """
    settings['LastSave'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w', encoding='UTF-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    """
    Initialises and returns the default settings for the application.

    This function provides the default configuration required for the application to function. It creates a
    dictionary with predefined default values such as system logs, paths, hardware configurations,
    and operational parameters. The intended use of this function is to establish a baseline for the
    app's settings when it is run for the first time.
    """
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'app-name': 'Tombola-Py',
                 'STW_forward': 1142,
                 'STW_register': 99,
                 'STW_stop': 0,
                 'api-key': 'change-me',
                 'autoshutdown': True,
                 'baud': 9600,
                 'bytesize': 8,
                 'clear_buffers_after_call': True,
                 'clear_buffers_before_call': True,
                 'control_start_register': 2,
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'database_path': './database/',
                 'gunicornpath': './logs/',
                 'logappname': 'Tombola-Py',
                 'logfilepath': './logs/tombola.log',
                 'loglevel': 'INFO',
                 'port': '/dev/ttyUSB0',
                 'read_length': 16,
                 'reading_start_register': 23,
                 'rpm_active_LED': 17,
                 'rpm_frequency': 11.91,
                 'rpm_magnets': 48,
                 'rpm_max': 99.9,
                 'rpm_sensor_GPIO': 27,
                 'rpm_timeout_seconds': 2,
                 'shutdowntime': '08:00:00',
                 'station': 1,
                 'stopbits': 1,
                 'syslog': '/var/log/syslog',
                 'serialtimeout': 0.75,
                 'wait_timeout': 10,
                 'camera0_enabled': False,
                 'camera0': {
                     'cameraBrightness': 10,
                     'cameraContrast': 10,
                     'cameraFPS': 5,
                     'cameraGain': 0,
                     'cameraGamma': 0,
                     'cameraHeight': 640,
                     'cameraHue': 0,
                     'cameraID': 0,
                     'cameraSaturation': 0,
                     'cameraSharpness': 0,
                     'cameraWidth': 480
                 }
                 }
    return isettings

def generate_api_key(key_len):
    """generate a new random api-key"""
    allowed_characters = "ABCDEFGHJKLMNPQRSTUVWXYZ-+~abcdefghijkmnopqrstuvwxyz123456789"
    return ''.join(random.choice(allowed_characters) for _ in range(key_len))


def readsettings():
    """
    Reads settings from a JSON file.

    This function attempts to load a JSON file named 'settings.json' into
    a dictionary. If the file is not found, it handles the exception and
    returns an empty dictionary. The file is expected to be UTF-8 encoded.
    """
    try:
        with open('settings.json', encoding='UTF-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}


def loadsettings():
    """
    Loads the application settings and updates them based on the values read from an external
    source. The method compares the existing `settings` with the default settings, and updates
    the `settings` with the values if available. If a default value is used for any setting
    due to its absence in the external source, the updated settings are saved back.
    """
    global settings
    settingschanged = 0
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print(f'settings[{item}] Not found in json file using default')
            settingschanged = 1
    if settings['api-key'] == 'change-me':
        settings['api-key'] = generate_api_key(30)
        settingschanged = 1
    if settingschanged == 1:
        writesettings()


settings = initialise()
loadsettings()
