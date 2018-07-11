import time

def getCount(chatid, active_users):
    n = []
    t = time.time()
    chat_users = active_users[chatid]
    print active_users
    for i in chat_users:
        if t - chat_users[i] <= 600:
            n.append(i)
    return n
