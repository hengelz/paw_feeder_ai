import gpiod
LED_PIN = 21
BUTTON_PIN = 6
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
button_line = chip.get_line(BUTTON_PIN)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
button_line.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
led_line.set_value(0)
try:
    while True:
        button_state = button_line.get_value()
        if button_state == 0:
            #print('button pressed')
           led_line.set_value(1)
        else:
           led_line.set_value(0)
finally:
    led_line.release()
    button_line.release()