import time
from fifo import Fifo
from machine import Pin, ADC
from piotimer import Piotimer
from oled_utils import oled_setup
from Project.web_handler import wifi_connector, kubios_upload


# Starting message
def start_message():
    global oled
    
    oled.fill(0)
    
    oled.rect(0, 0, 128, 64, 1)
    oled.text("PulseVision", 20, 4)
    oled.hline(20, 12, 88, 1)
    
    oled.text("Measures your", 5, 20)
    oled.text("HR, PNS and SNS", 5, 28)
    oled.text("Indexes", 5, 36)
    
    oled.fill_rect(2, 45, 124, 17, 1)
    
    oled.text("Press Rotary", 15, 46, 0)
    oled.text("to Start", 20, 54, 0)
    
    oled.show()


# Calibration message
def calibration_message():
    global oled
    
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)
    
    oled.text("!Calibrating!", 15, 4)
    
    oled.hline(18, 12, 98, 1)
    
    oled.fill_rect(20, 23, 96, 25, 1)
    
    oled.text("Please don't", 20, 24, 0)
    oled.text("move the", 35, 32, 0)
    oled.text("sensor", 45, 40, 0)
    
    oled.show()


# Message after calibration
def calibration_done():
    global oled
    global threshold
    
    oled.fill(0)
    
    oled.rect(0, 0, 128, 64, 1)
    
    oled.text("Calibration", 15, 4)
    oled.text("complete", 15, 12)
    
    oled.text("Threshold:", 15, 24)
    oled.text(f"{threshold}", 15, 32)
    
    oled.fill_rect(2, 45, 124, 17, 1)
    
    oled.text("Press Rotary", 15, 46, 0)
    oled.text("to continue", 20, 54, 0)
    
    oled.show()


# Main program message
def main_message():
    global oled
    
    oled.fill(0)
    
    oled.rect(0, 0, 128, 64, 1)
    
    oled.text("Measuring", 15, 4)
    
    oled.text("Results will",15 , 24)
    oled.text("be displayed", 15, 32)
    oled.text("in a moment", 15, 40)
    
    oled.show()


# Kubios results message
def results_message(resp):
    oled.fill(0)
    
    oled.rect(0, 0, 128, 64, 1)
    
    oled.text("Results", 30, 5)
    
    oled.text(f"SNS: {resp["analysis"]["sns_index"]:.2f}", 15, 32)
    oled.text(f"PNS: {resp["analysis"]["pns_index"]:.4f}", 10, 40)
    oled.text(f"Mean HR: {int(resp["analysis"]["mean_hr_bpm"])}bpm", 3, 48)
    
    oled.show()

# Callback to read signal
def read_signal(tmr):
    global buffer
    buffer.put(adc.read_u16())


# Calculating the threshold for BPM calculator
def calculate_threshold(arr):
    global threshold
    threshold = int(sum(arr) / len(arr))
    
    
# Calculating the BPM
def calculate_bpm():
    global fs
    global hr
    global ppi
    global peak
    global buffer
    global peak_time
    global threshold
    global ppi_array
    global prev_peak_time
    global peak_candidate
    global previous_signal

    current_signal = buffer.get()

    if current_signal > threshold and current_signal > previous_signal:
        peak_time = time.ticks_ms()
        peak_candidate = True
        
    elif threshold < current_signal < previous_signal and peak_candidate:
        if prev_peak_time > 0:
            time_diff = (peak_time - prev_peak_time) / 1_000
            if time_diff > 0:
                hr = 60 / time_diff
                
                if 150 > hr > 45:
                    ppi = 1 / (hr / 60_000)
                    
                    ppi_array.append(int(ppi))
                
                    print(f"HR: {int(hr)}, PPI: {int(ppi)}")
        peak_candidate = False
        prev_peak_time = peak_time

    previous_signal = current_signal


# SW_0 and SW_2 interrupt handler
def interrupt_handler(pin):
    global held
    global threshold
    
    if threshold:
        if SW_0.value() == 0 and not held and threshold > 1000:
            held = True
            threshold -= 1000
        elif SW_2.value() == 0 and not held and threshold < 64534:
            held = True
            threshold += 1000
            
    if SW_0.value() == 1:
        held = False
    if SW_2.value() == 1:
        held = False

# Variables
hr = 0
hr = 0
fs = 75
tmr = 0
ppi = 0
peak = 0
count = 0
array = []
held = False
peak_time = 0
ppi_array = []
threshold = None
prev_peak_time = 0
previous_signal = 0
buffer_size = 1024
peak_candidate = False

# Wifi credentials here
SSID = "KMD657_Group_8"
PASSWORD = "viiskytkuus"

# Join the wifi network
ip = wifi_connector(SSID, PASSWORD)

# Creating the ADC, OLED, Fifo and Buttons
adc = ADC(Pin(26))
oled = oled_setup()
buffer = Fifo(buffer_size)
ROT = Pin(12, Pin.IN, Pin.PULL_UP)
SW_0 = Pin(9, Pin.IN, Pin.PULL_UP)
SW_1 = Pin(8, Pin.IN, Pin.PULL_UP)
SW_2 = Pin(7, Pin.IN, Pin.PULL_UP)


SW_2.irq(handler=interrupt_handler, trigger=Pin.IRQ_FALLING)
SW_0.irq(handler=interrupt_handler, trigger=Pin.IRQ_FALLING)


# Main program starts here

# Display starting message 
start_message()

# Wait for user to push the rotary
while ROT.value() == 1:
    pass

# Display the calibration message
calibration_message()

# We create the Piotimer and sleep for 5 sec, after which, we stop the Piotimer
tmr = Piotimer(freq=fs, callback=read_signal)
time.sleep(5)
tmr.deinit()

# We go through the Fifo buffer and append them to the array
while not buffer.empty():
    array.append(buffer.get())

# We calculate the threshold for BPM measuring
calculate_threshold(array)

# Display the threshold and calibration message
calibration_done()

# Wait for user to press the rotary
while ROT.value() == 1:
    if SW_1.value() == 0:
        # Display the calibration message
        calibration_message()

        # We create the Piotimer and sleep for 5 sec, after which, we stop the Piotimer
        tmr = Piotimer(freq=fs, callback=read_signal)
        time.sleep(5)
        tmr.deinit()

        # We go through the Fifo buffer and append them to the array
        while not buffer.empty():
            array.append(buffer.get())

        # We calculate the threshold for BPM measuring
        calculate_threshold(array)

        # Display the threshold and calibration message
        calibration_done()
        
    else:
        # Display the threshold and calibration message
        calibration_done()
        pass

# Display main program message
main_message()

# We create a new timer for BPM measuring
tmr = Piotimer(freq=fs, callback=read_signal)

# Main loop
while True:
    if not buffer.empty():
        calculate_bpm()
    
        if len(ppi_array) == 20:
            upload = True

            response = kubios_upload(ppi_array)
            print(response)
            ppi_array.clear()
            results_message(response)
                
        else:
            continue
    
    else:
        continue
    
    time.sleep(1 / fs)
