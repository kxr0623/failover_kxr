#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class Command():
	filename = ""
	error = 0
	device_ip=""
	def __init__(self,device_ip,filename):
		self.filename = filename
		self.device_ip = device_ip

	def get_filename(self):
		return self.filename

	def generate_command(self,output_dict):
		'''
		function:
			get commands for a divice from a command_file.
			ignore white space and #
		arg：
			:param    command_file.
		:return：
			:return   a list of commands.
		'''
		error = 0
		cmds = []
		#print( 'command-file:'+ self.filename)
		try:
			with open(self.filename, 'r') as f:
				for line in f:
					line = line.strip()  # 去掉每行头尾空白
					if not len(line) or line.startswith('#'):  # empty line or commond line.
						continue  # 是的话，跳过不处理
					cmds.append(line.strip('\n'))
			# print('cmds:',cmds)
		except Exception as e:
			# print("Command Info Error. Get command info from config file failed.(command file: "+self.filename+")")
			output_dict[self.device_ip] += "\033[0;31m[Error] Get command info from config file failed.(command file: "+self.filename+")\033[0m\n"

			# print(e, sys._getframe().f_code.co_name)
			if e.message == "":
				err=str(e)
			else:
				err=e.message
			output_dict[self.device_ip] +=" \033[0;31m Function ["+sys._getframe().f_code.co_name+"]: " + err + "\n"
			error = 1
		self.error = error
		return cmds


def check_commands_info(arr):
	'''
	Function:
	    check the command lines is valid.
	:param              arr:command lines
	Return：
		:return is_ok:  =True: commands fine     False: commands error
		:return msg：   if is_ok=Ture: msg=null   is_ok=False: msg=error information。
	'''
	is_ok=True
	msg=''

	if len(arr) == 0:
		is_ok = False
		msg="No command exists."+"\n"

	if is_ok == True:
		# Check: all line is comment line?
		all_tag_line = True
		for cmd in arr:
			if not cmd.startswith('#'):
				all_tag_line = False
				break
		if all_tag_line == True:
			is_ok = False
			msg="Command Info Error. All lines are commented."+"\n"

	res={'is_ok':is_ok,'msg':msg}
	return res

