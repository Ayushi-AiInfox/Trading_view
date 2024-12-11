from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
import jwt
from django.contrib import messages
from django.conf import settings
from accounts.models import User  
import yfinance as yf
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from datetime import datetime

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()



KEYS = getattr(settings, "KEY", None)
def AdminDashboardView(request):
    if request.session.has_key('token'):
        message = request.session.get('message')
        message1 = request.session.get('message1')
        try:
            del request.session['message']
        except:
            pass
        try:
            del request.session['message1']
        except:
            pass
        token = request.session.get('token')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr = User.objects.get(email = d.get("email"))
            if d.get('method')!="verified" or usr.role!='admin':
                return redirect('../../accounts/login')
        except:
            return redirect('../../accounts/login')
        ticker = "AAPL"
        data = yf.download(ticker, start="2023-01-01", end="2024-12-11", interval="1d")
        data = data.drop(columns=('Adj Close',ticker))
        data.columns = [col[0] for col in data.columns]
        bt = Backtest(data, SmaCross, commission=.002,
              exclusive_orders=True,cash=10000000)
        stats = bt.run()    
        d= dict(stats)      
        trades_data = d.get('_trades')
        trades_data = trades_data.to_dict(orient="records")
        return render(request,'admin_dashboard.html',{'message':message,'message1':message1,"user":usr,"trades_data":trades_data,"d":d})
    else:
        return redirect('../../accounts/login')
    

