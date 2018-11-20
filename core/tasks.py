from celery.decorators import task
from .models import Host, HostStatus

import os


@task(bind=True)
def host_status(self):
    hosts = Host.objects.all()
    active = 0
    dead = 0
    for host in hosts:
        ret = os.system("ping -c 1 %s >/dev/null" % host.ip)
        if ret != 0:
            dead += 1
            status = False
        else:
            active += 1
            status = True
        update_host_status.delay(host.id, status)
    return ("Completed host status check, active: %s dead: %s" % (active, dead))


@task(ignore_results=True)
def update_host_status(hostid, ret):
    instance = HostStatus.objects.get(host_id=hostid)
    instance.status = ret
    instance.save()
