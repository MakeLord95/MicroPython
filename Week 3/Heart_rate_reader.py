import time
from fifo import Fifo
from machine import Pin, ADC
from piotimer import Piotimer

# Piotimer callback
def read_signal(timer):
    buffer.put(adc.read_u16())

# Sampling rate
fs = 250

# ADC
adc = ADC(Pin(26))

# Fifo
buffer = Fifo(1000)

# Piotimer
tmr = Piotimer(freq=fs, callback=read_signal)

prev_peak_time = 0
previous_signal = 0
peak_candidate = False

while True:
    current_signal = buffer.get()
    # print(current_signal)
    
    if current_signal > previous_signal:
        peak_time = time.ticks_ms()
        peak_candidate = True

    elif peak_candidate and current_signal < previous_signal and current_signal > 36500:
        # print(previous_signal)
        if prev_peak_time > 0:
            time_diff = peak_time - prev_peak_time
            # print(f"Time diff: {time_diff}ms")
            
            hr = round(60 / (time_diff / 1000))
            
            if hr < 45:
                pass
            elif hr > 150:
                pass
            else:            
                print(f"Heart rate: {hr}bpm")
            
        peak_candidate = False
        prev_peak_time = peak_time

    previous_signal = current_signal
    
    time.sleep(1 / fs)
