#import matplotlib as m
import csv
import os 
#import matplotlib.pyplot as plt
#import numpy as np
from datetime import date

s=50
#short term average (days)

l=200
#long term average (days)

i=0
temp=[]
ali=[]



#os.system("wget http://ichart.yahoo.com/table.csv?s=SPY&a=0&b=1&c=1994&d=0&e=31&f=2014&g=d -O dailySPY.csv")

with open('dailySPY.csv') as csvfile:
     alireader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for line in alireader:
       i=i+1
       if i>1:
         for j in range(1,len(line)) :
          line[j]=float(line[j])
         ali.append(line)
       else:
        ali.append(line)
del ali[0]
data=[0]*len(ali)

for i in range(0,len(ali)): # range(0,n) is from 0 to n-1 NOT n!!!
	data[i]=ali[len(ali)-i-1]
i=0
for j in range(101,111):
	i=i+data[j][4]
	


def SMA(howmanyday, whatday, data): # howmanyday simple moving average at whatday using only closing prices at each day
	SMA=0
	for x in range(whatday-howmanyday+1,whatday+1):
		SMA=SMA+data[x][4]   #using only closing prices
	return SMA/howmanyday


shortSMA=[0]*(len(ali))    #s for small value of howmanyday 
longSMA=[0]*(len(ali))   #l for large value of howmanyday


i=s+1                                    
for i in range(s+1, len(ali)):
	shortSMA[i]=SMA(s,i,data)
i=l+1
for i in range(l+1, len(ali)):
   longSMA[i]=SMA(l,i,data)

   
#npdata = np.array(data)[:,4]
#price = list(npdata.astype(np.float))

#Date,Open,High,Low,Close,Volume,Adj', 'Close']       



##################################
### PLOTTING
##################################

#
#fig = plt.figure()
#ax1 = fig.add_subplot(121)
#
### the data
#x = np.array(range(len(ali)))
#y1 = np.array(shortSMA)
#y2 = np.array(longSMA)
#y33 = np.array(data)[:,4]
#y3 = y33.astype(np.float)
#
### left panel
#ax1.scatter(x,y1,color='green',s=5,edgecolor='none')
#ax1.set_aspect(1./ax1.get_data_ratio()) # make axes square
#ax1.scatter(x,y2,color='red',s=5,edgecolor='none')
#ax1.scatter(x,y3,color='blue',s=5,edgecolor='none')
#plt.show()
 
##################################
### TESTING
##################################

#
#holding_stock = 0
#balance = 0
#last_bought_price = 0
#
##find first bullish crossing
#new_crossing = 0
#finished = 0
#   
#
#while(shortSMA[l] > longSMA[l]):
#  new_crossing = 0;
#while not finished:
#
#for t in range(len(ali)):   # shouldnt  be data instead of ali ????????
#  if t>l:
#   if((shortSMA[t] > longSMA[t]) & holding_stock==0):
#     holding_stock = 1
#     last_bought_price = price[t]
#     balance = balance - last_bought_price
#   if((shortSMA[t] < longSMA[t]) & holding_stock==1):
#     holding_stock = 0
#     last_bought_price = 0
#     balance = balance + price[t]
#
#print balance

########################################
######Ali 
########################################
MAdifference=[0]*len(data)
for t in range(l+1,len(data)):
	MAdifference[t]=-longSMA[t]+shortSMA[t] 
# if prices long ago were low and short term trend is going down breaks below the long term average then you should sell vice versa if long agoprices were higher than recently and short term is going back up again above the long term average is a good opportunity to buy...so everytime MAdifference becomes positive it's a buy and vice versa 	

#if MAdifferece[l+1]<0 :
# FirstCrossAction='Buy'
#else
# FirstCrossAction='NotBuy'

cross_t=l+1
MAcrossing=[]
for t in range(l+1,len(data)):
  if (MAdifference[t]>0  and MAdifference[cross_t]<0 ):
	MAcrossing.append([t,date.fromordinal(t),'buy',data[t][4]])
#date.fromordinal(t=number of days from date 0,0,0) gives the year, month and day
	cross_t=t     
  if (MAdifference[t]<0 and  MAdifference[cross_t]>0):
	MAcrossing.append([t,date.fromordinal(t),'sell',data[t][4]])
      	cross_t=t

if MAdifference[l+1]>0 : del MAcrossing[0] # we dont need the FirstCrossAction='sell'

#print MAcrossing
#print len(MAcrossing)

####################################################
### Analyzig wins and losses and net profit per share
####################################################
i=0
win, loss, wintrades,losstrades,profit,trades=0,0,0,0,0,0

for i in range(0,(len(MAcrossing)/2)*2,2):
# dividing by two is to remove a single 'buy' at the end that's not followed up by a 'sell'
#I could use the last price of the data as a sell to complete a trade but that's a bit cheating	
	if MAcrossing[i+1][3]-MAcrossing[i][3]>0:
		win=win+ MAcrossing[i+1][3]-MAcrossing[i][3]
		wintrades=wintrades+1
	else:
		loss=loss+MAcrossing[i+1][3]-MAcrossing[i][3]
		losstrades=losstrades+1
profit=win+loss
trades=wintrades+losstrades
#print "for shortterm and longterm=",s,"and",l,"days:"
#print "win=", win,", loss=", loss,", wintrades=",wintrades,",losstrades=",losstrades,",profit=",profit,",trades=",trades


#####################################################################
####### Analysis for different combinations of s & l
#####################################################################
strategy=[]

for s in range(5,51,5):
	for l in range (20,201,20):
		i=s+1                                    
		for i in range(s+1, len(ali)):
			shortSMA[i]=SMA(s,i,data)
		i=l+1
		for i in range(l+1, len(ali)):
		        longSMA[i]=SMA(l,i,data)
	

		MAdifference=[0]*len(data)
                for t in range(l+1,len(data)):
                	MAdifference[t]=-longSMA[t]+shortSMA[t] 
                
                cross_t=l+1
                MAcrossing=[]
                for t in range(l+1,len(data)):
                  if (MAdifference[t]>0  and MAdifference[cross_t]<0 ):
                	MAcrossing.append([t,date.fromordinal(t),'buy',data[t][4]])
                	cross_t=t     
                  if (MAdifference[t]<0 and  MAdifference[cross_t]>0):
                	MAcrossing.append([t,date.fromordinal(t),'sell',data[t][4]])
                      	cross_t=t
                
                if MAdifference[l+1]>0 : del MAcrossing[0]
		
		i=0
                win, loss, wintrades,losstrades,profit,trades=0,0,0,0,0,0
                
                for i in range(0,(len(MAcrossing)/2)*2,2):
                	if MAcrossing[i+1][3]-MAcrossing[i][3]>0:
                		win=win+ MAcrossing[i+1][3]-MAcrossing[i][3]
                		wintrades=wintrades+1
                	else:
                		loss=loss+MAcrossing[i+1][3]-MAcrossing[i][3]
                		losstrades=losstrades+1
                profit=win+loss
                trades=wintrades+losstrades
               # print "for shortterm and longterm=",s,"and",l,"days:"
               # print "win=", win,", loss=", loss,", wintrades=",wintrades,",losstrades=",losstrades,",profit=",profit,",trades=",trades
		
		if (win!=0 and trades!=0): 
 			strategy.append(["s,l=%d, %d"%(s,l),round(profit),win*100//(win-loss), wintrades*100//trades,wintrades-losstrades])


i,j=0,0
for i in range(0,len(strategy)):
	for j in range(0,len(strategy)):
		if strategy[j][1]>strategy[i][1]:
			temp=strategy[i]
			strategy[i]=strategy[j]
			strategy[j]=temp 
print strategy
