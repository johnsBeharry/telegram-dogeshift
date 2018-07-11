Feature: Telegram Bot
As a ___ 
I want ___
So that ___


Scenario: Get active users
Given active_users in a chat session "123"
"""
{
	"123": {
		"johnsBeharry": 1530835383.860277,
		"micey969": 1530835383.860277
	}
}
"""
When active_users object is passed to getCount
Then a list of active users is returned 