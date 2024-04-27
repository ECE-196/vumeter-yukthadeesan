import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep

# setup pins
microphone = AnalogIn(board.IO1)

status = DigitalInOut(board.IO17)
status.direction = Direction.OUTPUT

led_pins = [
    board.IO21,
    board.IO26, #type:ignore
    board.IO47,
    board.IO33, #type:ignore
    board.IO34, #type:ignore
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39,
]

leds = [DigitalInOut(pin) for pin in led_pins]

vold_thresholds = [20000, 25000, 30000, 35000, 40000, 45000, 50000, 60000, 70000, 80000, 900000]

for led in leds:
    led.direction = Direction.OUTPUT


filtered_volume = 0
smoothing_factor = 0.7

while True:
    volume = microphone.value
    
    print(volume)

    if volume > filtered_volume:
        filtered_volume = volume
    else:
        filtered_volume = smoothing_factor*filtered_volume+(1-smoothing_factor)*volume

    led_light = 0
    for i, t in enumerate(vold_thresholds):
        if filtered_volume >= t:
            led_light = i 

    for i, led in enumerate(leds):
        led.value = i < led_light

    sleep(0.1)