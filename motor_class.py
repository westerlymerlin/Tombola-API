"""
Motor Control Module for V20 Controller

This module provides a comprehensive interface for controlling an electric motor via a V20 controller
using Modbus RTU protocol over RS485. It handles motor speed control, direction, auto-shutdown,
and monitoring of motor parameters including RPM, voltage, and current.
Provides a motor control interface utilising Modbus communication.
"""

from time import sleep
from threading import Timer
from datetime import datetime
import minimalmodbus
import serial.serialutil
from app_control import settings, writesettings
from rpm_class import RPMClass
from logmanager import logger


class MotorClass:
    """
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
    """
    def __init__(self):
        self.command_start_register = settings['control_start_register']
        self.stw_control_register = settings['STW_register']
        self.query_start_register = settings['reading_start_register']
        self.read_length = settings['read_length']
        self.direction = 0  # 0 = forward, 1 = reverse
        self.frequency = 0  # 0 - 100%
        self.running = 0  # O = disabled 1 = enabled
        self.autoshutdown = settings['autoshutdown']
        self.autoshutdowntime = settings['shutdowntime']
        self.rpm_hz = settings['rpm_frequency']
        self.requested_rpm = 0
        self.serial_access = False
        self.rpm = RPMClass()
        timerthread = Timer(1, self.auto_stop_timer)
        timerthread.name = 'Auto Stop Thread'
        timerthread.start()
        try:
            self.controller = minimalmodbus.Instrument(settings['port'], settings['station'],
                                                       minimalmodbus.MODE_RTU)
            self.controller.serial.parity = minimalmodbus.serial.PARITY_EVEN
            self.controller.serial.baudrate = settings['baud']
            self.controller.serial.bytesize = settings['bytesize']
            self.controller.serial.stopbits = settings['stopbits']
            self.controller.serial.timeout = settings['serialtimeout']
            self.controller.clear_buffers_before_each_transaction = \
                settings['clear_buffers_before_call']
            self.controller.close_port_after_each_call = settings['clear_buffers_after_call']
            logger.debug('MotorClass: RS485 controller setup with modbus')
            # logger.debug('MotorClass: Resetting v20')
            # self.write_register(self.stw_control_register, settings['STW_forward'])
            # logger.debug('MotorClass: setting speed to 0')
            # self.stop()
        except serial.serialutil.SerialException:
            logger.error('MotorClass: init Error - no controller connected, '
                         'please check RS485 port address is correct')

    def set_speed(self, required_rpm):
        """
        Sets the speed of the motor to the specified revolutions per minute (RPM).

        This method adjusts the motor's speed based on the provided RPM value. It ensures
        that the RPM is within acceptable limits, stopping the motor if the RPM is below
        a minimum threshold and capping the RPM at a predefined maximum. The motor's
        running state and direction are updated accordingly, and the speed control logic
        is invoked.
        """
        try:
            required_rpm = int(float(required_rpm) * 10)/10
        except ValueError:
            return
        if required_rpm < 0.1:
            self.stop()
            return
        required_rpm = min(required_rpm, settings['rpm_max'])
        self.running = 1
        self.direction = 0
        self.requested_rpm = required_rpm
        self.rpm_controller()
        logger.debug('MotorClass: Set speed: %s', required_rpm)

    def rpm_controller(self):
        """
        Monitors and adjusts the drum motor's RPM to maintain the requested RPM value.

        This method is executed periodically while the motor is running. It compares the
        current RPM to the requested RPM and adjusts the motor frequency if necessary
        to minimise the difference. Adjustments depend on the magnitude of the RPM
        difference and update the motor control accordingly. If the RPM-hz ratio
        stabilises, it recalculates the steady value for further adjustments.
        """
        rpm = self.rpm.get_rpm()
        speedchanged = 1
        if self.running:  # run this check in 10s if the drum is running
            rpmthread = Timer(10, self.rpm_controller)
            rpmthread.name = 'RPM Reader Thread'
            rpmthread.start()
        else:
            return
        speed_diff = rpm - self.requested_rpm  # Difference between actual and requested rpm
        if abs(speed_diff) > 5:
            logger.debug('MotorClass: RPM diff > 5 so resetting')
            self.frequency = int(10 * self.requested_rpm * self.rpm_hz)
        elif speed_diff > 0.1:
            logger.debug('MotorClass: RPM slightly to high, reducing it a bit')
            self.frequency = int(self.frequency - self.rpm_hz)
        elif speed_diff < -0.1:
            logger.debug('MotorClass: RPM slightly to low, increasing it a bit')
            self.frequency = int(self.frequency + self.rpm_hz)
        else:
            speedchanged = 0
            rpm_hz = (self.frequency / self.rpm.get_rpm()) / 10  # calculate the steady rpm-hz ratio
            if abs(rpm_hz - self.rpm_hz) > 5:
                logger.info('MotorClass: rpm_hz value should be = %s', rpm_hz)
        if speedchanged:
            try:
                logger.debug('Motorclass: RPM Controller: Current RPM %.2f Desired %.2f setting to frequency %s',
                            rpm, self.requested_rpm, self.frequency)
                self.controller_command([self.frequency, self.running, self.direction, 1])
            except AttributeError:
                logger.error('MotorClass: rpm_controller function error No RS483 Controller')
                self.serial_access = False
            except minimalmodbus.NoResponseError:
                logger.error('MotorClass: rpm_controller function error RS485 timeout')
                self.serial_access = False


    def stop(self):
        """
        Stops the motor operation.

        This method halts the motor by resetting its direction, frequency, requested
        RPM, and running state to zero. It also communicates the stop command to the
        motor controller, ensuring that the motor stops safely. The method handles
        potential errors during communication with the controller and updates the
        `serialaccess` attribute to indicate the status of the communication link.
        """
        self.direction = 0
        self.frequency = 0
        self.requested_rpm = 0
        self.running = 0
        try:
            logger.info('MotorClass: STOP requested')
            self.controller_command([self.frequency, self.running, self.direction, 0])
            self.serial_access = False
        except AttributeError:
            self.serial_access = False
            logger.error('MotorClass: Stop function error No RS483 Controller')
            self.serial_access = False
        except minimalmodbus.NoResponseError:
            self.serial_access = False
            logger.error('MotorClass: Stop function error RS485 timeout')


    def controller_command(self, message):
        """
        Executes a command by writing a message to the controller's registers.

        This method ensures exclusive access to a serial connection while interacting
        with the controller. It writes the provided message to the starting register
        of the controller, then closes the serial connection, and resets the access flag.

        """
        while self.serial_access:
            pass
        self.controller.write_registers(self.command_start_register, message)
        self.controller.serial.close()
        self.serial_access = False

    def controller_query(self):
        """
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
        """
        while self.serial_access:
            pass
        self.serial_access = True
        try:
            actual_data = self.controller.read_registers(self.query_start_register,
                                                         self.read_length, 3)
            setting_data = self.controller.read_registers(self.command_start_register, 4, 3)
            self.controller.serial.close()
            self.serial_access = False
            return {'running': running(self.running), 'reqfrequency': setting_data[0] / 100,
                    'frequency': actual_data[0] / 100, 'voltage': actual_data[9], 'current':
                        actual_data[2] / 100,
                    'rpm': actual_data[1], 'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except AttributeError:   # RS485 not plugged in
            self.controller.serial.close()
            self.serial_access = False
            logger.error('MotorClass: Controller Query Error: RS485 controller is not '
                         'working or not plugged in')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': 'No RS485 Controller', 'voltage': 'No RS485 Controller',
                    'current': 'No RS485 Controller', 'rpm': 'No RS485 Controller',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except minimalmodbus.NoResponseError:
            self.controller.serial.close()
            self.serial_access = False
            logger.error('MotorClass: Controller Query Error: No response from the V20 controller, '
                         'check it is powered on and connected')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': 'RS485 Timeout', 'voltage': 'RS485 Timeout',
                    'current': 'RS485 Timeout', 'rpm': 'RS485 Timeout',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except serial.serialutil.SerialException:
            self.controller.serial.close()
            self.serial_access = False
            logger.error('MotorClass: Controller Query Error: unhandled exception', exc_info=BaseException)
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': '-', 'voltage': '-', 'current': '-', 'rpm': '-',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}

    def print_controlword(self):
        """
        Reads the control word from a specific register and logs the retrieved data.

        This method interacts with the controller's register to read motor-related
        control information. It ensures the serial connection is subsequently closed
        after the operation and logs the retrieved control word.
        """
        data = self.controller.read_register(99, 0, 3)
        self.controller.serial.close()
        logger.info('Motorclass: read control word: %s', data)

    def read_register(self, reg):
        """
        Reads a specified register from the RS485 controller and returns the value.

        This method communicates with an RS485 controller to retrieve the value from
        a specified register. The function first attempts to read the register and logs
        the result for debugging purposes. If the controller is unavailable or there is
        a timeout issue, the function logs the corresponding error and returns an
        appropriate response.
        """
        try:
            data = self.controller.read_register(reg, 0, 3)
            self.controller.serial.close()
            logger.debug('MotorClass: read registry: Registry %s. Word %s', reg, data)
            return {'register': reg, 'word': data}
        except AttributeError:
            logger.error('MotorClass: read_register function error No RS483 Controller')
            return {'register': reg, 'word': 'No RS485 Controller'}
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: read_register function error RS485 timeout')
            return {'register': reg, 'word': 'RS485 Timeout'}

    def write_register(self, reg, controlword):
        """
        Writes a value to a specified register of the RS485 controller.

        This method writes the provided control word to the given register of the RS485
        controller. The serial connection is closed after the write operation. Logs
        informational or error messages depending on the outcome of the operation.
        """
        try:
            self.controller.write_register(reg, controlword)
            self.controller.serial.close()
            logger.info('MotorClass: write registry: Registry %s. Word %s', reg, controlword)
        except AttributeError:
            logger.error('MotorClass: write_register function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: write_register function error RS485 timeout')

    def set_stop_time(self, autostop, stoptime):
        """
        Sets the stop time and autoshutdown configuration for the motor.

        This method updates the settings for automated shutdown of the motor,
        enabling or disabling the feature and defining the specific shutdown
        time. The provided shutdown time is validated to ensure correct format
        before applying the updates.
        """
        if time_format_check(stoptime):
            self.autoshutdown = autostop
            settings['autoshutdown'] = autostop
            self.autoshutdowntime = stoptime
            settings['shutdowntime'] = stoptime
            logger.info('MotorClass: Write settings.json')
            writesettings()

    def get_stop_time(self):
        """
        Gets the stop time configuration.

        This method retrieves the configuration details related to the stop time,
        including whether auto-stop is enabled and the configured stop time.
        """
        return {'autostop': self.autoshutdown, 'stoptime': self.autoshutdowntime}

    def auto_stop_timer(self):
        """
        Monitors and automatically stops the motor when the specified auto shutdown time is reached.

        Summary:
        This method continuously checks whether the auto shutdown feature is enabled and the motor is running. If the
        current time exceeds the configured auto shutdown time, it triggers the motor's stop functionality.
        """
        while True:
            if self.autoshutdown and self.running:
                stoptime = datetime.strptime(datetime.now().strftime('%d/%m/%Y ') +
                                             self.autoshutdowntime, '%d/%m/%Y %H:%M:%S')
                # print(stoptime)
                if stoptime < datetime.now():
                    logger.info('MotorClass: Auto stop time reached - stopping')
                    self.stop()
            sleep(1)

    def parse_control_message(self, message):
        """
        Processes the control messages for motor operations by interpreting the keys in the provided message
        dictionary and performing corresponding actions, such as stopping the motor, setting the RPM, resetting
        the controller, accessing registers, or updating stop time. Returns responses for specific queries.
        """
        if 'stop' in message.keys():
            logger.info('MotorClass: Stop request received from web application')
            self.stop()
        elif 'websetrpm' in message.keys():
            logger.info('MotorClass: RPM set by web application')
            self.set_speed(message['websetrpm'])
        elif 'setrpm' in message.keys():
            logger.info('MotorClass: RPM set by API')
            self.set_speed(message['setrpm'])
        elif 'reset' in message.keys():
            logger.info('MotorClass: Controller reset requested by web application')
            self.write_register(self.stw_control_register, settings['STW_forward'])
        elif 'write_register' in message.keys():
            logger.debug('MotorClass: Write Register received via API')
            self.write_register(message['write_register'], message['word'])
        elif 'read_register' in message.keys():
            logger.debug('MotorClass: Read Register received via API')
            return self.read_register(message['read_register'])
        elif 'rpm_data' in message.keys():
            logger.debug('MotorClass: RPM timing data request via API')
            return self.rpm.get_rpm_data()
        elif 'rpm' in message.keys():
            logger.debug('MotorClass: RPM speed request via API')
            return {'rpm': self.rpm.get_rpm()}
        elif 'stoptime' in message.keys():
            if 'autostop' in message.keys():
                self.set_stop_time(True, message['stoptime'])
            else:
                self.set_stop_time(False, message['stoptime'])
            logger.debug('Stop time updated via web application')
        else:
            logger.info('MotorClass: API message received but not processed  = %s', message)
        return self.controller_query()


def running(value):
    """
    Determines the operational state based on the given value.

    The function evaluates the integer input and returns a string
    indicating whether the system is "Running" or "Stopped".
    """
    if value == 1:
        return 'Running'
    return 'Stopped'


def time_format_check(value):
    """
    Checks if a given string adheres to the 'HH:MM:SS' time format.

    This function validates whether the input string follows the proper 24-hour
    time format 'HH:MM:SS'. It uses the `datetime.strptime` function for this
    purpose. If the format is correct, the function returns True. Otherwise, it
    returns False.
    """
    try:
        datetime.strptime(value, '%H:%M:%S')
        return True
    except ValueError:
        return False


if __name__ == '__main__':  # used for standlone testing
    tom = MotorClass()
