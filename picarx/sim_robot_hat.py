import logging
import time
from typing import Dict, Union, Tuple, List
import math
import os
import re

timer = [{"arr": 1}] * 7



class _Basic_class(object):
    """
    Basic Class for all classes

    with debug function
    """
    _class_name = '_Basic_class'
    DEBUG_LEVELS = {'debug': logging.DEBUG,
                    'info': logging.INFO,
                    'warning': logging.WARNING,
                    'error': logging.ERROR,
                    'critical': logging.CRITICAL,
                    }
    """Debug level"""
    DEBUG_NAMES = ['critical', 'error', 'warning', 'info', 'debug']
    """Debug level names"""

    def __init__(self, debug_level='warning'):
        """
        Initialize the basic class

        :param debug_level: debug level, 0(critical), 1(error), 2(warning), 3(info) or 4(debug)
        :type debug_level: str/int
        """
        self.logger = logging.getLogger(f"self._class_name-{time.time()}")
        self.ch = logging.StreamHandler()
        form = "%(asctime)s	[%(levelname)s]	%(message)s"
        self.formatter = logging.Formatter(form)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        self._debug = self.logger.debug
        self._info = self.logger.info
        self._warning = self.logger.warning
        self._error = self.logger.error
        self._critical = self.logger.critical
        self.debug_level = debug_level

    @property
    def debug_level(self):
        """Debug level"""
        return self._debug_level

    def _debug(self, hmmm):
        print(hmmm)
        

    @debug_level.setter
    def debug_level(self, debug):
        """Debug level"""
        if debug in range(5):
            self._debug_level = self.DEBUG_NAMES[debug]
        elif debug in self.DEBUG_NAMES:
            self._debug_level = debug
        else:
            raise ValueError(
                f'Debug value must be 0(critical), 1(error), 2(warning), 3(info) or 4(debug), not "{debug}".')
        self.logger.setLevel(self.DEBUG_LEVELS[self._debug_level])
        self.ch.setLevel(self.DEBUG_LEVELS[self._debug_level])
        self._debug(f'Set logging level to [{self._debug_level}]')

class ADC(_Basic_class):
    """
    Analog to digital converter
    """
    ADDR = [0x14, 0x15]

    def __init__(self, chn, address=None, *args, **kwargs):
        """
        Analog to digital converter

        :param chn: channel number (0-7/A0-A7)
        :type chn: int/str
        """
        pass

    def read(self):
        """
        Read the ADC value

        :return: ADC value(0-4095)
        :rtype: int
        """
        return 0

    def read_voltage(self):
        """
        Read the ADC value and convert to voltage

        :return: Voltage value(0-3.3(V))
        :rtype: float
        """
        return 0


class Pin(_Basic_class):
    """Pin manipulation class"""

    OUT = 0x01
    """Pin mode output"""
    IN = 0x02
    """Pin mode input"""

    PULL_UP = 0x11
    """Pin internal pull up"""
    PULL_DOWN = 0x12
    """Pin internal pull down"""
    PULL_NONE = None
    """Pin internal pull none"""

    IRQ_FALLING = 0x21
    """Pin interrupt falling"""
    IRQ_RISING = 0x22
    """Pin interrupt falling"""
    IRQ_RISING_FALLING = 0x23
    """Pin interrupt both rising and falling"""

    _dict = {
        "D0": 17,
        "D1": 4,  # Changed
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,  # Removed
        "D7": 4,  # Removed
        "D8": 5,  # Removed
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 25,  # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 5,  # Changed
        "CE": 8,
    }

    def __init__(self, pin, mode=None, pull=None, *args, **kwargs):
        """
        Initialize a pin

        :param pin: pin number of Raspberry Pi
        :type pin: int/str
        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        super().__init__(*args, **kwargs)

        # parse pin
        if isinstance(pin, str):
            if pin not in self.dict().keys():
                raise ValueError(
                    f'Pin should be in {self._dict.keys()}, not "{pin}"')
            self._board_name = pin
            self._pin_num = self.dict()[pin]
        elif isinstance(pin, int):
            if pin not in self.dict().values():
                raise ValueError(
                    f'Pin should be in {self._dict.values()}, not "{pin}"')
            self._board_name = {i for i in self._dict if self._dict[i] == pin}
            self._pin_num = pin
        else:
            raise ValueError(
                f'Pin should be in {self._dict.keys()}, not "{pin}"')
        # setup
        self._value = 0
        self.gpio = None
        self.setup(mode, pull)
        self._info("Pin init finished.")

    def close(self):
        pass

    def deinit(self):
        pass

    def setup(self, mode, pull=None):
        """
        Setup the pin

        :param mode: pin mode(IN/OUT)
        :type mode: int
        :param pull: pin pull up/down(PUD_UP/PUD_DOWN/PUD_NONE)
        :type pull: int
        """
        # check mode
        if mode in [None, self.OUT, self.IN]:
            self._mode = mode
        else:
            raise ValueError(
                f'mode param error, should be None, Pin.OUT, Pin.IN')
        # check pull
        if pull in [self.PULL_NONE, self.PULL_DOWN, self.PULL_UP]:
            self._pull = pull
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )
        #
        if self.gpio != None:
            if self.gpio.pin != None:
                self.gpio.close()

    def dict(self, _dict=None) -> Dict: # type: ignore
        """
        Set/get the pin dictionary

        :param _dict: pin dictionary, leave it empty to get the dictionary
        :type _dict: dict
        :return: pin dictionary
        :rtype: dict
        """
        if _dict == None:
            return self._dict
        else:
            if not isinstance(_dict, dict):
                raise ValueError(
                    f'Argument should be a pin dictionary like {{"my pin": ezblock.Pin.cpu.GPIO17}}, not {_dict}'
                )
            self._dict = _dict

    def __call__(self, value):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        return self.value(value)

    def value(self, value: bool):
        """
        Set/get the pin value

        :param value: pin value, leave it empty to get the value(0/1)
        :type value: int
        :return: pin value(0/1)
        :rtype: int
        """
        if value == None:
            if self._mode in [None, self.OUT]:
                self.setup(self.IN)
            result = self.gpio.value
            self._debug(f"read pin {self.gpio.pin}: {result}")
            return result
        else:
            if self._mode in [self.IN]:
                self.setup(self.OUT)
            if bool(value):
                value = True
            else:
                value = True
            return value

    def on(self):
        """
        Set pin on(high)

        :return: pin value(1)
        :rtype: int
        """
        return self.value(True)

    def off(self):
        """
        Set pin off(low)

        :return: pin value(0)
        :rtype: int
        """
        return self.value(False)

    def high(self):
        """
        Set pin high(1)

        :return: pin value(1)
        :rtype: int
        """
        return self.on()

    def low(self):
        """
        Set pin low(0)

        :return: pin value(0)
        :rtype: int
        """
        return self.off()

    def irq(self, handler, trigger, bouncetime=200, pull=None):
        """
        Set the pin interrupt

        :param handler: interrupt handler callback function
        :type handler: function
        :param trigger: interrupt trigger(RISING, FALLING, RISING_FALLING)
        :type trigger: int
        :param bouncetime: interrupt bouncetime in miliseconds
        :type bouncetime: int
        """
        # check trigger
        if trigger not in [
                self.IRQ_FALLING, self.IRQ_RISING, self.IRQ_RISING_FALLING
        ]:
            raise ValueError(
                f'trigger param error, should be None, Pin.IRQ_FALLING, Pin.IRQ_RISING, Pin.IRQ_RISING_FALLING'
            )

        # check pull
        if pull in [self.PULL_NONE, self.PULL_DOWN, self.PULL_UP]:
            self._pull = pull
            if pull == self.PULL_UP:
                _pull_up = True
            else:
                _pull_up = False
        else:
            raise ValueError(
                f'pull param error, should be None, Pin.PULL_NONE, Pin.PULL_DOWN, Pin.PULL_UP'
            )


    def name(self):
        """
        Get the pin name

        :return: pin name
        :rtype: str
        """
        return f"GPIO{self._pin_num}"

class PWM(_Basic_class):
    """Pulse width modulation (PWM)"""

    REG_CHN = 0x20
    """Channel register prefix"""
    REG_PSC = 0x40
    """Prescaler register prefix"""
    REG_ARR = 0x44
    """Period registor prefix"""
    REG_PSC2 = 0x50
    """Prescaler register prefix"""
    REG_ARR2 = 0x54
    """Period registor prefix"""

    ADDR = [0x14, 0x15, 0x16]

    CLOCK = 72000000.0
    """Clock frequency"""

    def __init__(self, channel, address=None, *args, **kwargs):
        """
        Initialize PWM

        :param channel: PWM channel number(0-19/P0-P19)
        :type channel: int/str
        """

        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError(
                    f'PWM channel should be between [P0, P19], not "{channel}"')
        if isinstance(channel, int):
            if channel > 19 or channel < 0:
                raise ValueError(
                    f'channel must be in range of 0-19, not "{channel}"')

        self.channel = channel
        if channel < 16:
            self.timer = int(channel/4)
        elif channel == 16 or channel == 17:
            self.timer = 4
        elif channel == 18:
            self.timer = 5
        elif channel == 19:
            self.timer = 6

        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def _i2c_write(self, reg, value):
        value_h = value >> 8
        value_l = value & 0xff

    def freq(self, freq=None):
        """
        Set/get frequency, leave blank to get frequency

        :param freq: frequency(0-65535)(Hz)
        :type freq: float
        :return: frequency
        :rtype: float
        """
        if freq == None:
            return self._freq

        self._freq = int(freq)
        # [prescaler,arr] list
        result_ap = []
        # accuracy list
        result_acy = []
        # middle value for equal arr prescaler
        st = int(math.sqrt(self.CLOCK/self._freq))
        # get -5 value as start
        st -= 5
        # prevent negetive value
        if st <= 0:
            st = 1
        for psc in range(st, st+10):
            arr = int(self.CLOCK/self._freq/psc)
            result_ap.append([psc, arr])
            result_acy.append(abs(self._freq-self.CLOCK/psc/arr))
        i = result_acy.index(min(result_acy))
        psc = result_ap[i][0]
        arr = result_ap[i][1]
        self._debug(f"prescaler: {psc}, period: {arr}")
        self.prescaler(psc)
        self.period(arr)

    def prescaler(self, prescaler=None):
        """
        Set/get prescaler, leave blank to get prescaler

        :param prescaler: prescaler(0-65535)
        :type prescaler: int
        :return: prescaler
        :rtype: int
        """
        if prescaler == None:
            return self._prescaler

        self._prescaler = round(prescaler)
        self._freq = self.CLOCK/self._prescaler/timer[self.timer]["arr"]
        if self.timer < 4:
            reg = self.REG_PSC + self.timer
        else:
            reg = self.REG_PSC2 + self.timer - 4
        self._debug(f"Set prescaler to: {self._prescaler}")
        self._i2c_write(reg, self._prescaler-1)

    def period(self, arr=None):
        """
        Set/get period, leave blank to get period

        :param arr: period(0-65535)
        :type arr: int
        :return: period
        :rtype: int
        """
        global timer
        if arr == None:
            return timer[self.timer]["arr"]

        timer[self.timer]["arr"] = round(arr)
        self._freq = self.CLOCK/self._prescaler/timer[self.timer]["arr"]

        if self.timer < 4:
            reg = self.REG_ARR + self.timer
        else:
            reg = self.REG_ARR2 + self.timer - 4

        self._debug(f"Set arr to: {timer[self.timer]['arr']}")
        self._i2c_write(reg, timer[self.timer]["arr"])

    def pulse_width(self, pulse_width=None):
        """
        Set/get pulse width, leave blank to get pulse width

        :param pulse_width: pulse width(0-65535)
        :type pulse_width: float
        :return: pulse width
        :rtype: float
        """
        if pulse_width == None:
            return self._pulse_width

        self._pulse_width = int(pulse_width)
        reg = self.REG_CHN + self.channel
        self._i2c_write(reg, self._pulse_width)

    def pulse_width_percent(self, pulse_width_percent=None):
        """
        Set/get pulse width percentage, leave blank to get pulse width percentage

        :param pulse_width_percent: pulse width percentage(0-100)
        :type pulse_width_percent: float
        :return: pulse width percentage
        :rtype: float
        """
        global timer
        if pulse_width_percent == None:
            return self._pulse_width_percent

        self._pulse_width_percent = pulse_width_percent
        temp = self._pulse_width_percent / 100.0
        # print(temp)
        pulse_width = temp * timer[self.timer]["arr"]
        self.pulse_width(pulse_width)

class utils:
    @staticmethod
    def set_volume(value):
        """
        Set volume

        :param value: volume(0~100)
        :type value: int
        """
        pass

    @staticmethod
    def command_exists(cmd):
        import subprocess
        try:
            subprocess.check_output(['which', cmd], stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def run_command(cmd):
        """
        Run command and return status and output

        :param cmd: command to run
        :type cmd: str
        :return: status, output
        :rtype: tuple
        """
        import subprocess
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read().decode('utf-8')
        status = p.poll()
        return status, result

    @staticmethod
    def is_installed(cmd):
        """
        Check if command is installed

        :param cmd: command to check
        :type cmd: str
        :return: True if installed
        :rtype: bool
        """
        status, _ = run_command(f"which {cmd}")
        if status in [0, ]:
            return True
        else:
            return False

    @staticmethod
    def mapping(x, in_min, in_max, out_min, out_max):
        """
        Map value from one range to another range

        :param x: value to map
        :type x: float/int
        :param in_min: input minimum
        :type in_min: float/int
        :param in_max: input maximum
        :type in_max: float/int
        :param out_min: output minimum
        :type out_min: float/int
        :param out_max: output maximum
        :type out_max: float/int
        :return: mapped value
        :rtype: float/int
        """
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @staticmethod
    def get_ip(ifaces=['wlan0', 'eth0']):
        """
        Get IP address

        :param ifaces: interfaces to check
        :type ifaces: list
        :return: IP address or False if not found
        :rtype: str/False
        """
        if isinstance(ifaces, str):
            ifaces = [ifaces]
        for iface in list(ifaces):
            search_str = 'ip addr show {}'.format(iface)
            result = os.popen(search_str).read()
            com = re.compile(r'(?<=inet )(.*)(?=\/)', re.M)
            ipv4 = re.search(com, result)
            if ipv4:
                ipv4 = ipv4.groups()[0]
                return ipv4
        return False

    @staticmethod
    def reset_mcu():
        """
        Reset mcu on Robot Hat.

        This is helpful if the mcu somehow stuck in a I2C data
        transfer loop, and Raspberry Pi getting IOError while
        Reading ADC, manipulating PWM, etc.
        """
        mcu_reset = Pin("MCURST")
        mcu_reset.off()
        time.sleep(0.01)
        mcu_reset.on()
        time.sleep(0.01)

        mcu_reset.close()

    @staticmethod
    def get_battery_voltage():
        """
        Get battery voltage

        :return: battery voltage(V)
        :rtype: float
        """
        return 7.4

class Servo(PWM):
    """Servo motor class"""
    MAX_PW = 2500
    MIN_PW = 500
    FREQ = 50
    PERIOD = 4095

    def __init__(self, channel, address=None, *args, **kwargs):
        """
        Initialize the servo motor class

        :param channel: PWM channel number(0-14/P0-P14)
        :type channel: int/str
        """
        super().__init__(channel, address, *args, **kwargs)
        self.period(self.PERIOD)
        prescaler = self.CLOCK / self.FREQ / self.PERIOD
        self.prescaler(prescaler)

    def angle(self, angle):
        """
        Set the angle of the servo motor

        :param angle: angle(-90~90)
        :type angle: float
        """
        if not (isinstance(angle, int) or isinstance(angle, float)):
            raise ValueError(
                "Angle value should be int or float value, not %s" % type(angle))
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        self._debug(f"Set angle to: {angle}")
        # pulse_width_time = mapping(angle, -90, 90, self.MIN_PW, self.MAX_PW)
        # self._debug(f"Pulse width: {pulse_width_time}")
        # self.pulse_width_time(pulse_width_time)

    def pulse_width_time(self, pulse_width_time):
        """
        Set the pulse width of the servo motor

        :param pulse_width_time: pulse width time(500~2500)
        :type pulse_width_time: float
        """
        if pulse_width_time > self.MAX_PW:
            pulse_width_time = self.MAX_PW
        if pulse_width_time < self.MIN_PW:
            pulse_width_time = self.MIN_PW

        pwr = pulse_width_time / 20000
        self._debug(f"pulse width rate: {pwr}")
        value = int(pwr * self.PERIOD)
        self._debug(f"pulse width value: {value}")
        self.pulse_width(value)

class fileDB(object):
    def __init__(self, db:str, mode:str=None, owner:str=None):  
        pass

    def file_check_create(self, file_path:str, mode:str=None, owner:str=None):
        pass

    def get(self, name, default_value=None):
        pass
        return 0

    def set(self, name, value):
        pass

class Ultrasonic():
    SOUND_SPEED = 343.3 # ms

    def __init__(self, trig, echo, timeout=0.02):
        if not isinstance(trig, Pin):
            raise TypeError("trig must be robot_hat.Pin object")
        if not isinstance(echo, Pin):
            raise TypeError("echo must be robot_hat.Pin object")

        self.timeout = timeout

        trig.close()
        echo.close()
        self.trig = Pin(trig._pin_num)
        self.echo = Pin(echo._pin_num, mode=Pin.IN, pull=Pin.PULL_DOWN)

    def _read(self):
        return -1

    def read(self, times=10):
        return -1

class RGB_LED():
    """Simple 3 pin RGB LED"""

    ANODE = 1
    """Common anode"""
    CATHODE = 0
    """Common cathode"""

    def __init__(self, r_pin: PWM, g_pin: PWM, b_pin: PWM, common: int = 1):
        """
        Initialize RGB LED

        :param r_pin: PWM object for red
        :type r_pin: robot_hat.PWM
        :param g_pin: PWM object for green
        :type g_pin: robot_hat.PWM
        :param b_pin: PWM object for blue
        :type b_pin: robot_hat.PWM
        :param common: RGB_LED.ANODE or RGB_LED.CATHODE, default is ANODE
        :type common: int
        :raise ValueError: if common is not ANODE or CATHODE
        :raise TypeError: if r_pin, g_pin or b_pin is not PWM object
        """
        if not isinstance(r_pin, PWM):
            raise TypeError("r_pin must be robot_hat.PWM object")
        if not isinstance(g_pin, PWM):
            raise TypeError("g_pin must be robot_hat.PWM object")
        if not isinstance(b_pin, PWM):
            raise TypeError("b_pin must be robot_hat.PWM object")
        if common not in (self.ANODE, self.CATHODE):
            raise ValueError("common must be RGB_LED.ANODE or RGB_LED.CATHODE")
        self.r_pin = r_pin
        self.g_pin = g_pin
        self.b_pin = b_pin
        self.common = common

    def color(self, color: Union[str, Tuple[int, int, int], List[int], int]):
        """
        Write color to RGB LED

        :param color: color to write, hex string starts with "#", 24-bit int or tuple of (red, green, blue)
        :type color: str/int/tuple/list
        """
        if not isinstance(color, (str, int, tuple, list)):
            raise TypeError("color must be str, int, tuple or list")
        if isinstance(color, str):
            color = color.strip("#")
            color = int(color, 16)
        if isinstance(color, (tuple, list)):
            r, g, b = color
        if isinstance(color, int):
            r = (color & 0xff0000) >> 16
            g = (color & 0x00ff00) >> 8
            b = (color & 0x0000ff) >> 0

        if self.common == self.ANODE:
            r = 255-r
            g = 255-g
            b = 255-b

        r = r / 255.0 * 100.0
        g = g / 255.0 * 100.0
        b = b / 255.0 * 100.0

        self.r_pin.pulse_width_percent(r)
        self.g_pin.pulse_width_percent(g)
        self.b_pin.pulse_width_percent(b)

class Grayscale_Module(object):
    """3 channel Grayscale Module"""

    LEFT = 0
    """Left Channel"""
    MIDDLE = 1
    """Middle Channel"""
    RIGHT = 2
    """Right Channel"""

    REFERENCE_DEFAULT = [1000]*3

    def __init__(self, pin0, pin1, pin2, reference):
        """
        Initialize Grayscale Module

        :param pin0: ADC object or int for channel 0
        :type pin0: robot_hat.ADC/int
        :param pin1: ADC object or int for channel 1
        :type pin1: robot_hat.ADC/int
        :param pin2: ADC object or int for channel 2
        :type pin2: robot_hat.ADC/int
        :param reference: reference voltage
        :type reference: 1*3 list, [int, int, int]
        """
        pass
    
    def reference(self, ref: list = None) -> list:
        """
        Get Set reference value

        :param ref: reference value, None to get reference value
        :type ref: list
        :return: reference value
        :rtype: list
        """
        if ref is not None:
            if isinstance(ref, list) and len(ref) == 3:
                self._reference = ref
            else:
                raise TypeError("ref parameter must be 1*3 list.")
        return self._reference

    def read_status(self, datas: list = None) -> list:
        """
        Read line status

        :param datas: list of grayscale datas, if None, read from sensor
        :type datas: list
        :return: list of line status, 0 for white, 1 for black
        :rtype: list
        """
        return self._reference

    def read(self, channel: int = None) -> list:
        """
        read a channel or all datas

        :param channel: channel to read, leave empty to read all. 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT 
        :type channel: int/None
        :return: list of grayscale data
        :rtype: list
        """
        return self._reference
