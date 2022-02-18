from machine import Pin, ADC, I2C
import utime
from libs import mma7660


xAxis: ADC
yAxis: ADC

buttonB: Pin
buttonA: Pin
buttonStart: Pin
buttonSelect: Pin


def x_value():
    return xAxis.read_u16()


def y_value():
    return yAxis.read_u16()


def button_a():
    return buttonA.value()


def button_b():
    return buttonB.value()


def button_start():
    return buttonStart.value()


def button_select():
    return buttonSelect.value()


class DelayEvent:
    def __init__(self, time_threshold, callback_handle):
        self.start_time = utime.ticks_ms()
        self.time_threshold = time_threshold
        self.callback_handle = callback_handle

    def tick(self):
        if utime.ticks_diff(utime.ticks_ms(), self.start_time) > self.time_threshold:
            self.callback_handle()
            self.start_time = utime.ticks_ms()


class JoystickEvent:
    def __init__(self, stick_pos_handle, great_than: bool, pos_threshold: int,
                 timer_threshold: int, callback_handle):
        self.counter = 0
        self.stick_pos_handle = stick_pos_handle
        self.stick_pos = self.stick_pos_handle()
        self.pos_threshold = pos_threshold
        self.great_than = great_than
        self.delay_event = DelayEvent(timer_threshold, callback_handle)

    def event(self):
        self.stick_pos = self.stick_pos_handle()
        trigger = False
        if self.great_than:
            if self.stick_pos > self.pos_threshold:
                trigger = True
        else:
            if self.stick_pos < self.pos_threshold:
                trigger = True
        if trigger:
            self.delay_event.tick()


class Joystick:
    def __init__(self, *args):
        self.controls = []
        for arg in args:
            self.controls.append(JoystickEvent(*arg))

    def run(self):
        for control in self.controls:
            control.event()


class ButtonEvent:
    def __init__(self, pin: Pin, trigger_event, time_threshold, callback_handle):
        self.irq = pin.irq(self.event, trigger_event)
        self.callback_handle = callback_handle
        self.delay_event = DelayEvent(time_threshold, callback_handle)

    def event(self, pin):
        self.delay_event.tick()


class Button:
    def __init__(self, *args):
        self.buttons = []
        for arg in args:
            self.buttons.append(ButtonEvent(*arg))


class MMA7660:
    def __init__(self, i2c:I2C):
        self.accel = mma7660.Accelerometer(i2c)


class Controller:
    joystick: Joystick
    button: Button
    def __init__(self):
        pass

    def set_button(self, button: Button):
        self.button = button

    def set_joystick(self, joystick):
        self.joystick = joystick

    def run(self):
        self.joystick.run()
