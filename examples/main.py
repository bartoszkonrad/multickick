import multiclick
from machine import Pin

led = Pin(2, Pin.OUT)

# esp8266 inputs
# btn = click.MultiClick(14)

# mcp inputs
btn = click.MultiClick(1, 'mcp')

while True:
    btn.update()

    if btn.is_click():
        print('click')
    if btn.is_single_click():
        print('single')
        led.on()
    if btn.is_hold():
        print('hold')
        led.off()
