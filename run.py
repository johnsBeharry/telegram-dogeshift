import requests
import time
from block_io import BlockIo
import os
import utils

token = os.environ['TELEGRAM_BOT_TOKEN']  # Telegram bot token
url = "https://api.telegram.org/bot%s/" % (token)
n = 0
version = 2
block_io = BlockIo(os.environ['BLOCKIO_API_KEY'], os.environ['BLOCKIO_PIN'], version)
active_users = {}
current_time = time.time()

# an array of reward items
monikers_tuple = [
    ("sandwich", "sandwiches", 21),
    ("coffee", "coffees", 7),
    ("tea", "teas", 5),
    ("lunch", "lunches", 49)
]
monikers_dict = {n[i]: n[2] for n in monikers_tuple for i in range(2)}
monikers_flat = [monikers_tuple[i][j] for i in range(len(monikers_tuple)) for j in range(3)]
monikers_str = '\n'.join(f"{i[0]}: {i[2]} doge" for i in monikers_tuple)


def withdrawMsg(dataPassed, address, amount):
    if dataPassed['status'] == 'success':
        return f"Withdrawal successful! Track it's progress here: https://dogechain.info/tx/{dataPassed['data']['txid']}"
    # To figure out later: how to get entire 'data' object returned when 'except'.
    elif dataPassed['status'] == 'fail':
        if dataPassed['data']['error_message'].split(' ')[0] == 'Cannot':
            return f"Sorry, funds are too low. Your maximum withdrawable balance is {float(dataPassed['data']['max_withdrawal_available']):,.0f} Doge.",
        elif dataPassed['data']['error_message'].split(' ')[0] == 'One':
            return f"Sorry, your destination address is invalid."
        else:
            return error


def sendMsg(message, chatid):
    requests.get(url + "sendMessage", data={"chat_id": chatid, "text": message})


def returnBal(username):
    data = block_io.get_address_balance(labels=username)
    balance = data['data']['balances'][0]['available_balance']
    pending_balance = data['data']['balances'][0]['pending_received_balance']
    balance_msg = "\nBalance: " + f"{float(balance):,.0f}" + " Doge"
    pending_msg = "\nPending: " + f"{float(pending_balance):,.0f}" + " Doge (not yet added)"
    pending_msg = "" if float(pending_balance) == 0 else pending_msg
    return (balance, pending_balance, balance_msg, pending_msg)


def process(message, username, chatid):
    global active_users
    parsedMsg = utils.msg_parse(message, monikers_flat)

    if "/register" in parsedMsg[0].lower():
        try:
            block_io.get_new_address(label=username)
            sendMsg("@" + username + " you are now registered.", chatid)
        except:
            sendMsg("@" + username + " you are already registered.", chatid)

    elif "/balance" in parsedMsg[0].lower():
        try:
            (balance, pending_balance, balance_msg, pending_msg) = returnBal(username)
            sendMsg("@" + username + balance_msg + pending_msg, chatid)
        except:
            sendMsg("@" + username + " you are not registered yet. use /register to register.", chatid)

    elif "/tip" in parsedMsg[0].lower():
        try:
            person = parsedMsg[1]
            amount_msg = parsedMsg[2]
            amount = abs(float(amount_msg)) * monikers_dict.get(parsedMsg[3], 1)

            if monikers_dict.get(parsedMsg[3], 0) == 0:
                sin_plu = "doge"
            elif amount_msg == 1:
                sin_plu = monikers_tuple[monikers_flat.index(parsedMsg[3]) // 3][0]
            else:
                sin_plu = monikers_tuple[monikers_flat.index(parsedMsg[3]) // 3][1]

            block_io.withdraw_from_labels(amounts=str(amount), from_labels=username, to_labels=person)
            sendMsg("@" + username + " tipped " + str(amount_msg) + " " + sin_plu +
                    ("" if monikers_dict.get(parsedMsg[3], 0) == 0 else f" ({str(amount)} doge)") +
                    " to @" + person + "", chatid)
        except ValueError:
            sendMsg("@" + username + " invalid amount.", chatid)
        except:
            sendMsg("@" + username + " insufficient balance or @" + person + " is not registered yet.", chatid)

    elif "/address" in parsedMsg[0].lower():
        try:
            data = block_io.get_address_by_label(label=username)
            sendMsg("@" + username + " your address is " + data['data']['address'] + "" +
                    "\n\nhttps://dogechain.info/address/" + data['data']['address'] + "", chatid)
        except:
            sendMsg("@" + username + " you are not registered yet. use /register to register.", chatid)

    elif "/withdraw" in parsedMsg[0].lower():
        try:
            amount = abs(float(parsedMsg[2]))
            address = parsedMsg[4]
            data = block_io.withdraw_from_labels(amounts=str(amount), from_labels=username, to_addresses=address)
            sendMsg(withdrawMsg(data, address, amount), chatid)
        except ValueError:
            sendMsg(f"Sorry, '{parsedMsg[1]}' is not a valid amount.", chatid)
        except Exception as error:
            try:
                url_fail = 'https://block.io/api/v2/withdraw_from_labels/?' + \
                           'api_key=' + os.environ['BLOCKIO_API_KEY'] + \
                           '&from_labels=' + username + \
                           '&to_addresses=' + address + \
                           '&amounts=' + str(amount)
                data = requests.get(url_fail, data={"offset": n}).json()

                sendMsg(withdrawMsg(data, address, amount), chatid)
            except:
                if (str(error)[:4] == "Fail"):
                    sendMsg("@" + username + ", " + str(error)[8:9].lower() + str(error)[9:], chatid)
                else:
                    sendMsg("@" + username + " oops it looks like you entered something wrong 🙈", chatid)
                    sendMsg("Double-check your amount & address and let's try that again!", chatid)

    elif "/rain" in parsedMsg[0].lower():
        try:
            users = getActive(chatid, active_users, current_time)
            if username in users:
                users.remove(username)
            number = len(users)

            amount = ("10," * (number - 1)) + '10'
            name = username
            username = ((username + ',') * (number - 1)) + username
            if number < 2:
                sendMsg("@" + username + " less than 2 shibes are active.", chatid)
            else:
                print(amount)
                print(username)
                block_io.withdraw_from_labels(amounts=amount, from_labels=username, to_labels=','.join(users))
                sendMsg("@" + name + " is raining on " + ','.join(users) + "", chatid)
        except:
            pass

    elif "/monikers" in parsedMsg[0].lower():
        sendMsg("--MONIKERS--\n\n" +
                monikers_str, chatid)

    elif "/getbotusers" in parsedMsg[0].lower():
        api_users = block_io.get_my_addresses(page='1')['data']['addresses']
        reg_users = utils.getRegistered(api_users)
        reg_users_string = ", ".join(f"@{i}" for i in reg_users)
        sendMsg(f"Active shibes ({len(reg_users)}): {reg_users_string}", chatid)

    elif "/active" in parsedMsg[0].lower():
        sendMsg("Current active : %d shibes" % (len(getActive(chatid, active_users, current_time))), chatid)
    else:
        try:
            active_users[chatid][username] = time.time()
        except KeyError:
            active_users[chatid] = {}
            active_users[chatid][username] = time.time()


while True:
    try:
        print("such dogeshift. much running.")
        # get's updates from the bot and decodes it
        data = requests.get(url + "getUpdates", data={"offset": n}).json()
        n = data["result"][0]["update_id"] + 1
        username = data["result"][0]["message"]["from"]['username']
        chatid = data["result"][0]["message"]["chat"]["id"]
        message = data["result"][0]["message"]["text"]
        process(message, username, chatid)
    except:
        pass
