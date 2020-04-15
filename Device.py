#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import time
import traceback

from netmiko import ConnectHandler
# import Write_To_Log as WL
def get_time():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def exec_command(device, cmds,output_dict,WL, timeout=600):
	'''
	Function：
		connect to a netwrk device; run a set of commands in configure-mode on the device.
	:param device:    a dictionary of device information
	:param cmds:       a list of commands
	:param output_dict: a dictionary of output information {deviceIP:outputmassage}
	:param timeout:    timeout number
	:return results:  {ip:[device ip] , err:[result code]}
	'''
	real_cmds = []
	err = 1   # get the result of running.
	mgs=''
	result_cmd =''
	try:
		# print("### Start connect to (ip: " + device['device_IP'] + ") and run command.")
		mgs = get_time()+"> Start run commands on (ip: " + device['device_IP'] + ")"+ "\n"
		WL.WriteLog(get_time()+"> Start run commands on (ip: " + device['device_IP'] + ")"+ "\n")

		# change device into format to complete netmiko module requirements.
		real_device = {
			'device_type': device['device_type'],  #  cisco_asa
			'ip':          device['device_IP'],
			'username':    device['username'],
			'password':    device['password'],
#				'port':        int(device['port']),
			'secret':      device['enable_password'],
			'timeout':     timeout,
		}
		conn = ConnectHandler(**real_device)
		hostname = conn.base_prompt
		# print("[INFO] connect device successfully: "+hostname)
		mgs += get_time()+"> Connect device successfully: "+hostname+"\n"
		WL.WriteLog(get_time()+"> Connect device successfully: "+hostname+"\n")
		# result_cmd = conn.send_config_set(real_cmds,exit_config_mode=False)
		real_cmds=cmds
		commit_flag='F'
		while device['device_type'] == 'juniper' and'commit' in real_cmds:
			real_cmds.remove('commit')
			commit_flag = 'T'

		result_cmd += conn.send_config_set(real_cmds,delay_factor=4,exit_config_mode=False)
		if device['device_type'] == 'juniper' and commit_flag=='T':
			result_cmd += conn.commit()

		mgs += get_time() + "> Output of Running cmds: \n"
		WL.WriteLog(get_time() + "> Output of Running cmds: \n")
		mgs += ("=" * 35) + "Output Begin" + ("=" * 35) + "\n"
		WL.WriteLog(("=" * 35) + "Output Begin" + ("=" * 35) + "\n")
		if isinstance(result_cmd, str) == False:
			result_cmd = str(result_cmd)
		mgs += "\033[0;34m " + result_cmd + "\033[0m" + "\n"
		WL.WriteLog("\033[0;34m " + result_cmd + "\033[0m" + "\n")
		mgs += ("-" * 35) + "Output End" + ("-" * 35) + "\n"
		WL.WriteLog(("-" * 35) + "Output End" + ("-" * 35) + "\n")

		conn.disconnect()
		err = 0

	except Exception as e:
		# print("Device execution Error. Detail:")
		if e.message == "":
			errmsg = str(e)
		else:
			errmsg = e.message
		mgs += "\033[0;31mDevice execution Error. Detail:\033[0m" + "\n"
		WL.WriteLog("\033[0;31mDevice execution Error. Detail:\033[0m" + "\n")
		# print(e, sys._getframe().f_code.co_name)
		# mgs += " \033[0;31m Function [" +sys._getframe().f_code.co_name+ "]: " + errmsg  + "\033[0m\n"
		# WL.WriteLog(" \033[0;31m Function [" +sys._getframe().f_code.co_name+ "]: " + errmsg  + "\033[0m\n")
		mgs += " \033[0;31m " + str(traceback.format_exc()) + "\033[0m\n"
		WL.WriteLog(" \033[0;31m " + str(traceback.format_exc()) + "\033[0m\n")
		# print("[ERROR] device(ip: " + device['device_IP'] + ") skipped.")

	finally:
		# print("[INFO]: device(ip: " + device['device_IP'] + ") end.")
		mgs += get_time()+"> Device(ip: " + device['device_IP'] + ") end." + "\n"
		WL.WriteLog(get_time()+"> Device(ip: " + device['device_IP'] + ") end." + "\n")

	results = {'ip':device['device_IP'], 'error':err}
	output_dict[device['device_IP']] += mgs

	return results



