from libraries.nrf import Bridge
import time
from random import randint


nrf = Bridge('/dev/ttyACM1')#'/dev/ttyACM0'
camera, eBugs, unknown = nrf.assign_addresses()

ID = 0
for address, info in eBugs.items():
    nrf.set_TX_address(address)
    nrf.LCD_backlight(0)
    nrf.enable_LEDs(0,1,0,0)
    nrf.LED_brightness(20)
    LED_set = info['led_sequence']
    nrf.set_LEDs(*LED_set)
    ID += 1
