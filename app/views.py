from django.shortcuts import render
from uptime import uptime
import subprocess
import re
from random import choice
from datetime import datetime
# Create your views here.

class userStats():
    def __init__(self, user_data_arr):
        self.data = user_data_arr
        self.traffic_sent = self.get_traffic_sent()

    def _read_traffic_at_index(self, index):
        if '0B' in self.data[index]: return 0
        if 'GiB'in self.data[index]: return float(self.data[index].replace('GiB', ''))
        if 'MiB'in self.data[index]: return float(self.data[index].replace('MiB', ''))/1024
        assert False, f"method _read_traffic_at_index() didn't find the traffic data at index {index} in self.data, got {self.data[index]}\nself.data = {self.data}"
    
    def get_traffic_sent(self): #id of bytes sent is 4, received 3
        return self._read_traffic_at_index(4)
    
    def get_traffic_received(self):
        return self._read_traffic_at_index(3)

    def get_traffic_full(self):
        return self.get_traffic_sent() + self.get_traffic_received()

    def get_user_name(self):
        return self.data[0]

    def get_virtual_ip(self):
        return self.data[2]

    def get_last_use_date(self):
        if len(self.data) <= 7: return "Never"
        return f"{self.data[5]} {self.data[6]} {self.data[7]}"

    def used_at_least_once(self):
        if self.get_traffic_received() == 0: return False
        return True

    def is_active(self): # very bad implementataion, hope it at least works TODO fix is_active
        date_string = self.data[6] 
        if not date_string.isdigit() : return False
        else: user_date = int(date_string)
        if date_string.isdigit(): 
            current_date = datetime.now().day
            if current_date - user_date <= 1: return True
            return False

    @staticmethod
    def is_valid(user_data_arr):
        if (len(user_data_arr) < 4): return False
        if "10.6.0" in user_data_arr[2]: return True


class statsCollector():
    def __init__(self, data = []):
        self.raw_data = data
        self.data = []
        self.traffic_received = 0
        self.traffic_sent = 0
        self.per_user_stats = []
        self._process_per_user_stats()

    def _process_per_user_stats(self):
        data_array = self.raw_data.split('\n')
        self.data = [user_data.split() for user_data in data_array]
        self.per_user_stats = [userStats(user_data) for user_data in self.data if userStats.is_valid(user_data)]

    def get_received_traffic(self):
        return sum([user_data.get_traffic_received() for user_data in self.per_user_stats])

    def get_sent_traffic(self):
        return sum([user_data.get_traffic_sent() for user_data in self.per_user_stats])

    def get_full_traffic(self):
        return self.get_sent_traffic() + self.get_received_traffic()

    def get_peer_count(self):
        return len(self.per_user_stats)
    
    def get_active_peer_count(self):
        return len([' ' for user_data in self.per_user_stats if user_data.used_at_least_once()])
    
    def get_peers_used_recently_count(self):
        return len([' ' for user_data in self.per_user_stats if user_data.is_active()])

    def get_per_user_stats(self): return self.per_user_stats 


def index(req):
    catMessages = ["have a good day", "rusk rusk rusk rusk", "the table", "how does it work", "boo", "you're awesome", "code works", "you're secure", "furfur", "meow", "yes, the кот"]
    # getting data
    p = subprocess.Popen(["pivpn -c"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    
    # proccessing data
    TESTING_STATS = """Name                     Remote IP                  Virtual IP      Bytes Received      Bytes Sent      Last Seen
neongm_main_desktop      00.000.000.00:00000        10.6.0.2        211MiB              1.7GiB          Mar 22 2022 - 12:19:22
neongm_android_1         00.000.000.00:00000        10.6.0.3        462MiB              1.6GiB          Mar 21 2022 - 10:36:14
ars_peer_poland          00.000.000.00:00000        10.6.0.4        500MiB              5.1GiB          Mar 19 2022 - 09:28:34
primary                  (none)                     10.6.0.5        0B                  0B              (not yet)
mobile                   (none)                     10.6.0.6        0B                  0B              (not yet)
grig_mobile              00.000.000.00:00000        10.6.0.7        114MiB              2.1GiB          Mar 19 2022 - 10:37:18
neongm_laptop            00.000.000.00:00000        10.6.0.8        37MiB               127MiB          Mar 19 2022 - 10:35:34
grig_desktop             (none)                     10.6.0.9        0B                  0B              (not yet)
: somethin something :"""
    #sc = statsCollector(output.decode('utf-8'))
    sc = statsCollector(TESTING_STATS)
    per_user_stats = sc.get_per_user_stats()


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