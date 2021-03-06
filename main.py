import gc
import machine
from machine import Pin, ADC, I2C
from libs import lcd
from tetris import Game
import control
import music
from libs import ws2812
import uos


# initialize
machine.freq(240000000)
gc.collect()

# init lcd
spi_sck = Pin(2, Pin.OUT)
spi_tx = Pin(3, Pin.OUT)
lcd_reset = Pin(0, Pin.OUT)
lcd_dc = Pin(1, Pin.OUT)
lcd_width = 240
lcd_height = 240
spi_lcd = machine.SPI(0, baudrate=80000000, phase=1, polarity=1,
                      sck=spi_sck, mosi=spi_tx)
display = lcd.lcd_config(spi_lcd, width=lcd_width, height=lcd_height,
                         reset=lcd_reset, dc=lcd_dc, rotation=0)

game = Game(display)

controller = control.Controller()
# set joystick
control.xAxis = ADC(Pin(29))
control.yAxis = ADC(Pin(28))
joystick_controller = \
        control.Joystick([control.x_value, False, 0xFFF, 120, game.move_left],
                         [control.x_value, True,  0xEFFF, 120, game.move_right],
                         [control.y_value, False,  0xFFF, 120, game.rotate],
                         [control.y_value, True,  0xEFFF, 120, game.move_down])
controller.set_joystick(joystick_controller)

# set button
control.buttonB = Pin(5, Pin.IN, Pin.PULL_UP)  # B
control.buttonA = Pin(6, Pin.IN, Pin.PULL_UP)  # A
control.buttonStart = Pin(7, Pin.IN, Pin.PULL_UP)
control.buttonSelect = Pin(8, Pin.IN, Pin.PULL_UP)
button_controller = \
    control.Button([control.buttonB, Pin.IRQ_FALLING, 150, game.rotate],
                   [control.buttonA, Pin.IRQ_FALLING, 150, game.drop],
                   [control.buttonStart, Pin.IRQ_FALLING, 150, game.start_game],
                   [control.buttonSelect, Pin.IRQ_FALLING, 150, game.pause_game])
controller.set_button(button_controller)

# set accelerometer
i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=400000)
accelerometer = control.Accelerometer(i2c)
accelerometer.set_events([accelerometer.accel.getAcceleration_y, (-2, -0.5), 120, game.move_left],
                         [accelerometer.accel.getAcceleration_y, (0.5, 2), 120, game.move_right],
                         [accelerometer.accel.getAcceleration_x, (-2, -0.5), 120, game.move_down],
                         [accelerometer.accel.getAcceleration_x, (0.5, 2), 250, game.rotate])
controller.set_accelerometer(accelerometer)

# set game controller
game.set_controller(controller)

# setup music
# One buzzer on pin 23
music.set_up_musics(23)
game.set_musics(music.musics)

# set led
sck = 14
mosi = 15
miso = 12
ws2812.init_led(sck, mosi, miso, 256, 0.1)

game.run()
