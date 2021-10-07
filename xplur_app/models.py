from django.db import models

# Create your models here.

import uuid
from django.contrib.auth.models import User
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=50, unique=False)
    phone = models.CharField(max_length=10, unique=True, null=False, blank=False)
    

def img_path(self, path):
    filename = '{}/img/{}'.format(self.id, path)
    return os.path.join(filename)


class MetaData(models.Model):
	small_icon = models.ImageField(blank=True, null=True, upload_to=img_path)
	large_icon  = models.ImageField(blank=True, null=True, upload_to=img_path)

class Product(models.Model):
  	sku = models.CharField(max_length=50, null=True, blank=True)
  	name = models.CharField(max_length=50, null=True, blank=True)
  	description = models.CharField(max_length=100, null=True, blank=True)
  	category = models.CharField(max_length=50, null=True, blank=True)
  	price = models.FloatField(blank=False, default=0)
  	metadata = models.ForeignKey(MetaData, on_delete=models.CASCADE,null=True,blank=True)



	#sridevi_n@quailty-matrix.com