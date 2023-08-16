import array
from machine import Pin, Signal, ADC, I2C
from piotimer import Piotimer
import ssd1306
from fifo import Fifo
import utime

# Functions

def difference_calculator(array, threshold_b, threshold_a, heart_value):
    filtered_values = [num for num in array if num > heart_value - threshold_b and num < heart_value + threshold_a and num != 0]
    if len(filtered_values) > 0:
        average_value = sum(filtered_values) / len(filtered_values)
        return average_value
    else:
        return 0
    
def resetter(x):
    data_manager.reset_bpm()
    
def pulse_check(x):
    readed = adc.read_u16()
    buffer.put(readed)
    
# Classes

class Datamanager:
    def __init__(self):
        i2c = I2C(1, scl=Pin("GP15"), sda=Pin("GP14"), freq=400000)
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.text_screen = []
        self.text_screen.append(["", 16])
        self.text_screen.append(["", 42])
        self.average_bpm = 0
        self.bpm_rack = []
        self.size = 10
        
    def bpm_adder(self, bpm):
        if 45 < bpm < 240:
            self.bpm_rack.append(bpm)
            if len(self.bpm_rack) > self.size:
                self.bpms.pop(0)
            self.average_bpm = int(sum(self.bpm_rack) / len(self.bpm_rack))
            
    def bpm_resetter(self):
        self.average_bpm = 0
        self.bpm_rack = []
    
    def bpm_shower(self):
        self.text_shower("Bpm is : " + str(self.average_bpm), self.text_screen[0][0], 32)
        self.text_screen[0] = ["Bpm is : " + str(self.average_bpm), 32]
        
    def touch(self, text):
        self.text_shower(text, self.text_screen[1][0], 42)
        self.text_screen[1] = [text, 42]
        
    def text_shower(self, value, oldvalue, pos):
        self.oled.text(oldvalue, 0, pos, 0)
        self.oled.text(value, 0, pos)
        self.oled.show()
    
        
class heartbeat:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.last_state = 0
        self.print_countter = 0
        self.highest_value = 0
        self.tip = 0
        self.high = 0
        self.previosly_high = 0
        self.dip = 0
        self.previosly_d = 0
        
    def beat_processer(self, value, average, dropped, max_value):
        pulse_checker = (average + max_value) // 2
        self.print_countter += 1
        if self.print_countter > 7:
            print("Pulse is: ", value, pulse_checker, average)
            self.print_countter = 0
            
            
        if value > pulse_checker:
            if self.last_state == 0:
                self.previosly_d = self.dip
                self.dip = 0
            
            if self.highest_value < value:
                self.highest_value = value
                self.high = 0
            
            self.high += 1
            self.tip += 1
            self.last_state = 1
        else:
            if self.last_state == 1:
                if self.previosly_high > 0:
                    self.bpm_calculator(self.previosly_high + self.dip + abs(self.high - self.tip), dropped)
                    
                self.previosly_high = self.high
                #Resetter
                self.high = 0
                self.tip = 0
                self.highest_value = 0
                
            self.dip += 1
            self.last_state = 0
            
    def bpm_calculator(self, times, delay):
        if delay < 1:
            delay = 1
        bpm = int(60 / (times * .004 * (delay)))
        self.data_manager.bpm_adder(bpm)
        
#Main program
        
adc = ADC(Pin("GP26"))
led = Pin("LED", Pin.OUT)
reset_pin = Pin("GP12", mode = Pin.IN, pull = Pin.PULL_UP)
reset_pin.irq(handler = resetter, trigger = Pin.IRQ_FALLING)
data_manager = Datamanager()
data_manager.bpm_shower()
beat_calculator = heartbeat(data_manager)
divider = 5
buffer_size = 755
buffer = Fifo(buffer_size)
average_data = Fifo(buffer_size // divider)
counter = 0
average = 0
second_average = 0
previosly_second_average = 0
difference = 0
minimium_average = 12000
maximium_average = 50000
maximium_difference = 23000
countting = 0
last_state = 1
last_bpm = 0
sample_rate = 250
timer = Piotimer(freq = sample_rate, callback=pulse_check)
while True:
    if buffer.empty():
        continue
    raw_value = buffer.get()
    second_average = raw_value
    counter += 1
    dropped = buffer.dropped()
    buffer.dc = 0
    if divider < counter:
        average_data.put(second_average)
        difference = abs(second_average - previosly_second_average)
        previosly_second_average = second_average
        average = difference_calculator(average_data.data, maximium_difference * 0.85, maximium_difference, average_data.get())
        counter = 0
        second_average = 0
        
    if minimium_average < average < maximium_average and difference < maximium_difference:
        beat_calculator.beat_processer(raw_value, average, max(average_data.data), dropped)
        if last_bpm != data_manager.average_bpm:
            data_manager.bpm_shower()
            last_bpm = data_manager.average_bpm
        countting = 1
    else:
        countting = 0
        
    if countting == 1 and last_state == 0:
        data_manager.touch("Calculating")
        last_state = 1
    elif countting == 0 and last_state == 1:
        data_manager.touch("Press the finger")
        last_state = 0

                
            
        