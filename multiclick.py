import time
import mcp
from machine import Pin


class MultiClick(object):

    active_high = 0
    btn_state = not active_high
    last_state = btn_state
    click_count = 0
    clicks = 0
    depressed = 0
    last_bounce_time = 0
    debounce_time = 20
    multiclick_time = 200
    long_click_time = 600

    def __init__(self, pin, target=None):
        self.target = target
        self.pin = pin
        if self.target is None:
            self.button = Pin(self.pin, Pin.IN, Pin.PULL_UP)
        elif self.target == 'mcp':
            self.io = mcp.MCP23017()
            self.io.setup(self.pin, mcp.IN)
            self.io.pullup(self.pin, True)

    def update(self):
        self.now = time.ticks_ms()
        if self.target is None:
            self.btn_state = self.button.value()
        elif self.target == 'mcp':
            self.btn_state = self.io.input(self.pin)

        if not self.active_high:
            self.btn_state = not self.btn_state

        if self.btn_state != self.last_state:
            self.last_bounce_time = self.now

        if self.now - self.last_bounce_time > self.debounce_time and self.btn_state != self.depressed:
            self.depressed = self.btn_state
            if self.depressed:
                self.click_count += 1

        if not self.depressed and self.now - self.last_bounce_time > self.multiclick_time:
            self.clicks = self.click_count
            self.click_count = 0

        if self.depressed and (self.now - self.last_bounce_time > self.long_click_time):
            self.clicks = 0 - self.click_count
            self.click_count = 0

        self.last_state = self.btn_state

    def is_click(self):
        return True if self.clicks else False

    def is_single_click(self):
        return True if self.clicks == 1 else False

    def is_double_click(self):
        return True if self.clicks == 2 else False

    def is_triple_click(self):
        return True if self.clicks == 3 else False

    def is_hold(self):
        return True if self.clicks == -1 else False

    def is_single_click_and_hold(self):
        return True if self.clicks == -2 else False

    def is_double_click_and_hold(self):
        return True if self.clicks == -3 else False
