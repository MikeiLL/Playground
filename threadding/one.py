import threading
import time

def wait_for_signal():
    print("Waiting for a signal...")
    event.wait()
    print("Signal received!")

event = threading.Event()
thread = threading.Thread(target=wait_for_signal)
thread.start()

# Simulate some work
time.sleep(3)
event.set()  # Send the signal
