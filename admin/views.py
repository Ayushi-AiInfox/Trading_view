from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
import jwt
from django.contrib import messages
from django.conf import settings
from accounts.models import * 
import yfinance as yf
import pandas as pd
import json
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


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

def symbol_list():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    sp500_data = pd.read_csv(url)
    sp500_symbols = sp500_data['Symbol'].tolist()
    valid_symbols = []
    for symbol in sp500_symbols:
        try:
            yf.Ticker(symbol) 
            valid_symbols.append(symbol)
        except Exception as e:
            print(f"Invalid symbol: {symbol}, Error: {e}")
    return valid_symbols 



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
        portfolio_data = PortfolioSettings.objects.all()[0]
        ticker = portfolio_data.symbol
        interval_data  = portfolio_data.interval

        if interval_data == '1':
            interval_data='1m'
        elif interval_data == '2':
            interval_data = '2m'
        elif interval_data == '3':
            interval_data = '3m'
        elif interval_data == '5':
            interval_data = '5m'
        elif interval_data == '10':
            interval_data ='10m'
        elif interval_data == '15':
            interval_data = '15m'
        elif interval_data == '30':
            interval_data = '30m'
        elif interval_data =='60':
            interval_data  = '1h'
        elif interval_data == '120':
            interval_data = '2h'
        elif interval_data == '240':
            interval_data = '4h'
        elif interval_data == '1140':
            interval_data = '1d'
        current_datetime = datetime.now()
        val = 58
        if interval_data == '1d' or interval_data == '1h' or interval_data == '2h' or interval_data=='4h':
            val=500
        date_before_59_days = current_datetime - timedelta(days=val)
        date_format = "%Y-%m-%d"
        
        previous_date = current_datetime - timedelta(days=1)
        previous_date  = previous_date.strftime(date_format)
        date_before_59_days_formatted = date_before_59_days.strftime(date_format)
        print(interval_data)

        data = yf.download(ticker, start=date_before_59_days, end=previous_date, interval=interval_data)
        print(data)
        data = data.drop(columns=('Adj Close',ticker))
        data.columns = [col[0] for col in data.columns]
        bt = Backtest(data, SmaCross, commission=.000,
              exclusive_orders=True,cash=10000000)
        stats = bt.run()    
        d= dict(stats)      
        trades_data = d.get('_trades')
        trades_data = trades_data.to_dict(orient="records")
        data_dict = {}  
        data_dict['Return'] = d['Return [%]']
        data_dict['total_trades'] = d["# Trades"]
        data_dict['best_trades']= d['Best Trade [%]']
        data_dict['buy_hold_return']=d["Buy & Hold Return [%]"]
        data_dict['Max_dropdown'] = d['Max. Drawdown [%]']
        data_dict['win_rate'] = d["Win Rate [%]"]
        data_dict['max_dropdown_duration'] = d['Max. Drawdown Duration']
        data_dict['average_dropdown_duration']=d["Avg. Drawdown Duration"]
        data_dict['worst_trades'] = d["Worst Trade [%]"]
        data_dict['profit_factor'] = d["Profit Factor"]
        symbols = symbol_list()


        
            
        return render(
            request,'admin_dashboard.html',
        {'message':message,'message1':message1,
        "user":usr,"trades_data":trades_data,
        "data_dict":data_dict,"symbols":symbols,'portfolio':portfolio_data,
        "interval_data":interval_data
        })
    else:
        return redirect('../../accounts/login')

def SaveSymbol(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        symbol_name = data.get('symbol')
        print(symbol_name)
        if symbol_name:
            symbol = PortfolioSettings.objects.all()[0]
            symbol.symbol = symbol_name
            symbol.save()
            return JsonResponse({"success":True,"message":"Symbol Saved successfully"})
        return JsonResponse({'success': False, 'message': 'Invalid symbol name'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def saveInterval(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        interval_data = data.get('interval')
        if interval_data == '1m':
            interval_data = '1'
        elif interval_data == '2m':
            interval_data = '2'
        elif interval_data == '3m':
            interval_data = '3'
        elif interval_data == '5m':
            interval_data = '5'
        elif interval_data == '10m':
            interval_data ='10'
        elif interval_data == '15m':
            interval_data = '15'
        elif interval_data == '30m':
            interval_data = '30'
        elif interval_data == '1h':
            interval_data = '60'
        elif interval_data == '2h':
            interval_data = '120'
        elif interval_data == '4h':
            interval_data = '240'
        elif interval_data == '1d':
            interval_data = '1140'

        if interval_data:
            interval = PortfolioSettings.objects.all()[0]
            interval.interval = interval_data
            interval.save()
            return redirect('../../admin/dashboard')
        return JsonResponse({'success': False, 'message': 'Invalid interval name'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

    
  

