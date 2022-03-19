from django.shortcuts import render
from uptime import uptime
import subprocess
import re
# Create your views here.

TESTING_STATS = """Name                     Remote IP                  Virtual IP      Bytes Received      Bytes Sent      Last Seen
neongm_main_desktop      00.000.000.00:00000        10.6.0.2        211MiB              1.7GiB          Mar 18 2022 - 12:19:22
neongm_android_1         00.000.000.00:00000        10.6.0.3        462MiB              1.6GiB          Mar 19 2022 - 10:36:14
ars_peer_poland          00.000.000.00:00000        10.6.0.4        500MiB              5.1GiB          Mar 19 2022 - 09:28:34
primary                  (none)                     10.6.0.5        0B                  0B              (not yet)
mobile                   (none)                     10.6.0.6        0B                  0B              (not yet)
grig_mobile              00.000.000.00:00000        10.6.0.7        114MiB              2.1GiB          Mar 19 2022 - 10:37:18
neongm_laptop            00.000.000.00:00000        10.6.0.8        37MiB               127MiB          Mar 19 2022 - 10:35:34
grig_desktop             (none)                     10.6.0.9        0B                  0B              (not yet)"""

def index(req):

    context = {
        'title': 'wireguard vps server',
        'uptimeDays': round(uptime()/(3600*24), 2),
        'uptimeHours': round(uptime()/3600, 2),
        'uptimeSeconds': round(uptime(), 2),
    }
    return render(req, 'index.html', context)


class statsCollector():
    def __init__(self):
        self.raw_data = TESTING_STATS
        self.data = []
    
    def process_data(self):
        data_array = self.raw_data.split('\n')
        data = [user_data.split() for user_data in data_array]




def index_testing_stats(req):
    p = subprocess.Popen(["pivpn -c"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    
    stats = output.decode('utf-8').split()
    MiB = sum([float(val.replace('MiB', '')) for val in stats if 'MiB' in val])
    GiB = sum([float(val.replace('GiB', '')) for val in stats if 'GiB' in val])
    print(GiB)
    data_used = MiB/1024 + GiB
    context = {
        'title': 'wireguard vps server',
        'uptimeDays': round(uptime()/(3600*24), 2),
        'uptimeHours': round(uptime()/3600, 2),
        'uptimeSeconds': round(uptime(), 2),
        'stats': round(data_used, 2) 
    }
    return render(req, 'index.html', context)