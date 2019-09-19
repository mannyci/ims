from django.db import models
from django.urls import reverse
from netaddr import *
from account.models import Account
from django.core.validators import MaxValueValidator,MinValueValidator

class Networks(models.Model):
  class Meta:
    db_table = 'networks'

  name = models.CharField(blank=True, null=True, unique=True, max_length=255)
  description = models.CharField(blank=True, null=True, unique=False, max_length=255)
  ip = models.GenericIPAddressField(blank=False, null=False, unique=True, protocol="IPv4")
  prefix = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(5), MaxValueValidator(30)])
  added_by = models.ForeignKey(Account, on_delete=models.CASCADE)
  subnet_mask = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
  size = models.IntegerField(blank=True, null=True)

  def __str__(self):
    return ' - '.join([self.name, self.ip])

  def get_absolute_url(self):
    return reverse("ui:networkupdate", kwargs={"id": self.id})