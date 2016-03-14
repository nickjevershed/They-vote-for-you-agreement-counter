import requests
import simplejson as json
from itertools import groupby
from operator import itemgetter


crossBenchers = ['jacqui_lambie','glenn_lazarus','david_leyonhjelm','john_madigan','ricky_muir','nick_xenophon','dio_wang','bob_day']

majorParties = ['Australian Labor Party', 'Australian Greens', 'Liberal Party','Country Liberal Party','National Party']
partyShortnames = {'Australian Labor Party':'ALP','Australian Greens':'Greens','Liberal Party':'LIB','National Party':'NAT','Country Liberal Party':'CLP'}

#change to party-voting-new.json
dataFile = open('crossbench-voting-new.json')
data = json.load(dataFile)
crossFile = open('crossbencher-info.json')
crossInfo = json.load(crossFile)

jsonObj = {}

for s in crossBenchers:
	print s
	newData = {}
	newData['keyName'] = data[s]['keyName']
	newData['cleanKeyName'] = data[s]['cleanKeyName']
	newData['shortName'] = crossInfo[data[s]['cleanKeyName']]['shortName']
	voteData = []
	# for d in data[s]['voteData']:
	# 	if d['cleanName'] in crossBenchers and d['cleanName'] != s:
	# 		voteData.append(d)

	newlist2 = sorted(data[s]['voteData'], key=itemgetter('name')) 
	for value, group in groupby(newlist2, key=itemgetter('name')):
		print 'Group for value {}'.format(value)
		agreementData = {}
		agreementMeanList = []
		for d in group:
			print d
			agreementMeanList.append(d['agreement'])
		print agreementMeanList
		agreementMean = float("{0:.2f}".format(sum(agreementMeanList) / float(len(agreementMeanList))))	
		print agreementMean
		# print agreementMean
		currName = value.lower().replace(" ","_")
		if currName in crossBenchers:
			agreementData['agreement'] = agreementMean
			agreementData['name'] = value
			agreementData['cleanName'] = currName
			agreementData['shortName'] = crossInfo[currName]['shortName']
			agreementData['state'] = crossInfo[currName]['state']
			agreementData['party'] = crossInfo[currName]['party']
			if agreementData not in voteData and currName != s:
				# print agreementData
				voteData.append(agreementData)		

	print voteData
	newlist = sorted(data[s]['voteData'], key=itemgetter('party')) 
	for value, group in groupby(newlist, key=itemgetter('party')):
		# print 'Group for value {}'.format(value)
		agreementData = {}
		agreementMeanList = []
		for d in group:
			# print d
			agreementMeanList.append(d['agreement'])
		
		agreementMean = float("{0:.2f}".format(sum(agreementMeanList) / float(len(agreementMeanList))))	
		
		# print agreementMean

		agreementData['agreement'] = agreementMean
		agreementData['name'] = value
		agreementData['cleanName'] = value.lower().replace(" ","_")
		agreementData['state'] = ''
		agreementData['party'] = value
		agreementData['shortName'] = ''
		if agreementData['party'] in majorParties:
			agreementData['shortName'] = partyShortnames[agreementData['party']]
			voteData.append(agreementData)

	newData['voteData'] = voteData	
	# print voteData	

	jsonObj[s] = newData		

newJson = json.dumps(jsonObj, indent=4)
with open('crossbench-party-voting-final.json','w') as fileOut:
		fileOut.write(newJson)

