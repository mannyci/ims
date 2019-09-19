from celery.decorators import task
from .models import Networks
from netaddr import *
from ipaddress import IPv4Address, IPv4Network

@task(bind=True)
def update_network(self, network=None):
    networks = Networks.objects.all()
    for network in networks:
        net = IPv4Network('{0}/{1}'.format(network.ip, network.prefix))
        network.size = net.num_addresses
        network.subnet_mask = str(net.netmask)
        net.compare_networks
        network.save()
        
