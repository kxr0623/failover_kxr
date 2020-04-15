#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Function：
	get devices information from a configure file(device——list).
	get commands for every device from different command files.
	command files is related to the configure information in device_list file.

	netmiko is used to connect to network device。
	run commands on the devices and return outputs for You.
	The output is recored in logfiles.
Usage：
	python main.py <username> <password> <enable_password>  <device_list_file>...<device_list_file>
	eg:
	python main.py  hkopr 123456 123456 /appset/script/failover/config/pro1_SZ_devices.list /appset/script/failover/config/pro2_HK_devices.list

	:param username:         username of network device
	:param password:         password of the user
	:param enable_password:  enablepassword of the user
	:param device_list:     the list file of devices. can set a couple of list_file.
							all the devices listed in one file will run concurrentlly.
Author： Xiaorui Kuang
History： 2019/03/05  release1.0
		2019/03/20  release2.0   add process control for all devices.
		2019/03/27  release2.1   change the way of running command on device. make it run with configure mode.
		2019/03/27  release2.2   writing outputs into log files
'''

import sys
import os
import datetime
from multiprocessing import Process, Queue
import Command
import Device
import Globle_Variables as gl
import Write_To_Log as WL
def get_time():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
########################################
def run_on_one_device(devive_info,output_q,logfile):
	'''
	function：
	 	get commands for a device
		run commands on a device.
	'''
	output_dict = {}
	ip = devive_info['device_IP']
	command_file = devive_info['device_command_file']

	WL.LOGFILE = WL.set_logfile(logfile,mode='write_log')
	# print("\n\n")
	try:
		output_dict[ip] = ("*" * 101)+"\n"
		output_dict[ip] += ("*" * 35) + " Start "+devive_info['device_IP']+("*" * 35) +"\n"
		WL.WriteLog(("*" * 90)+"\n")
		WL.WriteLog(("*" * 30) + "["+get_time()+"] Start "+devive_info['device_IP']+("*" * 30) +"\n")

		output_dict[ip] += get_time()+"> Start command file: " + command_file + " \n"
		WL.WriteLog(get_time()+"> Start command file: " + command_file + " \n")
		### Get Commands and Check it.
		command_config = Command.Command(device_ip=ip,filename=command_file)	# new class
		commands = command_config.generate_command(output_dict=output_dict)	# get a list of cmds
		if command_config.error > 0:
			output_dict['err_count']=1
			raise Exception("Cannot find Command file!")
			# return 1

		res = Command.check_commands_info(commands)
		if res['is_ok'] == False:
			output_dict[ip] += get_time()+"> [ERROR] Commands Error. Check commands failed. Detail:\n"
			WL.WriteLog(get_time()+"> [ERROR] Commands Error. Check commands failed. Detail:\n")
			output_dict[ip] += " \033[0;31m"+ res['msg'] +"\033[0m\n"
			WL.WriteLog(" \033[0;31m"+ res['msg'] +"\033[0m\n")
			output_dict['err_count'] = 1
			raise Exception("Something Err with Commands:"+res['msg'])
			# return 1
		# print(get_time() + "> get command info successful. command list:")
		else:
			output_dict[ip] += get_time() + "> Get commands successfully;" + "\n"
			WL.WriteLog(get_time() + "> Get commands successfully;" + "\n")

		## Connect device and run commands
		device_results = Device.exec_command(device=devive_info,output_dict=output_dict, cmds=commands,WL=WL)
		failed_device_count = device_results['error']

		if failed_device_count == 0:
			output_dict['err_count'] = 0
			output_dict[ip] += get_time() + "> " + devive_info['device_IP'] + " device Success" + "\n"
			WL.WriteLog(get_time() + "> " + devive_info['device_IP'] + " device Success" + "\n")
		else:
			output_dict['err_count'] = 1
			output_dict[ip] += get_time() + "> " + devive_info['device_IP'] + " device Fail" + "\n"
			WL.WriteLog(get_time() + "> " + devive_info['device_IP'] + " device Fail" + "\n")

	except Exception as e:
		if e.message == "":
			err = str(e)
		else:
			err = e.message
		output_dict[ip] += "\033[0;31m[Error] Detail:\033[0m" + "\n"
		WL.WriteLog("\033[0;31m[Error] Detail:\033[0m" + "\n")
		output_dict[ip] += " \033[0;31m Function [" + sys._getframe().f_code.co_name + "]: " + err + "\n"
		WL.WriteLog(" \033[0;31m Function [" + sys._getframe().f_code.co_name + "]: " + err + "\n")
		output_dict['err_count'] = 1
		# return 1


	# print("################################ End "+devive_info['device_IP']+"#######################")
	output_dict[ip] += ("*" * 35) + " End " + devive_info['device_IP'] + ("*" * 35) + "\n"
	output_dict[ip] += ("*" * 88) + "\n"
	WL.WriteLog(("*" * 30) + "["+get_time()+ "] End " + devive_info['device_IP'] + ("*" * 30) + "\n")
	WL.WriteLog(("*" * 101) + "\n")

	if WL.LOGFILE['fo'] != None and  WL.LOGFILE['fo'].closed == False:
		WL.LOGFILE['fo'].close()

	output_q.put(output_dict)
	# print output_dict[ip]
	return output_dict['err_count']

def get_devices(Dev_username,Dev_password,Dev_enable_password,Device_List_file,LOG_DIR):
	devices_info = []
	Failure_num = 0
	Device_num = 0
	device_info_dict = {}
	device_info_dict['username'] = Dev_username
	device_info_dict['password'] = Dev_password
	device_info_dict['enable_password'] = Dev_enable_password
	procs = []
	output_q = Queue(maxsize=20)

	print('(' + get_time() + ') Get devices information from the Device List file:')
	with open(Device_List_file, 'r') as f:
		for line in f:
			line = line.strip()  # 去掉每行头尾空白
			if not len(line) or line.startswith('#'):  # 判断是否是空行或注释行
				continue  # 是的话，跳过不处理
			print(line.strip('\n').split())
			devices_info.append(list(line.strip('\n').split()))
	# print(devices_info)

	### get info for every device.
	for device_info in devices_info:
		Device_num += 1
		device_info_dict['device_name'] = device_info[0]
		device_info_dict['device_IP'] = device_info[1]
		device_info_dict['device_type'] = device_info[2]
		device_info_dict['device_command_file'] = device_info[3]
		logfile=LOG_DIR+ '/'+ device_info_dict['device_name'] + '.log'
		# print(device_info_dict)
		# result_code= run_on_one_device(device_info_dict)
		my_proc = Process(target=run_on_one_device, args=(device_info_dict, output_q,logfile))
		my_proc.start()
		procs.append(my_proc)

	# Make sure all processes have finished
	for a_proc in procs:
		a_proc.join()

	while not output_q.empty():
		my_dict = output_q.get()
		for key, value in my_dict.items():
			if key == "err_count":
				Failure_num += value
			else:
				print(value)
	print('\n\033[0;32m[Result] There are ' + str(Device_num) + ' Devices in toltal. ' + str(
		Failure_num) + ' devices Running command Failed.\033[0m')
	return Failure_num

if __name__ == '__main__':
	Dev_username = sys.argv[1]
	Dev_password = sys.argv[2]
	Dev_enable_password = sys.argv[3]
	err_count=0
	# print(len(sys.argv))
	# SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
	LOG_DIR= BASE_DIR+"/output_logs"
	for i in range(4,len(sys.argv)):
		Device_List_file=sys.argv[i]
		print("\n\n")
		print(("#" * 10) + " Get Device Lists: " + Device_List_file + ("#" * 10))
		err_dev_num = get_devices(Dev_username,Dev_password,Dev_enable_password,Device_List_file,LOG_DIR)
		err_count += err_dev_num

	exit(err_count)




