# None

<a id="motor_class"></a>

# motor\_class

Motor Control Module for V20 Controller

This module provides a comprehensive interface for controlling an electric motor via a V20 controller
using Modbus RTU protocol over RS485. It handles motor speed control, direction, auto-shutdown,
and monitoring of motor parameters including RPM, voltage, and current.
Provides a motor control interface utilising Modbus communication.

<a id="motor_class.sleep"></a>

## sleep

<a id="motor_class.Timer"></a>

## Timer

<a id="motor_class.datetime"></a>

## datetime

<a id="motor_class.minimalmodbus"></a>

## minimalmodbus

<a id="motor_class.serialutil"></a>

## serialutil

<a id="motor_class.settings"></a>

## settings

<a id="motor_class.writesettings"></a>

## writesettings

<a id="motor_class.RPMClass"></a>

## RPMClass

<a id="motor_class.logger"></a>

## logger

<a id="motor_class.MotorClass"></a>

## MotorClass Objects

```python
class MotorClass()
```

Represents a motor controller that interfaces with an RS485 communication protocol.

This class provides functionality to initialize and control a motor using commands
and queries sent over RS485. The motor controller adjusts various operational parameters
such as speed, direction, and frequency based on user input and feedback from the motor.
It includes mechanisms for monitoring the motor's current state and automatically adjusting
its parameters to maintain desired performance levels. The class also handles communication
errors and ensures that the controller operates within its preconfigured limits.

Attributes:
    command_start_register (int): Register address for sending control commands.
    stw_control_register (int): Register address for sending start/stop commands.
    query_start_register (int): Register address to initiate data queries.
    read_length (int): Number of registers to read during a query.
    direction (int): Indicates motor direction; 0 for forward, 1 for reverse.
    frequency (int): Operating frequency of the motor, expressed as a percentage (0-100%).
    running (int): State of the motor; 0 for disabled, 1 for enabled.
    autoshutdown (bool): Determines if the motor will shut down automatically after inactivity.
    autoshutdowntime (int): Time duration (in seconds) before the motor shuts down automatically.
    rpm_hz (int): Ratio of revolutions per minute (RPM) to frequency (Hz).
    requested_rpm (float): The desired RPM of the motor.
    serial_access (bool): Indicates whether the class is actively communicating with the controller.
    rpm (RPMClass): Instance of the RPMClass used to measure and control motor speed.

<a id="motor_class.MotorClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="motor_class.MotorClass.set_speed"></a>

#### set\_speed

```python
def set_speed(required_rpm)
```

Sets the speed of the motor to the specified revolutions per minute (RPM).

This method adjusts the motor's speed based on the provided RPM value. It ensures
that the RPM is within acceptable limits, stopping the motor if the RPM is below
a minimum threshold and capping the RPM at a predefined maximum. The motor's
running state and direction are updated accordingly, and the speed control logic
is invoked.

<a id="motor_class.MotorClass.rpm_controller"></a>

#### rpm\_controller

```python
def rpm_controller()
```

Monitors and adjusts the drum motor's RPM to maintain the requested RPM value.

This method is executed periodically while the motor is running. It compares the
current RPM to the requested RPM and adjusts the motor frequency if necessary
to minimise the difference. Adjustments depend on the magnitude of the RPM
difference and update the motor control accordingly. If the RPM-hz ratio
stabilises, it recalculates the steady value for further adjustments.

<a id="motor_class.MotorClass.stop"></a>

#### stop

```python
def stop()
```

Stops the motor operation.

This method halts the motor by resetting its direction, frequency, requested
RPM, and running state to zero. It also communicates the stop command to the
motor controller, ensuring that the motor stops safely.

<a id="motor_class.MotorClass.controller_command"></a>

#### controller\_command

```python
def controller_command(message)
```

Executes a command by writing a message to the controller's registers.

This method ensures exclusive access to a serial connection while interacting
with the controller. It writes the provided message to the starting register
of the controller, then closes the serial connection, and resets the access flag.

<a id="motor_class.MotorClass.controller_query"></a>

#### controller\_query

```python
def controller_query()
```

Queries the motor controller to retrieve operational and configuration data. The method
communicates with the motor controller using RS485 communication, retrieves register
values for actual and setting data, and handles various error scenarios during communication.

Returns:
    dict: A dictionary containing the following keys:
        - running (bool): Indicates if the motor is running.
        - reqfrequency (float): Requested frequency divided by 100.
        - frequency (float or str): Actual frequency divided by 100, or an error message
          if communication fails.
        - voltage (int or str): Actual voltage value, or an error message if communication fails.
        - current (float or str): Actual current divided by 100, or an error message if communication fails.
        - rpm (int or str): Actual RPM value, or an error message if communication fails.
        - tombola_speed (str): Current tombola speed formatted to two decimal places.
        - requested_speed (float): The requested RPM value.

<a id="motor_class.MotorClass.print_controlword"></a>

#### print\_controlword

```python
def print_controlword()
```

Reads the control word from a specific register and logs the retrieved data.

This method interacts with the controller's register to read motor-related
control information. It ensures the serial connection is subsequently closed
after the operation and logs the retrieved control word.

<a id="motor_class.MotorClass.read_register"></a>

#### read\_register

```python
def read_register(reg)
```

Reads a specified register from the RS485 controller and returns the value.

This method communicates with an RS485 controller to retrieve the value from
a specified register. The function first attempts to read the register and logs
the result for debugging purposes. If the controller is unavailable or there is
a timeout issue, the function logs the corresponding error and returns an
appropriate response.

<a id="motor_class.MotorClass.write_register"></a>

#### write\_register

```python
def write_register(reg, controlword)
```

Writes a value to a specified register of the RS485 controller.

This method writes the provided control word to the given register of the RS485
controller. The serial connection is closed after the write operation. Logs
informational or error messages depending on the outcome of the operation.

<a id="motor_class.MotorClass.set_stop_time"></a>

#### set\_stop\_time

```python
def set_stop_time(autostop, stoptime)
```

Sets the stop time and autoshutdown configuration for the motor.

This method updates the settings for automated shutdown of the motor,
enabling or disabling the feature and defining the specific shutdown
time. The provided shutdown time is validated to ensure correct format
before applying the updates.

<a id="motor_class.MotorClass.get_stop_time"></a>

#### get\_stop\_time

```python
def get_stop_time()
```

Gets the stop time configuration.

This method retrieves the configuration details related to the stop time,
including whether auto-stop is enabled and the configured stop time.

<a id="motor_class.MotorClass.auto_stop_timer"></a>

#### auto\_stop\_timer

```python
def auto_stop_timer()
```

Monitors and automatically stops the motor when the specified auto shutdown time is reached.

Summary:
This method continuously checks whether the auto shutdown feature is enabled and the motor is running. If the
current time exceeds the configured auto shutdown time, it triggers the motor's stop functionality.

<a id="motor_class.MotorClass.parse_control_message"></a>

#### parse\_control\_message

```python
def parse_control_message(message)
```

Processes the control messages for motor operations by interpreting the keys in the provided message
dictionary and performing corresponding actions, such as stopping the motor, setting the RPM, resetting
the controller, accessing registers, or updating stop time. Returns responses for specific queries.

<a id="motor_class.set_status_message"></a>

#### set\_status\_message

```python
def set_status_message(message)
```

Updates the status message with a timestamp and saves it.

This function updates the status message in the application settings by
appending the current date and time to the provided message. After updating
the status, it writes the changes to the settings file.

<a id="motor_class.running"></a>

#### running

```python
def running(value)
```

Determines the operational state based on the given value.

The function evaluates the integer input and returns a string
indicating whether the system is "Running" or "Stopped".

<a id="motor_class.time_format_check"></a>

#### time\_format\_check

```python
def time_format_check(value)
```

Checks if a given string adheres to the 'HH:MM:SS' time format.

This function validates whether the input string follows the proper 24-hour
time format 'HH:MM:SS'. It uses the `datetime.strptime` function for this
purpose. If the format is correct, the function returns True. Otherwise, it
returns False.

