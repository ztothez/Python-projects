import builtins
import logger
import os
import time
from collections import namedtuple



#Confguration options:
# - days = if uptime is greater than X, create alert
# - alert_interval = Create alert at most evey X minutes
# - poll_interval = Execute module evey X seconds

#Default configurations:
builtins.logdir = "error.log"
builtins.ALERT_TIME = {}
config = {
    "alert_percent": 2,
    "alert_interval": 60,
    "poll_interval": 60,
    "Physical_Disk_Only": False
        }

disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')

ret_dict = {}

def run(para=None):
    if para != None:
        for option in para:
            config[option] = para[option]
#Compare timestamp of last alert + alert interval to current one to determine if alert should be created. If this is the first time running, set alert to true
    try:
        alert_time_passed = (builtins.ALERT_TIME["disk_info"] + config['alert_interval'] * 60 <= int(time.time()))
    except:
        alert_time_passed = True

    
    phydevs = []
    with open("/proc/filesystems", "r") as f:
        for line in f:
##            if not line.startswith("nodev"):
            phydevs.append(line.strip())
    all = config["Physical_Disk_Only"]
    retlist = []
    with open('/proc/mounts', "r") as f:
        for line in f:
            if not all and line.startswith('none'):
                continue
            fields = line.split()
            device = fields[0]
            mountpoint = fields[1]
            fstype = fields[2]
            if not all and fstype not in phydevs:
                continue
            if device == 'none':
                device = ''
            ntuple = disk_ntuple(device, mountpoint, fstype)
            retlist.append(ntuple.device)
            st = os.statvfs(ntuple.mountpoint)
            free = (st.f_bavail * st.f_frsize)
            total = (st.f_blocks * st.f_frsize)
            used = (st.f_blocks - st.f_bfree) * st.f_frsize
            try:
                percent = ret = (float(used) / total) * 100
            except ZeroDivisionError:
                percent = 0
            print(retlist,usage_ntuple(total, used, free, round(percent, 1)))
            ret_dict["Device_" + ntuple.device] = "True"
            ret_dict["Mountpoint_" + ntuple.mountpoint] = "True"
            ret_dict["Fstype_" + ntuple.fstype] = "True"
            ret_dict["DiskInfo_" + ntuple.device] = usage_ntuple(total, used, free, round(percent, 1))
            #ret_dict["Alert", ((percent) >= config['alert_percent'] and alert_time_passed)]
        if alert_time_passed:
            builtins.ALERT_TIME["disk_info"] = int(time.time())
        next_run = int(time.time()) + config["poll_interval"]
        return ret_dict
##    except FileNotFoundError as e:
##        logger.log("ERROR",os.path.basename(__file__),"Module failed: {}:{}".format(str(e),str(e.filename)))
##
##    except Exception as e:
##        logger.log("ERROR",os.path.basename(__file__),"Module failed; " + str(e))
while 1:
    print(run())
    time.sleep(1)
