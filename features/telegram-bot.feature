Feature: Telegram Bot
As a ___ 
I want ___
So that ___


Scenario: Get list of active users
Given active_users in a chat session "123"
"""
{
	"123": {
		"johnsBeharry": 1530000125.000001,
		"micey969": 1530000265.000001,
		"selimira": 1530000545.000001,
		"esc750": 1530000000.000001,
		"kengeo": 1529999999.999999
	},
	"124": {
		"anon": 1530000000,
		"moose": 1530000000.000001
	}
}
"""
And the timenow is "1530000600.000001"
When active_users object is passed to getActive
Then a list of active users is returned 
"""
["johnsBeharry", "micey969", "esc750", "selimira"]
"""

Scenario: No active users
Given active_users in a chat session "124"
"""
{
	"124": {
		"anon": 1530000000,
		"moose": 1530000000
	}
}
"""
And the timenow is "1530000600.000001"
When active_users object is passed to getActive
Then a list of active users is returned 
"""
[]
"""
