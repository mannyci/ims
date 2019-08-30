from django.db import models

class Subnet(models.Model):
    class Meta:
      db_table = 'subnet'

  name = models.CharField(max_length=40, unique=True)
  cidr = models.GenericIPAddressField