# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# based off python3
#

import requests
#import csv_header
import json
import datetime
import urllib
#import collections

#general constants
FIRST_ITEM = 0
EMPTY_RESPONSE = ''


# property constants
FIELD_NAME = 'name'
FIELD_MESSAGE = 'message'
FIELD_ID = 'id'
FIELD_DATA = 'data'
FIELD_PAGING = 'paging'
FIELD_NEXT = 'next'
FIELD_EMAIL = 'email'
FIELD_MESSAGE_TIME = 'created_time'
TIME_FORMAT =  '%Y-%m-%dT%H:%M:%S+%f'



#request constants
HEADER_AUTH_KEY = 'Authorization'
HEADER_AUTH_VAL_PREFIX = 'Bearer '
USERS_RESOURCE_SUFFIX = 'Users'
THREAD_RESOURCE_SUFFIX = 'conversations'
MESSAGE_RESOURCE_SUFFIX = 'messages'
MEMBERS_RESOURCE_SUFFIX = 'members'
COMMUNITY_RESOURCE_SUFFIX='community'

HTTP_DELIM = '/'
PARA_DELIM = '?'
PARA_AND = '&'
#EMAIL_LOOKUP_SUFFIX = '?filter=userName'
#ESCAPED_EMAIL_LOOKUP_PREFIX = ' eq \"'
#ESCAPED_EMAIL_LOOKUP_SUFFIX = '\"'
START_INDEX = "startIndex="
USER_FILTER = "user="
FIELDS_FILTER = "fields="


#response status code constants
RESPONSE_OK = 200
RESPONSE_CREATED = 201


#prompt constants
RESULT_STATUS_DELIM = ':'
EXPORT_RESULT_DELIM = " / "
#CREATING_USER_PROMPT = 'Creating user '
#DELETING_USER_PROMPT = 'Deleting user '
#UPDATING_USER_PROMPT = 'Updating user '

#error constants
ERROR_WITHOUT_MESSAGE = "Invalid request, no error message found"


def getHeaders(access_token):
	headers = {HEADER_AUTH_KEY: HEADER_AUTH_VAL_PREFIX + access_token}
	return headers

def getMessagesByThreads(graphurl,access_token,threadid,userid,since,fields=None, filters=None):
	if fields : fields = PARA_AND+FIELDS_FILTER+fields
	url = graphurl+str(threadid)+HTTP_DELIM+MESSAGE_RESOURCE_SUFFIX+PARA_DELIM+USER_FILTER+str(userid)+fields+filters;
	return getPagedDataWithFilter(access_token,url,[],FIELD_MESSAGE_TIME,since);
		

def getThreads(graphurl, access_token, userid, fields=None, filters=None):
	url = graphurl+str(userid)+HTTP_DELIM+THREAD_RESOURCE_SUFFIX+fields+filters;
	return getPagedData(access_token,url,[])

def getMembers(graphurl,access_token,fields=None,filters=None) :
	#memberColletion = [];
	url = graphurl+HTTP_DELIM+COMMUNITY_RESOURCE_SUFFIX+HTTP_DELIM+MEMBERS_RESOURCE_SUFFIX+fields+filters;
	return getPagedData(access_token,url,[])


def getPagedData(access_token, endpoint, data):
    headers = getHeaders(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    json_keys = result_json.keys()
    if FIELD_DATA in json_keys and len(result_json[FIELD_DATA]):
        data.extend(result_json[FIELD_DATA])
    if FIELD_PAGING in json_keys and FIELD_NEXT in result_json[FIELD_PAGING]:
        next = result_json[FIELD_PAGING][FIELD_NEXT]
        if next:
            getPagedData(access_token, next, data)
    return data

def getPagedDataWithFilter(access_token, endpoint, data,filter_field,filter_value):
	headers = getHeaders(access_token)
	result = requests.get(endpoint,headers=headers)
	result_json = json.loads(result.text)
	json_keys = result_json.keys()
	if FIELD_DATA in json_keys and len(result_json[FIELD_DATA]):
		for item in result_json[FIELD_DATA] :
			filter_date = datetime.datetime.strptime(item[filter_field],TIME_FORMAT)
			if filter_date>filter_value : data.extend([item]);
			else : return data

	if FIELD_PAGING in json_keys and FIELD_NEXT in result_json[FIELD_PAGING]:
		next = result_json[FIELD_PAGING][FIELD_NEXT]
		if next:
			#print('go for next page')
			getPagedDataWithFilter(access_token, next, data,filter_field,filter_value)
	return data
	


