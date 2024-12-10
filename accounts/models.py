from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid

import json

class User(AbstractUser):
    email=models.EmailField(unique=True)
    verified_at = models.CharField(max_length=200,default='False')
    role =models.CharField(max_length=200,default='user')
    status = models.CharField(max_length=20, default='1')
    updated_at = models.CharField(max_length=200,default=datetime.utcnow())
    created_at = models.CharField(max_length=200,default=datetime.utcnow())
    remember_token=models.CharField(max_length=200,default='False')
    phone_no=models.CharField(max_length=200,null=True)
    activation_date=models.CharField(max_length=200,default='N/A')
    class Meta:
        db_table='users'
        
