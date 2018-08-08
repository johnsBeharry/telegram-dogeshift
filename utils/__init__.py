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

