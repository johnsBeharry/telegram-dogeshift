from behave import * 
from test import *
import json
  

@given(u'active_users in a chat session "{chat_id}"')
def step_impl(context, chat_id):
	context.active_users = json.loads(context.text)
	context.chat_id = chat_id

@when(u'active_users object is passed to getCount')
def step_impl(context):
	context.response = getCount(context.chat_id, context.active_users)

@then(u'a list of active users is returned')
def step_impl(context):
	print context.response
