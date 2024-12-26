# https://video.search.yahoo.com/search/video?fr=mcafee&p=connecting+a+relay+to+raspberry+pi&type=E210US1494G0#id=3&vid=1ff4fa512c01ebcba72f54fef1506161&action=click

import gpiod
import time
RELAY_PIN = 18
chip = gpiod.Chip('gpiochip4')
relay_line = chip.get_line(RELAY_PIN)
relay_line.request(consumer="RELAY", type=gpiod.LINE_REQ_DIR_OUT)
try:
   while True:
       relay_line.set_value(1)
       time.sleep(10)
       relay_line.set_value(0)
       time.sleep(10)
finally:
   led_line.release()

