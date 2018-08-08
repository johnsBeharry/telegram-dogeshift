from behave import * 
import unittest
from utils import *
import json

testcase = unittest.TestCase('__init__')
  

@given(u'active_users in a chat session "{chat_id}"')
def step_impl(context, chat_id):
	context.active_users = json.loads(context.text)
	context.chat_id = chat_id

@given(u'the timenow is "{timenow}"')
def step_impl(context, timenow):
	context.timenow = float(timenow)

@when(u'active_users object is passed to getActive')
def step_impl(context):
	context.response = getActive(context.chat_id, context.active_users, context.timenow)

@then(u'a list of active users is returned')
def step_impl(context):
	context.expected_users = json.loads(context.text)
	testcase.assertCountEqual(context.response, context.expected_users)
