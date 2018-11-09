# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
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


class Host(models.Model):
    class Meta:
        db_table = 'hosts'

    name = models.CharField(max_length=40, unique=True)
    ip = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Hostgroup)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ui:updatehost", kwargs={"name": self.name})

    def get_env_url(self):
        return reverse("ui:updateenv", kwargs={"id": self.environment.id})
