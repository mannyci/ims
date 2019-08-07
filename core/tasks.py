from celery.decorators import task
from .models import Host, HostStatus, HostFacts

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
    try:
        instance = HostStatus.objects.get(host_id=hostid)
    except:
        host = Host.objects.get(id=hostid)
        instance = HostStatus(host=host)
    if instance.status != ret:
        instance.status = ret
        instance.save()
        return ("%s changed status to %s" % (instance.host, ret))
    else:
        return "Complete"

@task(bind=True)
def host_facts(self):
    hosts = Host.objects.all()
    for host in hosts:
        fact = os.popen("ping -c 1 %s" % host.ip).read()
        tid=host_facts.request.id
        host_f = HostFacts(id=tid, facts=fact)
        host_f.save()
        host.facts.add(host_f)
