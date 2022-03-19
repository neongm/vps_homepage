from django.shortcuts import render
from uptime import uptime
import subprocess
import re
# Create your views here.


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
        self.raw_data = []
        self.data = []
    
    def process_data(self, data):
        if data: data_array = data.split('\n')
        else: data_array = self.data.split('\n')

        data = [user_data.split() for user_data in data_array]
        for d in data: print(d)



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