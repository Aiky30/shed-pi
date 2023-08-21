import os
import glob
import time
from datetime import datetime
import logging


logging.basicConfig(
    filename = '/var/log/shed-pi.log',
    level = logging.INFO,
    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger("parent")
TIME_TO_SLEEP = 60 # time in seconds


class TempProbe:
    def __init__(self):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def read_temp(self):
        def read_temp_raw():
            f = open(self.device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines

        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c


def check_os():
    return os.uname()[4].startswith("arm")

def get_cpu_temp():
    cpu_temp = os.popen("vcgencmd measure_temp").readline()

    # Convert the temp read from the OS to a clean float
    return float(cpu_temp.replace("temp=","").replace("'C\n", ""))


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S") # 24-Hour:Minute:Second
    return current_time

def main():

    logger.info(f"Shed pi started: {get_time()}, using version: 0.0.1")

    if not check_os():
        logger.error("only rasbian os supported")
        return

    temp_probe = TempProbe()

    while True:
        pi_temp = get_cpu_temp()
        probe_1_temp = temp_probe.read_temp()
        logger.info(f"Pi temp: {pi_temp}, probe_1 temp: {probe_1_temp}")

        time.sleep(TIME_TO_SLEEP)

if __name__ == "__main__":
    main()
