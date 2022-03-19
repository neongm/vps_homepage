from django.shortcuts import render
from uptime import uptime
import subprocess
import re
from random import choice
# Create your views here.


class statsCollector():
    def __init__(self, data = []):
        self.data = data
        self.traffic_received = 0
        self.traffic_sent = 0
    
    def process_data(self, data = []):
        if len(self.data): data_array = self.data.split('\n')
        else: data_array = data.split('\n')
        self.data = [user_data.split() for user_data in data_array][2:-2:]
        
    
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
    catMessages = ["have a good day", "rusk rusk rusk rusk", "the table", "how does it work", "boo", "you're awesome", "code works", "you're secure", "furfur", "meow"]
    # getting data
    p = subprocess.Popen(["pivpn -c"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    
    # proccessing data
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
        'catSays': choice(catMessages)
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