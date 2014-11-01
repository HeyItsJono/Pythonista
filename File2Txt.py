from console import clear
from console import hud_alert
from os import remove

def drop_extension(filename):
	dictionary = dict(enumerate(filename, start = 1))
	try:
		assert '.' in dictionary.values()
	except AssertionError:
		return filename
	for (k, v) in dictionary.iteritems():
		if v == '.':
			return filename[:k-1]
		else:
			pass

if __name__ == '__main__':
	clear()
	filename = raw_input('Enter filename (Path Optional) \n')
	with open(drop_extension(filename) + '.txt', 'w') as out_file:
		try:
			with open(filename, 'r') as in_file:
				out_file.write(in_file.read())
				in_file.close()
		except IOError:
			hud_alert('File not found', icon = 'error')
			remove(drop_extension(filename) + '.txt')
		out_file.close()
