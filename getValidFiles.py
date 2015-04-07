#!/usr/bin/python
import os, re

class Dataset:
	'''dataset of info from FINAL.txt'''
	def __init__(self, vallist):
		[self.num, 
		self.thresh_joy,
		self.thresh_au12,
		self.joy_int,
		self.joy_frt,
		self.au12_int,
		self.au12_frt,
		self.mix_int,
		self.mix_frt] = vallist
		self.paramlist = []

class ParamData:
	'''dataset of p1 vs p2 data'''
	def __init__(self, parameterlist):
		[self.parameters,
		self.p_rev,
		self.p_reb,
		self.n_rev,
		self.n_reb,
		self.miscount] = parameterlist

filelist = []
dslist = []

rootDir = "individual_data"
for dirName, subdirList, fileList in os.walk(rootDir):
	for sname in subdirList:
		finalfile = os.path.join(rootDir, sname) + "/FINAL.txt"
		filelist.append(finalfile)

for f in filelist:
	fl = open(f, 'r')
	nextline = fl.readline()
	n = re.search("\d", nextline)
	val = int(nextline[n.start():])
	if val > 0:
		vallist = []
		vallist.append(val)
		while(nextline.find("parameters") == -1):
			m = re.search("\d+.\d+", nextline)
			if m is not None:
				numb = float(nextline[m.start():])
				vallist.append(numb)
			nextline = fl.readline()
		dset = Dataset(vallist)
		parset = []
		
		parameters = nextline[21:]
		parlist = [parameters]
		print parameters
		for i in range(5):
			nextline = fl.readline()
			m = re.search("\d+.\d", nextline)
			if m is not None:
				numb = float(nextline[m.start():])
				print numb
				parlist.append(numb)
		parset.append(ParamData(parlist))
		nextline = fl.readline()
		nextline = fl.readline()
		
		parameters = nextline[21:]
		parlist = [parameters]
		print parameters
		for i in range(5):
			nextline = fl.readline()
			m = re.search("\d+.\d", nextline)
			if m is not None:
				numb = float(nextline[m.start():])
				print numb
				parlist.append(numb)
		parset.append(ParamData(parlist))

		dset.paramlist = parset
		dslist.append(dset)

for item in dslist:
	for par in item.paramlist:
		print par.parameters, par.p_rev, par.p_reb, par.n_rev, par.n_reb