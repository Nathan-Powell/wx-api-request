import requests
import sys
from datetime import datetime, timedelta
import os.path
import shutil

nl = "\n"
log_path = "C:\\Scripts\\log.txt"
temp_file = "C:\\Scripts\\temp.txt"
old_log_dir = "C:\\Scripts\\old_logs\\log.txt"

# Set current time for log timestamps.
raw_time = datetime.now()
timestamp = raw_time.strftime("%m-%d-%Y %H:%M:%S")

# Open log file and append.
try:
    log_file = open(log_path, "a")
except OSError as err:
    print(f"OS error: {err}")
    sys.exit()

# If the file is inaccessible the script will throw an error and exit.
try:
    text_file = open(temp_file, "w+")
except OSError as err:
    print(f"OS error: {err}")
    log_file.write(f"{timestamp} | ERROR | Unable to access T:temp.txt{nl}")
    sys.exit()

# Requests data from WX API and parses temperature. 
def get_temp(log):
    try:
        response = requests.get("https://sample.api/observations.json?language=en-US&units=e&apiKey=123456789abcd").json()
        raw_temp = float(response['observation']['temp'])
        global temp
        temp = int(raw_temp)
        print(f"Temperature: {temp}")
        return temp
    except:
        print("Failed to access API or data does not match format.")
        log.write(f"{timestamp} | ERROR | Failed to access API or data does not match format.{nl}")
        sys.exit()

# Writes temp to text file. If temp variable holds invalid data, writes blank value to file.
get_temp(log_file)
if isinstance(temp, int) == True:
    text_file.write(str(temp))
    log_file.write(f"{timestamp} | INFO | Temperature: {str(temp)} | Successfully wrote temp to {temp_file}{nl}")
else:
    log_file.write(f"{timestamp} | ERROR | get_temp() returned malformed data.{nl}")
    text_file.write('')

# Gracefully close files before exit
text_file.close()
log_file.close()

# Check log file age. If age is older than 7 days, move file to backup folder.
old_log_file = os.path.getctime(log_path)
old = raw_time - timedelta(days=7)
old_date = old.timestamp()
if old_log_file < old_date:
    shutil.move(log_path, old_log_dir)

