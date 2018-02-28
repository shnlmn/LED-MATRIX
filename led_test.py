from gpiozero import LED
led = LED(18)
import time

while 1:
    print("loop begin")
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
