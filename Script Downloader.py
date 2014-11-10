# coding: utf-8

import ui
import urllib2
import clipboard
from console import hud_alert
import console
import sys
import os

def parse_name(url):
	n = len(url)-1
	name = ''
	try:
		assert r'/' in url
	except AssertionError:
		return url
	for char in url:
		if url[n] != r'/':
			name = url[n] + name
			n += -1
		else:
			break
	return name

def parse_extension(name):
	n = len(name)-1
	extension = ''
	try:
		assert r'.' in name
	except AssertionError:
		return extension
	for char in name:
		if name[n] != r'.':
			extension = name[n] + extension
			n += -1
		else:
			break
	return extension


#@ui.in_background
#def download(url):
#   return urllib2.urlopen(url)


def button_tapped(sender):
	'@type sender: ui.Button'

	console.clear()

	urlfield = sender.superview['urlfield']
	filenamefield = sender.superview['filenamefield']
	extensionfield = sender.superview['extensionfield']
	extensioncontrol = sender.superview['extensioncontrol']

	if extensioncontrol.selected_index == 0:
		extension = '.py'
	elif extensioncontrol.selected_index == 1:
		extension = '.pyui'
	elif extensioncontrol.selected_index == 2:
		if extensionfield.text != '':
			extension = '.' + extensionfield.text
		else:
			extension = ''

	filename = filenamefield.text + extension
	filenum = 1
	while os.path.isfile(filename) is True:
		filename = filenamefield.text + ' ({})'.format(str(filenum)) + extension
		filenum += 1
	hud_alert('Downloading...')
	try:
		console.show_activity()
		url = urllib2.urlopen(urlfield.text)
#       url = download(urlfield.text)
	except (ValueError, urllib2.URLError):
		hud_alert('URL not valid', icon = 'error')
		sys.exit()
	hud_alert("Saving...")
	with open(filename, "w") as out_file:
		out_file.write(url.read())
		out_file.close()
	console.hide_activity()
	hud_alert("Saved!")


def paste_tapped(sender):
	'@type sender: ui.Button'

	urlfield = sender.superview['urlfield']
	filenamefield = sender.superview['filenamefield']
	extensionfield = sender.superview['extensionfield']
	extensioncontrol = sender.superview['extensioncontrol']

	urlfield.text = unicode(clipboard.get())
	name = parse_name(urlfield.text)
	extension = parse_extension(name)
	name = name[:(len(name) - (len(extension) + 1))]
	filenamefield.text = name
	if extension == 'py':
		extensioncontrol.selected_index = 0
		extensionfield.text = ''
	elif extension == 'pyui':
		extensioncontrol.selected_index = 1
		extensionfield.text = ''
	else:
		extensioncontrol.selected_index = 2
		extensionfield.text = extension


def clear_tapped(sender):
	'@type sender: ui.Button'

	urlfield = sender.superview['urlfield']
	filenamefield = sender.superview['filenamefield']
	extensionfield = sender.superview['extensionfield']

	if sender.name == 'clearurl':
		urlfield.text = ''
	elif sender.name == 'clearname':
		filenamefield.text = ''
	elif sender.name == 'clearextension':
		extensionfield.text = ''


v = ui.load_view('Script Downloader')
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present(orientations=['portrait'])
