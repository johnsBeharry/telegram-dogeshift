import re


def getActive(chatid, active_users, timenow):
    """
    This function accepts three parameters; chatid, active_users
    and timenow and returns a list of active users in a chat session

    Parameters:
        chatid (int): ID of chat session 
        active_users (object): list of users in the chat session
        timenow (float): value of current time

    Return:
        n (list): currently active users
    """
    n = []
    chat_users = active_users[chatid]
    for i in chat_users:
        if timenow - chat_users[i] <= 600:
            n.append(i)
    return n


def msg_parse(message, monikers_flat):
    """
    This function accepts two parameters; message & monikers_flat
    and returns a list of selected message items

    Parameters:
        message (string): imported Telegram message
        monikers_flat (list): list of all tuple elements from 'monikers_tuple'

    Return:
        n (list): selected message items  as follows:
        message[0]: bot call
        message[1]: username
        message[2]: amount
        message[3]: moniker
        message[4]: address
    """
    pattern_call = "^(\/\w+)"
    pattern_address = "(\w{26,})"
    pattern_username = "@(\w+)"
    pattern_amount = "\s(\d+)" if re.search("\s(\d+)", message) else "\s(a[h|n]?)\s"
    pattern_moniker = pattern_amount.replace("(", "").replace(")", "") + "\s*(\w+)"
    patterns = [pattern_call, pattern_username, pattern_amount, pattern_moniker, pattern_address]

    results = []
    for pattern in patterns:
        result = re.search(pattern, message)
        if result:
            results.append(result.group(1))
        else:
            results.append("")

    # Second pass to set moniker word properly at results[3]
    pattern_allWords = "[^\/]\\b([a-zA-Z]+)\\b"
    allWords = re.findall(pattern_allWords, message)
    if results[3] not in monikers_flat:
        for word in allWords:
            if word in monikers_flat:
                results[3] = word
                break

    # Convert single amount descriptors 'a/an'  to an amount of "1" at results[2]
    results[2] = "1" if ((results[2] == "" and results[3] != "") or 'a' in results[2]) else results[2]

    return results
