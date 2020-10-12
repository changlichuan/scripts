# Copyright 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# -*- coding: utf-8 -*-

#general imports

#project imports
import graph_sdk

#prompts
START_THREADBYUSER_PROMPT = 'Getting all chats by user:';

#input prompts


#error messages



#other constants


#file constants
FILE_WRITE_PERMISSION = 'wb'
FILE_DELIM = ','
FILE_QUOTE = '"'


#url constants for validating url param
SCIM_URL = 'https://www.facebook.com/scim/v1/'
GRAPH_URL = 'https://graph.facebook.com/'


def exportThreadsByUser(access_token,scim_url,user_id) :
	print(START_THREADBYUSER_PROMPT+user_id);
	threadCollection = [];
	threadCollection = graph_sdk.getThreads()



if __name__ == '__main__':
	access_token = raw_input(ACCESS_TOKEN_INPUT_PROMPT);
	if not access_token:
		print(ERROR_MISSING_ACCESS_TOKEN)
		return