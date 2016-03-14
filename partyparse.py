import requests
import simplejson as json
from itertools import groupby
from operator import itemgetter

crossBenchers = ['jacqui_lambie_-_independent','jacqui_lambie_-_palmer_united_party','glenn_lazarus_-_independent','glenn_lazarus_-_palmer_united_party','david_leyonhjelm_-_liberal_democratic_party','john_madigan_-_democratic_labor_party','john_madigan_-_independent','ricky_muir_-_australian_motoring_enthusiast_party','nick_xenophon_-_independent','dio_wang_-_palmer_united_party','bob_day_-_family_first_party']

majorParties = ['Australian Labor Party', 'Australian Greens', 'Liberal Party','Country Liberal Party','National Party']
partyShortnames = {'Australian Labor Party':'ALP','Australian Greens':'Greens','Liberal Party':'LIB','National Party':'NAT','Country Liberal Party':'CLP'}


dataFile = open('party-voting-new.json')
data = json.load(dataFile)
crossFile = open('crossbencher-info.json')
crossInfo = json.load(crossFile)

jsonObj = {}

for s in crossBenchers:
	print s
	newData = {}
	newData['keyName'] = data[s]['keyName']
	newData['cleanKeyName'] = data[s]['cleanKeyName']
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
			if d['agreement'] != None:
				agreementMeanList.append(d['agreement'])
		print agreementMeanList
		if agreementMeanList:
			agreementMean = float("{0:.2f}".format(sum(agreementMeanList) / float(len(agreementMeanList))))	
			print agreementMean
			# print agreementMean
			currName = value.lower().replace(" ","_")
			if currName in crossBenchers:
				agreementData['agreement'] = agreementMean
				agreementData['name'] = value
				agreementData['cleanName'] = currName
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
			if d['agreement'] != None:
				agreementMeanList.append(d['agreement'])
		if agreementMeanList:
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

