# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[app](./app.md)  
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

[app_control](./app_control.md)  
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

[logmanager](./logmanager.md)  
Logging Configuration and Management

This module provides centralized logging configuration and management for the application.
Configures logging formats, handlers, and log file management to ensure consistent
logging across all application components.

Features:
    - Standardized log formatting
    - File-based logging with rotation
    - Log level management
    - Thread-safe logging operations

Exports:
    logger: Configured logger instance for use across the application

Usage:
    from logmanager import logger

    logger.info('Operation completed successfully')
    logger.warning('Resource threshold reached')
    logger.error('Failed to complete operation')

Log Format:
    Timestamps, log levels, and contextual information are automatically included
    in each log entry for effective debugging and monitoring.

Log Files:
    Logs are stored with automatic rotation to prevent excessive disk usage
    while maintaining historical records.

[motor_class](./motor_class.md)  
Motor Control Module for V20 Controller

This module provides a comprehensive interface for controlling an electric motor via a V20 controller
using Modbus RTU protocol over RS485. It handles motor speed control, direction, auto-shutdown,
and monitoring of motor parameters including RPM, voltage, and current.

Key features:
- Two-way communication with V20 motor controller via Modbus RTU
- Real-time RPM monitoring and speed adjustment
- Auto-shutdown capability based on configurable timer
- Error handling for connection issues and timeouts
- Comprehensive logging of motor operations and errors

Dependencies:
- minimalmodbus: Handles Modbus RTU communication
- serial: Manages serial port connections
- rpm_class: Provides actual motor speed measurement
- app_control: Manages application settings
- logmanager: Handles logging

[rpm_class](./rpm_class.md)  
RPM Calculation Module

This module provides functionality to calculate vehicle wheel RPM (Revolutions Per Minute)
by processing pulses from an ABS (Anti-lock Braking System) sensor connected to a Raspberry Pi GPIO.

The module:
- Detects and timestamps ABS sensor pulses via GPIO input
- Calculates RPM based on rolling averages of pulse intervals
- Handles timeout detection for wheel stoppage
- Provides both RPM values and raw timing data

Requirements:
- Raspberry Pi with GPIO configured
- ABS sensor connected to the specified GPIO pin
- Configuration settings from app_control.settings

[tom_cmd](./tom_cmd.md)  
A basic command line app to allow a user connected to the raspberry pi console via TTY or SSH
to send stop start messages to the app.


---


  
-------
#### Copyright (C) 2025 Gary Twinn  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.  
  
  ##### Author: Gary Twinn  
  
 -------------
  
