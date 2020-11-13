from utime import ticks_ms
start_time=ticks_ms() # note t=time() is in seconds. to measure execution time

from utime import sleep_ms, sleep, sleep_us
import machine


# define GPIO pins
led=13 # wemos D1 d7
buzzer = 12 # d6 active low
mosfet = 15 # D8

hall = 14 # d5 active low. 0 is magnet close , door closed
stay = 4 # d2  to prevent deep sleep otherwize loose hand

"""
POWER consumption:
6ma in deep sleep with mosfet, and power ESP 8266 thru usb. led on hall sensor removed
9ma without mosfet. 

95 ma while running, 100ms
"""


print('ESP8266 frigo V1.2')

led = machine.Pin(led,machine.Pin.OUT, value=0) # set with led.on(), led.off()
buzzer = machine.Pin(buzzer, machine.Pin.OUT, value=1) # active low
mosfet = machine.Pin(mosfet,machine.Pin.OUT, value=1) # use mosfet to power buzzer and hall
# ESP8266 GPIO goes to low in deep sleep

stay = machine.Pin(stay, machine.Pin.IN,machine.Pin.PULL_UP) 
hall = machine.Pin(hall,machine.Pin.IN, machine.Pin.PULL_UP)
# connect stay pin to ground to prevent deep sleep , and keep contact with the ESP8266

deepsleep_duration = 30000  # in milli sec. so 30 sec
allowopen_duration = 30  # in sec . if door is detected open, will not trigger buzzer until this time

# power sensors. this is in case, should be set to 1 at boot
mosfet.on() 
sleep_ms(1)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
  print('woke from a deep sleep')
  # set led to signal wake up from deep sleep
  # clue the system is working
  led.on()
  sleep_ms(10)
  led.off()
    
    
else: 
  print('woke from power on')   
  # some sound to confirm the ESP8266 just booted from power on
  for i in range(3):
    buzzer.off()
    led.on()
    sleep(0.5)
    buzzer.on()
    led.off()
    sleep(0.5)
 
# disable alarms
led.off()
buzzer.on() # as active low, this means the buzzer does not produce sound

# test is door opened
door = hall.value()
print('value of hall sensor (1 is door open): ', door)


if door: # magnet is away from hall sensor, door opened
  print('door is open. wait a bit: ')
  sleep(allowopen_duration) # allow user to do their business with the fridge
  
  
while hall.value() == 1: # magnet is still away from hall sensor, door still opened
  print('door still open')
  buzzer.off() # sound, as the buzzer GPIO pin is active low
  led.on()
  sleep(1)
  
# door is finally closed
print('door closed. alarms off')
buzzer.on()
led.off()

print('turn mosfet off to cut power to sensors')
mosfet.off() # in case, should go to low in deep sleep
 
if stay.value() == 1: # as pin is pulled up, this means no jumper cable to ground
  print('stay pin (D2) is HIGH. go to deep sleep')
  # configure RTC.ALARM0 to be able to wake the device
  # to enable deep sleep, connect D1 (RST) to DO (GPIO 16)
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
 
  # set RTC.ALARM0 to fire after x seconds (waking the device)
  rtc.alarm(rtc.ALARM0, deepsleep_duration) 
  
  print ('script execution time(ms): ', ticks_ms()-start_time)
  
  print('enter deep sleep')
  machine.deepsleep()
  
  # at this point, will go to deep sleep and reboot after deepsleep_duration

else: # pin D2 is connected to ground
  print('stay pin (D2) is LOW. script terminates and you should get a REPL')
  print('Hall: ', hall.value())
  print('stay: ', stay.value())
  print('mosfet: ', mosfet.value())
  print('buzzer: ', buzzer.value())
  
  print('reset or power cycle the microcontroler to restart the script')
  
  # the programs stops, but micropython is still running. should get a REPL prompt
  
  
"""
uPyCraft will stay connected and show terminal ouput across deep sleep
even if go back to deep sleep immediatly at boot, can catch up and download . reset, set serial port, download. tricky timing

"""







