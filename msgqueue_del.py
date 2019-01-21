#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:18:54 2018

@author: sdc
"""

import os
import re


def find_message_queue_id():
	content = os.popen("ipcs -q").read()
	msgqueue_id_regex = re.compile(r'\s\d{5,10}\s')
	ids = [one.strip() for one in msgqueue_id_regex.findall(content)]
	return ids
def del_message_queue(queue_id):
	for id in queue_id:
		cmd = "ipcrm -q " + id
		print(cmd)
		os.system(cmd)

def main():
	ids = find_message_queue_id()
	print(ids)
	del_message_queue(ids)

if __name__ == '__main__':
	main()
