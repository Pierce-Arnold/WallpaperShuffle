
import time
from datetime import datetime
if __name__ == "__main__":
    #loop forever, always sleeping 1 second and printing when each minute rolls over
    while True:
        now = datetime.now() #finds the current time
        current_second = now.second #extracts the seconds from the current time
        if current_second == 0:
            print("its a new minute")
            time.sleep(59)
        time.sleep(1)
