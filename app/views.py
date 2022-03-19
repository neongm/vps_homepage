from django.shortcuts import render
from uptime import uptime
import subprocess
import re
# Create your views here.


class statsCollector():
    def __init__(self, data = []):
        self.data = data
        self.traffic_received = 0
        self.traffic_sent = 0
    
    def process_data(self, data = []):
        if len(self.data): data_array = self.data.split('\n')
        else: data_array = data.split('\n')

        self.data = [user_data.split() for user_data in data_array]
    
    def get_received_traffic(self):
        if self.traffic_received == 0:
            mib = sum([float(d[3].replace('MiB', ''))/1024 for d in self.data if 'MiB' in d[3]])
            gib = sum([float(d[3].replace('GiB', '')) for d in self.data if 'GiB' in d[3]])
            self.traffic_received = mib + gib
        return self.traffic_received

    def get_sent_traffic(self):
        if self.traffic_sent == 0:
            mib = sum([float(d[4].replace('MiB', ''))/1024 for d in self.data if 'MiB' in d[4]])
            gib = sum([float(d[4].replace('GiB', '')) for d in self.data if 'GiB' in d[4]])
            self.traffic_sent = mib + gib

        return self.traffic_sent

    def get_full_traffic(self):
        return self.get_sent_traffic() + self.get_received_traffic()

    def get_peer_count(self):
        return len(self.data)-1
    
    def get_active_peer_count(self):
        return self.get_peer_count() - len([d[4] for d in self.data if "0B" in d[4]])


def index(req):
    # getting data
    p = subprocess.Popen(["pivpn -c"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    # proccessing data
    td = """Name                     Remote IP                  Virtual IP      Bytes Received      Bytes Sent      Last Seen
neongm_main_desktop      00.000.000.00:00000        10.6.0.2        211MiB              1.7GiB          Mar 18 2022 - 12:19:22
neongm_android_1         00.000.000.00:00000        10.6.0.3        462MiB              1.6GiB          Mar 19 2022 - 10:36:14
ars_peer_poland          00.000.000.00:00000        10.6.0.4        500MiB              5.1GiB          Mar 19 2022 - 09:28:34
primary                  (none)                     10.6.0.5        0B                  0B              (not yet)
mobile                   (none)                     10.6.0.6        0B                  0B              (not yet)
grig_mobile              00.000.000.00:00000        10.6.0.7        114MiB              2.1GiB          Mar 19 2022 - 10:37:18
neongm_laptop            00.000.000.00:00000        10.6.0.8        37MiB               127MiB          Mar 19 2022 - 10:35:34
grig_desktop             (none)                     10.6.0.9        0B                  0B              (not yet)"""
    sc = statsCollector(output.decode('utf-8'))
    sc.process_data()

    context = {
        'title': 'wireguard vps server',
        'uptimeDays': round(uptime()/(3600*24), 2),
        'uptimeHours': round(uptime()/3600, 2),
        'uptimeSeconds': round(uptime(), 2),
        'peerCount': sc.get_peer_count(),
        'activePeerCount': sc.get_active_peer_count(),
        'receivedTraffic': round(sc.get_received_traffic(), 2),
        'sentTraffic': round(sc.get_sent_traffic(), 2),
        'fullTraffic': round(sc.get_full_traffic(), 2),
    }
    return render(req, 'index.html', context)


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