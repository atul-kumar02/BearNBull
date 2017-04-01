import urllib.request
import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


import tkinter as tk
from tkinter import ttk


style.use('ggplot')
def StockPulling(StockToPull):
    
      u="http://chartapi.finance.yahoo.com/instrument/1.0/ "+StockToPull+ "/chartdata;type=quote;range=1y/csv"    
      x=urllib.request.urlopen(u)
      charset=x.info().get_content_charset()
      content=x.read().decode(charset)
      dayStock=content.split('\n')
      c.execute("SELECT COUNT(Date) FROM "+stockToPull)
      date=c.fetchall()
      date1=date[0]
      print(date,date1[0])
      if  date1[0]!= 0:
          c.execute("SELECT MAX(Date) FROM "+stockToPull)
          date=c.fetchall()
          date1=date[0]
      maxDate=date1[0]
      print(maxDate)


      print(len(dayStock))
      
      for day in dayStock:
           dayl=day.split(',')
           if len(dayl)==  6:
               if 'close' not in dayl:
                   
                   if(int(dayl[0])>int(maxDate)):
                       #print(dayl[0])
                  
                       command="INSERT INTO " +stockToPull+" VALUES("+str(dayl[0])+","+str(dayl[1])+","+str(dayl[2])+","+str(dayl[3])+","+str(dayl[4])+","+str(dayl[5])+")"
                       c.execute(command)
                       


    
def graph_plot(c,stockToPull):
      
      dates=[]
      close=[]
      c.execute('SELECT Date,close FROM '+stockToPull)
      for row in c.fetchall():
            s_datetime = datetime.datetime.strptime(row[0], '%Y%m%d')
            dates.append(s_datetime)
            close.append(row[1])
      plt.plot_date(dates,close,'-')
      
      

conn = sqlite3.connect('StockData.db')
stock=['YHOO','GOOG','TSLA']
c=conn.cursor()
for stockToPull in stock:
      co='CREATE TABLE IF NOT EXISTS '+stockToPull+' (Date TEXT,close INT,high INT,low INT,open INT,volume INT)'
      c.execute(co)
      StockPulling(stockToPull)

      conn.commit()
for stockToPull in stock:
      
      graph_plot(c,stockToPull)
plt.show()
c.close()
