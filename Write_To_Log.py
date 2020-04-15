#!/usr/bin/python
# -*- coding: utf-8 -*-

# from common import *
# from lib.base.common import *
import Globle_Variables as gl
import sys
import datetime
# sys.setdefaultencoding('utf8')

'''
Information of logfile
'''
LOGFILE = {
	'logfile' : '',
	'fo'       : None,
	'mode'     : 'std',
	'color'    : gl.FontColor.BLUE,
}

def set_logfile(filename='', mode='std', font_color=gl.FontColor.BLUE):
	if filename != '':
		res = {}
		res['logfile']  = filename
		res['fo']        = None
		res['mode']      = mode
		res['color']     = font_color

		if res['mode'] in ['write_log', 'both']:
			res['fo'] = open(filename, 'a')
	else:
		res = LOGFILE

	return res

'''
print the massage and write to log
'''
def WriteLog(msg, color=''):
	fo = LOGFILE['fo']
	mode = LOGFILE['mode']
	if color == '':
		real_color = LOGFILE['color']
	else:
		real_color = color
	if isinstance(msg, str) == False:
		msg = str(msg)
	# msg = "\033[0;"+color_code+"m" + msg + "\033[0m"
	if mode in ['write_log', 'both']:
		fo.write(msg)
