# None

<a id="app_control"></a>

# app\_control

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

<a id="app_control.random"></a>

## random

<a id="app_control.json"></a>

## json

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.writesettings"></a>

#### writesettings

```python
def writesettings()
```

Updates the 'LastSave' field in the settings dictionary with the current datetime
and writes the updated settings dictionary to a JSON file.

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

Initialises and returns the default settings for the application.

This function provides the default configuration required for the application to function. It creates a
dictionary with predefined default values such as system logs, paths, hardware configurations,
and operational parameters. The intended use of this function is to establish a baseline for the
app's settings when it is run for the first time.

<a id="app_control.generate_api_key"></a>

#### generate\_api\_key

```python
def generate_api_key(key_len)
```

generate a new random api-key

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Reads settings from a JSON file.

This function attempts to load a JSON file named 'settings.json' into
a dictionary. If the file is not found, it handles the exception and
returns an empty dictionary. The file is expected to be UTF-8 encoded.

<a id="app_control.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

Loads the application settings and updates them based on the values read from an external
source. The method compares the existing `settings` with the default settings, and updates
the `settings` with the values if available. If a default value is used for any setting
due to its absence in the external source, the updated settings are saved back.

<a id="app_control.settings"></a>

#### settings

