import sys
# print sys.getrecursionlimit()

f = open('generated.xml','w')
f.write('<?xml version="1.0" encoding="utf-8" ?>')


def help(num):

	f.write('<hello>')
	if num <= 0:
		return 
	else:
		help(num-1)

	f.write('</hello>')

help(3)
f.close()