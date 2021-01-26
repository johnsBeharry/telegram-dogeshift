import requests
import time
from block_io import BlockIo
import os

token = os.environ['TELEGRAM_BOT_TOKEN'] #Telegram bot token
url = "https://api.telegram.org/bot%s/" %(token)
n = 0
version = 2
block_io = BlockIo(os.environ['BLOCKIO_API_KEY'], os.environ['BLOCKIO_PIN'], version)
active_users = {}

monikers_tuple  = [
	("sandwich","sandwiches",21),
	("coffee", "coffees",7),
	("tea", "teas",5),
	("lunch", "lunches",49)
]
monikers_dict = {n[i]: n[2] for n in monikers_tuple for i in range(2)}
monikers_flat = [monikers_tuple[i][j] for i in range(len(monikers_tuple)) for j in range(3)]
monikers_str  = '\n'.join(f"{i[0]}: {i[2]} doge" for i in monikers_tuple)

def getCount(chatid):
	n = []
	t = time.time()
	chat_users = active_users[chatid]
	for i in chat_users:
		if t - chat_users[i] <= 600:
			n.append(i)
	return n

def sendMsg(message,chatid):
	requests.get(url + "sendMessage", data={"chat_id":chatid,"text":message})

def returnBal(username):
	data = block_io.get_address_balance(labels=username)
	balance = data['data']['balances'][0]['available_balance']
	pending_balance = data['data']['balances'][0]['pending_received_balance']
	return (balance, pending_balance)

def process(message,firstname,username,chatid):
	message = message.split(" ")
	for i in range(message.count(' ')):
		message.remove(' ')

# /start
	if "/start" in message[0]:
		try:
			sendMsg(str(username)+" welcome. I'm the the Peak Shift @ Work Bot\n\nHere's how it works.\n\nYou can use @dogeshift_bot by messaging it directly or in a group that it is a part of.\n\nAvailable Commands\n\n/register - Registers your username with the bot\n/tip @username 10 doge - use this to tip some doge from your balance to another user\n/address - Get your deposit address\n/withdraw 100 <address> - to withdraw your balance",chatid)
		except Exception as e:
			print("Error : 50 : "+str(e))
# /help
	elif "/help" in message[0]:
		try:
			sendMsg(str(username)+" welcome. I'm the the Peak Shift @ Work Bot\n\nHere's how it works.\n\nYou can use @dogeshift_bot by messaging it directly or in a group that it is a part of.\n\nAvailable Commands\n\n/register - Registers your username with the bot\n/tip @username 10 doge - use this to tip some doge from your balance to another user\n/address - Get your deposit address\n/withdraw 100 <address> - to withdraw your balance",chatid)
		except Exception as e:
			print("Error : 55 : "+str(e))
# /register
	elif "/register" in message[0]:
		try:
			block_io.get_new_address(label=username)
			sendMsg("@"+username+" you are now registered.",chatid)
		except:
			sendMsg("@"+username+" you are already registered.",chatid)
# /balance
	elif "/balance" in message[0]:
		try:
			(balance, pending_balance) = returnBal(username)
			sendMsg("@"+username+" Balance : "+balance+ "Doge ("+pending_balance+" Doge)",chatid)
		except:
			sendMsg("@"+username+" you are not registered yet. use /register to register.",chatid)
# /tip
	elif "/tip" in message[0]:
		try:
			person = message[1].replace('@','')
			amount_msg = 1 if message[2] in ('a', 'an', '1') else message[2]
			amount = abs(float(amount_msg)) * monikers_dict.get(message[3], 1)

			if monikers_dict.get(message[3], 0) == 0:
				sin_plu = "doge"
			elif amount_msg == 1:
				sin_plu = monikers_tuple[monikers_flat.index(message[3])//3][0]
			else:
				sin_plu = monikers_tuple[monikers_flat.index(message[3])//3][1]

			block_io.withdraw_from_labels(amounts=str(amount), from_labels=username, to_labels=person)
			sendMsg("@"+username+" tipped "+ str(amount_msg) + " " + sin_plu +
					("" if monikers_dict.get(message[3], 0) == 0 else f" ({str(amount)} doge)") +
					" to @"+person+"",chatid)
			(balance, pending_balance) = returnBal(person)
			sendMsg("@"+person+" Balance : "+balance+ "Doge ("+pending_balance+" Doge)",chatid)
		except ValueError:
			sendMsg("@"+username+" invalid amount.",chatid)
		except:
			sendMsg("@"+username+" insufficient balance or @"+person+" is not registered yet.",chatid)
# /address
	elif "/address" in message[0]:
		try:
			data = block_io.get_address_by_label(label=username)
			sendMsg("@"+username+" your address is "+data['data']['address']+"",chatid)
		except:
			sendMsg("@"+username+" you are not registered yet. use /register to register.",chatid)
# /withdraw
	elif "/withdraw" in message[0]:
		try:
			amount = abs(float(message[1]))
			address = message[2]
			data = block_io.withdraw_from_labels(amounts=str(amount), from_labels=username, to_addresses=address)
		except ValueError:
			sendMsg("@"+username+" invalid amount.",chatid)
		except:
			sendMsg("@"+username+" insufficient balance or you are not registered yet.",chatid)
# /rain
	elif "/rain" in message[0]:
		try:
			users = getCount(chatid)
			if username in users:
				users.remove(username)
			number = len(users)

			amount = ("10," * (number - 1)) + '10'
			name = username
			username = ((username+',') * (number - 1)) + username
			if number < 2:
				sendMsg("@"+username+" less than 2 shibes are active.",chatid)
			else:
				print(amount)
				print(username)
				block_io.withdraw_from_labels(amounts=amount, from_labels=username, to_labels=','.join(users))
				sendMsg("@"+name+" is raining on "+','.join(users)+"",chatid)
		except:
			pass
# /monikers
	elif "/monikers" in message:
		sendMsg("--MONIKERS--\n" +
			monikers_str,chatid)

	elif "/active" in message:
		sendMsg("Current active : %d shibes" %(len(getCount(chatid))),chatid)
	else:
		global active_users
		try:
			active_users[chatid][username] = time.time()
		except KeyError:
			active_users[chatid] = {}
			active_users[chatid][username] = time.time()

while True:
	try:
		print("such dogeshift. much running. ",time.time())
		data = requests.get(url+"getUpdates", data={"offset":n}).json()
		#print(data)
		#print(" \n ")
		n = data["result"][0]["update_id"] + 1
		try:
			username = data["result"][0]["message"]["from"]["username"]
		except:
			username = "UnKnown uname"
		try:
			firstname = data["result"][0]["message"]["from"]["first_name"]
		except Exception as e:
			print(e)
			firstname = "Unknown name"
		chatid = data["result"][0]["message"]["chat"]["id"]
		message = data["result"][0]["message"]["text"]
		process(message,firstname,username,chatid)
	except Exception as e:
		#print("Error : 141 : "+str(e))
		pass
