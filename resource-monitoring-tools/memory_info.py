import builtins
import logger
from os path
import time


#Confguration options:
# - days = if uptime is greater than X, create alert
# - alert_interval = Create alert at most evey X minutes
# - poll_interval = Execute module evey X seconds

#Default configurations:
builtins.logdir = "error.log"
builtins.ALERT_TIME = {}
config = {
    "alert_percent": 100,
    "alert_interval": 60,
    "poll_interval": 60
        }

def run(para=None):
    if para != None:
        for option in para:
            config[option] = para[option]
#Compare timestamp of last alert + alert interval to current one to determine if alert should be created. If this is the first time running, set alert to true
    try:
        alert_time_passed = (builtins.ALERT_TIME["memory_info"] + config['alert_interval'] * 60 <= int(time.time()))
    except:
        alert_time_passed = True
    try:    
        #Opens the proc/meminfo command as read.     
        with open("/proc/meminfo", "r") as f:
            #Adds variable to read line f=file short term.
            lines =f.readlines()
            #Saves MemTotal,MemFree,MemAvailable to variables, removes unwanted spaces and outputs.
            mem_total = lines[0].strip().replace("MemTotal: ","").replace("kB","")
            mem_free = lines[1].strip().replace("MemFree: ","").replace("kB","")
            mem_available = lines[2].strip().replace("MemAvailable: ","").replace("kB","")
            #This is for converting to string to value.
            conv_total = int(mem_total)
            conv_free = int(mem_free)
            conv_available = int(mem_available)
            #The calculating percent of MemAvaiable and MemTotal.
            percentage = float(conv_available/conv_total*100)

            #The output print comes as KiloBytes.
            ret_dict = {
                    "Alert": ((percentage) <= config['alert_percent'] and alert_time_passed),
                    "MemTotal_kB": conv_total,
                    "MemFree_kB":  conv_free,
                    "MemAvailable_kB": conv_available,
                    "UsagePercentage": percentage
                    }
        if alert_time_passed:
            builtins.ALERT_TIME["memory_info"] = int(time.time())
        next_run = int(time.time()) + config["poll_interval"]
        return ret_dict
    except FileNotFoundError as e:
        logger.log("ERROR",path.basename(__file__),"Module failed: {}:{}".format(str(e),str(e.filename)))

    except Exception as e:
        logger.log("ERROR",path.basename(__file__),"Module failed; " + str(e))
while 1:
    print(run())
    time.sleep(1)
