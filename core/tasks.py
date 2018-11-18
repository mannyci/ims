from celery.decorators import task
from .models import Host

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
            if host.active is True:
                host.active = False
        else:
            active += 1
            if host.active is False:
                host.active = True
        update_host_status.delay(host.id, host.active)
    return ("Completed host status check, active: %s dead: %s" % (active, dead))


@task(ignore_results=True)
def update_host_status(host, status):
    instance = Host.objects.get(id=host)
    if instance.active == status:
        return ("Status of %s is %s" % (instance, status))
    else:
        instance.active = status
        instance.save()
        return ("Status of %s changed to %s" % (instance, status))
