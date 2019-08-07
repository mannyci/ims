# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.utils import timezone
from django.db import models
from account.models import Account


class Environment(models.Model):
    class Meta:
        db_table = 'environments'

    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=50, null=True)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Hostgroup(models.Model):
    class Meta:
        db_table = 'hostgroups'

    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=50, null=True)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HostStatus(models.Model):
    class Meta:
        db_table = 'hoststatus'

    host = models.OneToOneField('Host', on_delete=models.CASCADE)
    status = models.BooleanField(default=False, verbose_name='Host is rechable')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.status is 0:
            return 'Dead'
        else:
            return 'Active'


class Host(models.Model):
    class Meta:
        db_table = 'hosts'

    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Hostgroup)
    facts = models.ManyToManyField('HostFacts')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ui:updatehost", kwargs={"id": self.id})

    def get_env_url(self):
        return reverse("ui:updateenv", kwargs={"id": self.environment.id})

class HostFacts(models.Model):
    class Meta:
        db_table = 'host_facts'
    
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    facts = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.created_at = timezone.now()
        return super(HostFacts, self).save(*args, **kwargs)