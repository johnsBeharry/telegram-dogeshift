import time

"""
This function acceppts two parameters; chatid and active_users
and returns a list of active users in a chat session

Parameters:
	chatid (int): Id of current chat session 
	active_users (object): list of users in the chat session

Return:
	n (list): currently active users
"""

def getCount(chatid, active_users):
    n = []
    t = time.time()
    chat_users = active_users[chatid]
    print(active_users)
    for i in chat_users:
        if t - chat_users[i] <= 600:
            n.append(i)
    return n
