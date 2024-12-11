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


class Symbols(models.Model):
    symbol = models.CharField(max_length=200)
    status = models.CharField(max_length=100,default='1')
    class Meta:
        db_table = 'symbols'

class PortfolioSettings(models.Model):
    interval = models.CharField(max_length=100)
    symbol = models.CharField(max_length = 100)
    indicators = models.TextField()
    class Meta:
        db_table = 'portfolio_settings'


class OverView(models.Model):
    net_profit = models.CharField(max_length=200)
    total_closed_trades = models.CharField(max_length=200)
    percent_profitable = models.CharField(max_length=200)
    profit_factor = models.CharField(max_length=200)
    max_dropdown = models.CharField(max_length=200)
    avg_trades = models.CharField(max_length=200)
    gross_profit = models.CharField(max_length=200)
    gross_loss = models.CharField(max_length=200)
    buy_hold = models.CharField(max_length=200)
    avg_winning_trades = models.CharField(max_length=200)
    avg_lossing_trades = models.CharField(max_length=200)
    total_open_trades = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    class Meta:
        db_table = 'overview'


        
