from celery.decorators import task
from .models import Host

import os


@task(bind=True)
def debug_task(self):
    hosts = Host.objects.all()
    active = 0
    dead = 0
    for host in hosts:
        ret = os.system("ping -c 1 %s" % host.ip)
        if ret != 0:
            dead += 1
            host.status = False
        else:
            active += 1
            host.status = True
        host.save()
    return ("Completed host status check, active: %s dead: %s" % (active, dead))
