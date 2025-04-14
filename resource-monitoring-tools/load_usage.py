import builtins
import logger
import os
import time


#Confguration options:
# - days = if uptime is greater than X, create alert
# - alert_interval = Create alert at most evey X minutes
# - poll_interval = Execute module evey X seconds

#Default configurations:
builtins.logdir = "error.log"
builtins.ALERT_TIME = {}
config = {
    "alert_percent": 5,
    "alert_interval": 60,
    "poll_interval": 60
        }


def run(param=0):
    if param != 0:
       for option in param:
            config[option] = param[option]
#Compare timestamp of last alert + alert interval to current one to determine if alert should be created. If this is the first time running, set alert to true
    try:
        alert_time_passed = (builtins.ALERT_TIME["load_usage"] + config['alert_interval'] * 60 <= int(time.time()))
    except:
        alert_time_passed = True
    try:
        #Opens the proc/loadavg command as read.
        with open("/proc/loadavg","r") as f:
            #Adds variable to read line f=file short term.
            lines =f.readline().split()
            core_load = float(lines[0])

        with open("/proc/cpuinfo","r") as f:
            lines = f.read().split('cpu cores	: ')[1].split('\n')[0]
            core_number = int(lines)

    except FileNotFoundError as e:
        logger.log("ERROR",os.path.basename(__file__),"Module failed: {}:{}".format(str(e),str(e.filename)))

    except Exception as e:
        logger.log("ERROR",os.path.basename(__file__),"Module failed; " + str(e))
    
    core_usage = float(core_load)/(core_number)*100
    ret_dict = {
                "Alert": ((core_usage) >= config['alert_percent'] and alert_time_passed),
                "CoreLoad:": core_load,
                "CoreNumber:": core_number,
                "CoreUsage:": core_usage,
                }
    if alert_time_passed:
        builtins.ALERT_TIME["load_usage"] = int(time.time())
    next_run = int(time.time()) + config["poll_interval"]
    return(ret_dict)

while 1:
    print(run())
    time.sleep(1)
