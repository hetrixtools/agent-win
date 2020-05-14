import time
import base64

import psutil
import requests
import wmi
from win32com.client import GetObject
import pythoncom

####################
# Settings
####################
# Server version (do not edit)
VERSION = '1.5.4'
URL = 'https://sm.hetrixtools.net'

####################
# Functions
####################
def get_win_version():
    c = wmi.WMI()
    for os_record in c.Win32_OperatingSystem():
        win = os_record.Caption
        sp = os_record.ServicePackMajorVersion
    win = win.replace('Microsoft ','')
    if sp and sp > 0:
        win += 'SP'+str(sp)
    return win


def get_cpu_type():
    root_winmgmts = GetObject("winmgmts:root\cimv2")
    cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
    return cpus[0].Name

def gather_data(server_id):
    pythoncom.CoInitialize()
    # Initial Network Stats
    net_stats1 = psutil.net_io_counters()
    
    # Time
    sec = int(time.strftime("%S"))
    sleep = 60 - sec

    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=sleep)

    # Secondary Network Stats
    net_stats2 = psutil.net_io_counters()

    # OS
    os_name = base64.b64encode(get_win_version())

    # Uptime
    uptime = int(time.time() - psutil.boot_time())

    # CPU Model
    cpu_model = base64.b64encode(get_cpu_type())

    # CPU Speed
    cpu_speed = int(psutil.cpu_freq().current)

    # CPU Cores
    cpu_cores = psutil.cpu_count()

    # IOWait
    cpu_iowait = 0

    # RAM Info
    ram_info = psutil.virtual_memory()

    # RAM Size
    ram_size = int(ram_info.total/1000)

    # RAM Usage
    ram_usage = ram_info.percent

    # Swap Info
    swap_info = psutil.swap_memory()

    # Swap Size
    swap_size = int(swap_info.total/1000)

    # Swap Usage
    swap_usage = swap_info.percent

    # Disks
    disks = psutil.disk_partitions()
    all_disk_data = []
    for disk in disks:
        if disk.fstype:
            try:
                disk_usage = psutil.disk_usage(disk.mountpoint)
                disk_data = ','.join([disk.mountpoint, str(disk_usage.total), str(disk_usage.used)])
                all_disk_data.append(disk_data)
            except:
                pass

    disk_str = '{};'.format(';'.join(all_disk_data))
    disks = base64.b64encode(disk_str)

    # Network
    rx = int((net_stats2.bytes_recv - net_stats1.bytes_recv)/sleep)
    tx = int((net_stats2.bytes_sent - net_stats1.bytes_sent)/sleep)

    # Post Data
    data = [
        os_name,
        str(uptime),
        cpu_model,
        str(cpu_speed),
        str(cpu_cores),
        str(cpu_usage),
        str(cpu_iowait),
        str(ram_size),
        str(ram_usage),
        str(swap_size),
        str(swap_usage),
        disks,
        str(rx),
        str(tx)
    ]
    post_data = '{}|'.format('|'.join(data))

    payload = {'v': VERSION, 'a': '2', 's': server_id, 'd': post_data}

    # Post the collected data
    requests.post(URL, data=payload, timeout=15)
