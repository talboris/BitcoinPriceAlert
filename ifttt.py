#Bitcoin price alert app, using the IFTTT service and telegram
#Needed to install IFTTT and Telegram , can be mobile or desktop , in this example name of IFTTT event is 'btc' 


import requests
import time
from datetime import datetime


btc_api = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'  #coinmarketcap API for getting BTC price
iftt_hook = 'https://maker.ifttt.com/trigger/{}/with/key/cNwB-4Yv_vnFXu4bwT5E4z' #IFTTT API for triggering the IFTTT app
			
#function to get the btc price
def btc_price():
	response = requests.get(btc_api) #sending GET to CC
	response = response.json() #converting to json format
	btc = response[0]['price_usd']
	return float(btc) # return the btc price
	
		
#function that receives the trigger name and value to add to data in IFTTT, then the function send POST that triggers the IFTTT		
def post_ifft(event,value):
	iftt = iftt_hook.format(event) #adding event name to the URI
	data ={'value1': value}
	requests.post(iftt, json=data) # sending POST for webhooks in IFTTT app
	
	
#function to format nicely data for the telegram output as telegram can work with several html tags	
def hist(bitcoin_history):
	rows = []
	for x in bitcoin_history:
		date = x['date'].strftime('%d.%m.%Y %H:%M') 
		
		price = x['price']
		row = '{}: $<b>{}<b/>'.format(date, price)  
		rows.append(row)
		
	return '<br>'.join(rows) #returning rows with \r\n for the convinience
	
	
	

def main():
	
	bitcoin_history = [] #define new list
	
	while True:
		btc_new_price = btc_price() #get the BTC price
		date = datetime.now()
		bitcoin_history.append({'date': date, 'price': btc_new_price}) #populate btc history with date and price
		print(bitcoin_history)
		if len(bitcoin_history)>4: # i want to accumulate history of 5 btc prices and send it to my telegram only when btc price higher than 8K
			if btc_new_price > 8000:
				print("sending to IFTTT\n\n\n")
				post_ifft('btc', hist(bitcoin_history)) #using btc ticker since this trigger string for my IFTTT app and history sent as value to give more info
				bitcoin_history=[] #cleaning BTC history stack as i iam interested only in 5 rows
		
		time.sleep(2) # wait func not to spam the COINCAPMARKET API
	
	
if __name__ == '__main__':
	main()
