# Copyright 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# -*- coding: utf-8 -*-

#general imports
import sys
import re
import time
import datetime
import os
import json
from dotenv import load_dotenv


#project imports
import graph_sdk


#prompts
START_THREADBYUSER_PROMPT = 'Getting all chats by user:';

#input prompts
ACCESS_TOKEN_INPUT_PROMPT = 'Access token? '
USER_ID_INPUT_PROMPT = 'user id?'

#error messages
ERROR_MISSING_ACCESS_TOKEN = 'Access token is required, exiting...'
ERROR_USER_ID = 'User id is required, exiting...'


#other constants
FIELD_THREAD='messages'
FIELD_THREAD_DATA = 'data'
FIELD_THREAD_ID = 'id'
FIELD_THREAD_PART = 'participants'
FIELD_THREAD_TIME = 'updated_time'

FIELD_MESSAGE_ID = 'id'
FIELD_MESSAGE_TIME = 'created_time'
FIELD_MESSAGE_SENDER = 'from' 
FIELD_MESSAGE_SENDER_NAME = 'name'
FIELD_MESSAGE_SENDER_EMAIL = 'email'
FIELD_MESSAGE_SENDER_ID = 'id'

TIME_FORMAT =  '%Y-%m-%dT%H:%M:%S+%f'

#file constants
FILE_WRITE_PERMISSION = 'wb'
FILE_DELIM = ','
FILE_QUOTE = '"'


#url constants for validating url param
SCIM_URL = 'https://www.facebook.com/scim/v1/'
GRAPH_URL = 'https://graph.facebook.com/'


#initialize
load_dotenv();

access_token = os.getenv("ACCESS_TOKEN");
#user_id = 100046091736554;
if os.getenv("HISTORY") : history = int(os.getenv("HISTORY"))
else : history = 180;
SINCE = datetime.datetime.now() - datetime.timedelta(days=history);

if os.getenv("LIMIT") : LIMIT = int(os.getenv("LIMIT"));
else : LIMIT = 50;


def exportMessagesByThread(access_token,threadid,userid) :
	messages = graph_sdk.getMessagesByThreads(GRAPH_URL,access_token,threadid,user_id,SINCE,'id,from,created_time','&limit='+str(LIMIT));
	return messages;


def exportThreadsID(access_token,user_id,threadsCol,filter_by_since=True) :
	threads=graph_sdk.getThreads(GRAPH_URL,access_token,user_id,'?fields=id,updated_time,name','&limit='+str(LIMIT));


	for thread in threads :
		#thread_time = datetime.datetime.strptime(thread['updated_time'], '%Y-%m-%dT%I:%M:%S+%f');
		if thread[FIELD_THREAD_ID] in threadsCol :
			threadsCol[thread[FIELD_THREAD_ID]][FIELD_THREAD_PART].add(user_id);
		else : 
			thread_time = datetime.datetime.strptime(thread[FIELD_THREAD_TIME], TIME_FORMAT);
			if (not filter_by_since) or (thread_time>SINCE) :
				threadsCol[thread[FIELD_THREAD_ID]] = {FIELD_THREAD_TIME:thread[FIELD_THREAD_TIME],FIELD_THREAD_PART:{user_id}};
	return threadsCol;

def exportMembersID(access_token) :
	members = graph_sdk.getMembers(GRAPH_URL,access_token,'?fields=id,email,name','&limit='+str(LIMIT));
	return members;



if __name__ == '__main__':
	if not access_token :
		access_token = input(ACCESS_TOKEN_INPUT_PROMPT);
		if not access_token:
			print(ERROR_MISSING_ACCESS_TOKEN)

	print('Extracting conversations since :' + str(SINCE));
	print('--------- Starting at : '+str(datetime.datetime.now()) +'---------');

	#extract active members

	members = exportMembersID(access_token);
	with open('members.csv', FILE_WRITE_PERMISSION) as outfile:
		json.dump(members, outfile)
	print('--------- '+str(len(members))+' Members extracted by : '+str(datetime.datetime.now()) +'---------');


	#extract threads with at least one active member
	threads={};
	for member in members :
		threads = exportThreadsID(access_token,member[FIELD_MESSAGE_SENDER_ID],threads);

	print('--------- '+str(len(threads))+' Threads extracted by : '+str(datetime.datetime.now()) +'---------');

	#extract messages within each chat 

	for thread in threads :
		print(thread + ' : ' + str(threads[thread]));
		user_id = threads[thread][FIELD_THREAD_PART].pop();
		threads[thread][FIELD_THREAD_PART].add(user_id);
		messages = exportMessagesByThread(access_token,thread,user_id)
		for msg in messages:
			if FIELD_MESSAGE_SENDER_EMAIL in msg[FIELD_MESSAGE_SENDER] :
				print(thread + ': '+msg[FIELD_MESSAGE_TIME]+'  from:'+msg[FIELD_MESSAGE_SENDER][FIELD_MESSAGE_SENDER_EMAIL]);
		print('-------------------------------------------');

	print('---------  messages extracted by : '+str(datetime.datetime.now()) +'---------');

		






