#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time


# 错误代码
class ErrorCode():
	OK                      = 0
	ERROR                   = 1

	ARGUMENT_ERROR          = 2
	DATABASE_ERROR          = 3
	TASK_INFO_ERROR         = 4
	DEVICE_INFO_ERROR       = 4
	COMMAND_INFO_ERROR      = 5
	SESSION_INFO_ERROR      = 6

	ALL_DEVICE_FAILED       = 10
	PART_DEVICE_FAILED      = 11


# 字体颜色
class FontColor():
	RED     = 'red'
	YELLOW  = 'yellow'
	BLUE    = 'blue'
	GREEN   = 'green'
	WHITE   = 'white'
'''
Get the color code
'''
def get_font_color_code(color):
	dic = {
		'red'    : 31,
		'yellow' : 33,
		'blue'   : 34,
		'green'  : 32,
		'black'  : 30,
		'white'  : 37,
	}
	if color in dic.keys():
		color_code = dic[color]
	else:
		color_code = dic['white']
	return str(color_code)



