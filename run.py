import datetime
import json
import math
import os
import requests
import time
from urllib.parse import urljoin
import traceback

from block_io import BlockIo
from github import Github
import yaml
from markdown_it import MarkdownIt


# Global constants
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TOKEN}/"


# Clients
BLOCKIO_API_KEY = os.environ['BLOCKIO_API_KEY']
BLOCKIO_PIN = os.environ['BLOCKIO_PIN']
VERSION = 2
block_io = BlockIo(BLOCKIO_API_KEY, BLOCKIO_PIN, VERSION)

GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
github_client = Github(GITHUB_ACCESS_TOKEN)


# Global objects
MD = MarkdownIt()
ACTIVE_USERS = {}

REPO_LABEL = 'peakshift/telegram-dogecoin'
REPO = github_client.get_repo(REPO_LABEL)



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
	chat_users = ACTIVE_USERS[chatid]
	for i in chat_users:
		if t - chat_users[i] <= 600:
			n.append(i)
	return n

def sendMsg(message, chatid, mode=None):
	# Prepare request data
	endpoint = urljoin(URL, "sendMessage")
	data = {
		"chat_id": chatid,
		"text": message,
		"parse_mode": mode
	}

	# Send GET request
	resp = requests.get(endpoint, data=data)
	success = (200 <= resp.status_code <= 299)
	if success:
		print(f"just sent a message to - {chatid}")
	else:
		print(f"failed to send message to - {chatid}: " +
			  f"({resp.status_code}: {resp.reason})")

	return None

def returnBal(username):
	data = block_io.get_address_balance(labels=username)
	balance = data['data']['balances'][0]['available_balance']
	pending_balance = data['data']['balances'][0]['pending_received_balance']
	return (balance, pending_balance)

def myconverter(o):
	if isinstance(o, datetime.date) or isinstance(o, datetime.datetime):
		return o.__str__()

def process(message, firstname, username, chatid):
	print(f"Received message: {message}")
	message = message.split(" ")
	for i in range(message.count(' ')):
		message.remove(' ')

	# /start
	if "/start" in message[0]:
		try:
			sendMsg("@" + str(username) + " welcome. I'm the the Peak Shift @ Work Bot\n\nHere's how it works.\n\nYou can use @dogeshift_bot by messaging it directly or in a group that it is a part of.\n\nAvailable Commands\n\n/register - Registers your username with the bot\n/tip @username 10 doge - use this to tip some doge from your balance to another user\n/address - Get your deposit address\n/withdraw 100 <address> - to withdraw your balance",chatid)
		except Exception as e:
			print("Error : 50 : "+str(e))

	# /help
	elif "/help" in message[0]:
		try:
			sendMsg("@" + str(username) + " welcome. I'm the the Peak Shift @ Work Bot\n\nHere's how it works.\n\nYou can use @dogeshift_bot by messaging it directly or in a group that it is a part of.\n\nAvailable Commands\n\n/register - Registers your username with the bot\n/tip @username 10 doge - use this to tip some doge from your balance to another user\n/address - Get your deposit address\n/withdraw 100 <address> - to withdraw your balance",chatid)
		except Exception as e:
			print("Error : 55 : "+str(e))

	# /register
	elif "/register" in message[0]:
		try:
			resp = block_io.get_new_address(label=username)
			addr = resp['data']['address']

			msg = f"@{username} you are now registered.\n" +\
				  f"Your Address : <code>{addr}</code>"

		except Exception as e:
			msg = f"@{username} you are already registered."

		try:
			sendMsg(msg, chatid)
		except Exception as e:
			pass

	# /work
	elif "/work" in message[0]:
		# Fetch issues with reward label
		open_reward_issues = \
			[issue for issue in REPO.get_issues()
				if "reward" in [label.name for label in issue.labels] ]

		# Parse reward issue yaml and return info
		msg = f"\n<b>{REPO_LABEL}</b>\n\n"
		for issue in open_reward_issues:
			# TODO: This assumes the yaml is right at the start
			#       of issue body. Explore making this more robust
			md_objs = MD.parse(issue.body)
			yaml_md_obj = None
			if md_objs:
				yaml_md_obj, *_ = md_objs

			if yaml_md_obj is not None:
				issue_yaml = yaml_md_obj.content
				issue_json = yaml.safe_load(issue_yaml)
				# issue_json_normalized = json.loads(json.dumps(issue_json, default=myconverter))
				msg += f"<code>" + \
					f"#{issue.number} > " + \
					f"{issue.title} -- " + \
					f"{issue_json['Reward']} 💰\n" + \
					f"</code>"

		msg += "\n\nUse /body_[issue_number] , Example : <code>/body_13</code>"

		sendMsg(msg, chatid, "html")

	# /body
	elif "/body" in message[0]:
		msg_str = ' '.join(message)
		issue_num_re = re.search(r'\d+', msg_str)
		if issue_num_re:
			issue_num_str = issue_num_re.group(0)
			issue_num = int(issue_num_str)

			issue = REPO.get_issue(number=issue_num)

			sendMsg(issue.body, chatid, "markdown")

		else:
			sendMsg("null", chatid)

	# /balance
	elif "/balance" in message[0]:
		try:
			balance, pending_balance = returnBal(username)
			bal = math.floor(float(balance))
			pending_bal = math.floor(float(pending_balance))

			msg = f"@{username}<b> " + \
				  f"Balance : </b>{bal} Doge \n" + \
				  f"(<b>Pending : </b>{pending_bal} Doge)"

			sendMsg(msg, chatid, "html")

		except Exception as e:
			print(e)
			msg = f"@{username} you are not registered yet. " + \
				  f"Use /register to register."

			sendMsg(msg, chatid)

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
			sendMsg("@"+person+" Balance : "+math.floor(balance)+ "Doge ("+math.floor(pending_balance)+" Doge)",chatid)
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

	# /active
	elif "/active" in message:
		sendMsg("Current active : %d shibes" %(len(getCount(chatid))),chatid)
	else:
		try:
			ACTIVE_USERS[chatid][username] = time.time()
		except KeyError:
			ACTIVE_USERS[chatid] = {}
			ACTIVE_USERS[chatid][username] = time.time()

print("-- Bot Started Successfully >_<")

def serve():
	UPDATES_OFFSET = 0

	while True:
		try:
			# Setup updates request
			updates_endpoint = urljoin(URL, "getUpdates")
			updates_data = {
				"offset": UPDATES_OFFSET,
			}

			# Ping for updates
			print(f"\nPinging '{updates_endpoint}' with data '{updates_data}'")
			resp = requests.get(updates_endpoint, data=updates_data)
			data = resp.json()
			print(f"Received response: {data}")
			if not data["result"]:
				continue

			# Handle any updates received
			UPDATES_OFFSET = data["result"][0]["update_id"] + 1
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
			process(message, firstname, username, chatid)

		except Exception as e:
			print(traceback.format_exc())


if __name__ == "__main__":
	serve()
