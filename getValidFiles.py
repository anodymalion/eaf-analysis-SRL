#!/usr/bin/python
import os, re, statistics

values = ["num", "joy threshold", "au12 threshold", "propr of joy in truth", "propr of truth in joy",
"propr of au12 in truth", "propr of truth in au12", "propr of mixed in truth", "propr of truth in mixed"]
pvalues = ["parameters", "positive relevance", "positive reliability", "negative relevance", 
"negative reliability", "miscount"]

class Dataset:
	'''dataset of info from FINAL.txt'''
	def __init__(self, vallist):
		'''[self.num, 
		self.thresh_joy,
		self.thresh_au12,
		self.joy_int,
		self.joy_frt,
		self.au12_int,
		self.au12_frt,
		self.mix_int,
		self.mix_frt] = vallist'''
		self.vlist = vallist
		self.paramlist = []

class ParamData:
	'''dataset of p1 vs p2 data'''
	def __init__(self, parameterlist):
		'''[self.parameters,
		self.p_rev,
		self.p_reb,
		self.n_rev,
		self.n_reb,
		self.miscount] = parameterlist'''
		self.plist = parameterlist

filelist = []
dslist = []
numlist = []
joy_intlist = []
joy_frtlist = []
au12_intlist = []
au12_frtlist = []
mix_intlist = []
mix_frtlist = []

rootDir = "/cygdrive/e/individual_data"
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
		#print parameters
		for i in range(5):
			nextline = fl.readline()
			m = re.search("\d+.\d", nextline)
			if m is not None:
				numb = float(nextline[m.start():])
				#print numb
				parlist.append(numb)
		parset.append(ParamData(parlist))
		nextline = fl.readline()
		nextline = fl.readline()
		
		parameters = nextline[21:]
		parlist = [parameters]
		#print parameters
		for i in range(5):
			nextline = fl.readline()
			m = re.search("\d+.\d", nextline)
			if m is not None:
				numb = float(nextline[m.start():])
				#print numb
				parlist.append(numb)
		parset.append(ParamData(parlist))

		dset.paramlist = parset
		dslist.append(dset)

for i in range(0, len(dslist[0].vlist)):
	lst = []
	for d in dslist:
		lst.append(d.vlist[i])
	#print lst
	print values[i]
	print "median:", statistics.median(lst)
	print "mean:", statistics.mean(lst)
	print "std dev:", statistics.stdev(lst)
	print "\n"
for i in range(1, len(dslist[0].paramlist[0].plist) - 1):
	#print i
	lst1 = []
	lst2 = []
	for d in dslist:
		lst1.append(d.paramlist[0].plist[i])
		lst2.append(d.paramlist[1].plist[i])
	#print lst1, lst2

	print pvalues[i], ":  Truth vs Joy Intensity"
	print "median:", statistics.median(lst1)
	print "mean:", statistics.mean(lst1)
	print "std dev:", statistics.stdev(lst1)
	print "\n"

	print pvalues[i], ":  Truth vs AU12"
	print "median:", statistics.median(lst2)
	print "mean:", statistics.mean(lst2)
	print "std dev:", statistics.stdev(lst2)
	print "\n"	

	#	print par.parameters, par.p_rev, par.p_reb, par.n_rev, par.n_reb