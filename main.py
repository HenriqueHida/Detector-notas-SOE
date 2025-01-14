from RPLCD.i2c import CharLCD
import sounddevice as sd
import numpy as np
import time as pytime 

# Initialize the LCD
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()

#  counter
detection_count = 0
last_update_time = 0 

# Audio detection callback
def detect_loud_audio(indata, frames, stream_time, status):  
    global detection_count, last_update_time
    if status:
        print(f"Status: {status}")
    # Calculate the volume as the RMS (Root Mean Square)
    volume = np.sqrt(np.mean(indata**2))

    # Threshold for loud audio 
    threshold = 0.05
    cooldown = 0.4  # Cooldown period in seconds

    current_time = pytime.time()
    if volume > threshold and (current_time - last_update_time) > cooldown:
        detection_count += 1
        last_update_time = current_time  

        # Print and update LCD display
        print(f"Audio detectectado! Count: {detection_count}")
        lcd.clear()
        lcd.write_string(f"audio detectado!")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"contador: {detection_count}")

try:
    print("Monitorando... Press Ctrl+C para parar.")
    lcd.write_string("escutando...")
    # Stream audio input
    with sd.InputStream(callback=detect_loud_audio):
        sd.sleep(20_000)  # Run for 20 seconds
except KeyboardInterrupt:
    print("Interrompido pelo user.")
    lcd.clear()
    lcd.write_string("Interrompido")
except Exception as e:
    print(f"An error occurred: {e}")
    lcd.clear()
    lcd.write_string("Error occurred")

