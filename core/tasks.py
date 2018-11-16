from celery.decorators import task
from .models import Host

import os


@task(bind=True)
def host_status(self):
    hosts = Host.objects.all()
    active = 0
    dead = 0
    for host in hosts:
        ret = os.system("ping -c 1 %s" % host.ip)
        if ret != 0:
            dead += 1
            if host.active == True:
                host.active = False
                host.save()
        else:
            active += 1
            if host.active == False:
                host.active = True
                host.save()
    return ("Completed host status check, active: %s dead: %s" % (active, dead))
