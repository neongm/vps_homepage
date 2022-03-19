from django.shortcuts import render
from uptime import uptime
# Create your views here.

def index(req):
    context = {
        'title': 'wireguard vps server',
        'uptimeDays': round(uptime()/(3600*24), 2),
        'uptimeHours': round(uptime()/3600, 2),
        'uptimeSeconds': round(uptime(), 2)
    }
    return render(req, 'index.html', context)