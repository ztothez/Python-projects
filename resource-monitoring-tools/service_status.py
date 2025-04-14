import builtins
import dbus
import logger
import os
import time
#Still-In-Progress

#Confguration options:
# - days = if uptime is greater than X, create alert
# - alert_interval = Create alert at most evey X minutes
# - poll_interval = Execute module evey X seconds

#Default configurations:
builtins.logdir = "error.log"
builtins.ALERT_TIME = {}
config = {
    "alert_status": "inactive" and "loaded",
    "alert_interval": 60,
    "poll_interval": 60
        }

def run(para=None):
    if para != None:
        for option in para:
            config[option] = para[option]
#Compare timestamp of last alert + alert interval to current one to determine if alert should be created. If this is the first time running, set alert to true
    try:
        alert_time_passed = (builtins.ALERT_TIME["service_status"] + config['alert_interval'] * 60 <= int(time.time()))
    except:
        alert_time_passed = True
    try:    
        service = 'man-db'
        bus = dbus.SystemBus()
        systemd = bus.get_object(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1'
        )
        manager = dbus.Interface(
            systemd,
            'org.freedesktop.systemd1.Manager'
        )
        service_unit = service if service.endswith('.service') else manager.GetUnit('{0}.service'.format(service))
        service_proxy = bus.get_object('org.freedesktop.systemd1', str(service_unit))
        service_properties = dbus.Interface(service_proxy, dbus_interface='org.freedesktop.DBus.Properties')
        service_load_state = service_properties.Get('org.freedesktop.systemd1.Unit', 'LoadState')
        print(service_load_state)
        service_active_state = service_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
        print("service_active",service_active_state)
        ret_dict = {
                    "Alert": ((service_active_state) <= config['alert_status'] and alert_time_passed),
                    "LoadState": str(service_load_state),
                    "ActiveState": str(service_active_state),
#Eli määritän sen login sille ja luen sen infon sieltä mistä se on määritetty jos ei ole määritetty /var/log/messages#                    "log":{'rivi1', 'rivi2'}
                    }
        print("ret",ret_dict)
        if alert_time_passed:
            builtins.ALERT_TIME["service_status"] = int(time.time())
        next_run = int(time.time()) + config["poll_interval"]
        if service_load_state == 'loaded' and service_active_state == 'inactive':
            service_active_state = service_properties.Get('org.freedesktop.systemd1.Unit', 'StatusState')
        return ret_dict
    except FileNotFoundError as e:
        logger.log("ERROR",os.path.basename(__file__),"Module failed: {}:{}".format(str(e),str(e.filename)))

    except Exception as e:
        logger.log("ERROR",os.path.basename(__file__),"Module failed; " + str(e))
while 1:
    print(run())
    time.sleep(1)
