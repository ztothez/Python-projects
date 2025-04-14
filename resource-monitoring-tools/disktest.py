import psutil
import os

##usage = shutil.disk_usage(os.getcwd())
##usage2 = shutil.disk_usage(())
##total = usage[0]
##used = usage[1]
##free = usage[2]
##print(usage)
##print(usage2)
##print("total",total)
##print("used",used)
##print("Free",free)



values = []
disk_partitions = psutil.disk_partitions(all=True)
for partition in disk_partitions:
    usage = psutil.disk_usage(partition.mountpoint)
    device = {'device': partition.device,
              #'mountpoint': partition.mountpoint,
              #'fstype': partition.fstype,
              #'opts': partition.opts,
              'total': usage.total,
              'used': usage.used,
              'free': usage.free,
              'percent': usage.percent
              }
    values.append(device)
    print(device)
values = sorted(values, key=lambda device: device['device'])


