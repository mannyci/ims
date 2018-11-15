from celery.decorators import task
from .models import Host

import os

@task(bind=True)
def debug_task(self):
    hosts = Host.objects.all()
    for host in hosts:
        ret = os.system("ping -c 1 %s" % host.ip)
        if ret != 0:
            print "%s is alive" % host
        else:
            print "%s is dead" % host
