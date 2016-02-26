import requests
import simplejson as json
from datetime import date, timedelta, datetime
import os

OA_KEY = os.environ['OA_THEYVOTEFORYOU']
polFile = open('people.json')
politicians = json.load(polFile)
startDate = datetime.strptime("2013-11-13", "%Y-%m-%d")
todaysDate = datetime.now()
daysDiff = (todaysDate - startDate).days

divisionIds = []

for x in xrange(0, daysDiff):
	print x
	queryDate = startDate + timedelta(days=x)
	queryDateStr = datetime.strftime(queryDate, '%Y-%m-%d')
	baseUrl = 'https://theyvoteforyou.org.au/api/v1/divisions.json?house=senate&key={key}&start_date={queryDateStr}&end_date={queryDateStr}'.format(queryDateStr=queryDateStr,key=OA_KEY)
	print "checking", baseUrl
	r = requests.get(baseUrl, verify=False)
	rJson = r.json()
	print "length: ",len(rJson)
	for d in rJson:
		print "adding Ids"
		divisionIds.append(d['id'])

print divisionIds		