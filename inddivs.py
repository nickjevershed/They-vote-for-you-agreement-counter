#coding: utf8

import requests
import unicodecsv as csv
import simplejson as json
from datetime import date, timedelta, datetime
import os

OA_KEY = os.environ['OA_THEYVOTEFORYOU']

crossBenchers = ['jacqui_lambie','glenn_lazarus','david_leyonhjelm','john_madigan','ricky_muir','nick_xenophon','dio_wang','bob_day']
coalitionParties = ['Liberal Party','Country Liberal Party','National Party']

divFile = open('divisiondata.json')
divisions = json.load(divFile)
divisionIds = divisions['divisionIds']

divFile.close()

#Make a list of current senator IDs to check 

totalAgreement = {}

#Get all possible senators

divNames = []

baseUrl = 'https://theyvoteforyou.org.au/divisions/senate/'

with open('all-vote-positions.csv', 'w') as csvoutput:
	writer = csv.writer(csvoutput, lineterminator='\n')
	headers = ['voteId','title','url','date','time','turnout','govWins']
	for pol in crossBenchers:
		headers.append(pol)

	writer.writerow(headers)

	for id in divisionIds:
		print "Division", 'https://theyvoteforyou.org.au/api/v1/divisions/{id}.json?key={key}'.format(id=id,key=OA_KEY)
		fileLoc = 'votejson/{id}.json'.format(id=id)
		with open(fileLoc,'r') as jsonFile:
			votes = json.load(jsonFile)

			url = baseUrl + votes['date'] + "/" + str(votes['number'])
			print url

			totalVotes = votes['aye_votes'] + votes['no_votes'] * 1.0
			print "totalVotes", totalVotes
			possibleVotes = votes['possible_turnout'] * 1.0
			print "possibleVotes", possibleVotes
			turnout = round(((totalVotes / possibleVotes) * 100),1)
			print "turnout", turnout
			majorityNeeded = round((totalVotes/2.0))
			print "majorityNeeded", majorityNeeded
			ayeVotes = votes['aye_votes']
			print "aye_votes", ayeVotes
			noVotes = votes['no_votes']
			print "noVotes", noVotes
			if ayeVotes >= majorityNeeded:
				voteStatus = 'aye'
			elif noVotes >= majorityNeeded:
				voteStatus = 'no'	

			print "voteStatus", voteStatus	

			crossBencherResults = [id,votes['name'],url,votes['date'],votes['clock_time'],turnout]

			senatorsPresent = []
			for vote in votes['votes']:
				voteName = (vote['member']['first_name'] + "_" + vote['member']['last_name']).lower()
				senatorsPresent.append(voteName)
			# print senatorsPresent
			

			#Get government position		

			govPositions = []

			for vote in votes['votes']:
				# print vote
				voteParty = vote['member']['party']
				if voteParty in coalitionParties:
					position = vote['vote']
					if position == 'aye':
						govPositions.append(1)
					elif position == 'no':
						govPositions.append(0)	

			print govPositions
			govMeanPosition = sum(govPositions) / float(len(govPositions))			
			if govMeanPosition > 0.5:
				govPositionStr = 'aye'

			elif govMeanPosition < 0.5:
				govPositionStr = 'no'

			if govPositionStr == voteStatus:
				govWins = 'gov_wins'
			else:
				govWins = 'gov_loses'			 		

			print "govPositionStr", govPositionStr	
			print "govWins", govWins

			crossBencherResults.append(govWins)

			#Get labor position		

			labPositions = []

			for vote in votes['votes']:
				# print vote
				voteParty = vote['member']['party']
				if voteParty == 'Australian Labor Party':
					position = vote['vote']
					if position == 'aye':
						labPositions.append(1)
					elif position == 'no':
						labPositions.append(0)	

			print labPositions
			labMeanPosition = sum(labPositions) / float(len(labPositions))			
			if labMeanPosition > 0.5:
				labPositionStr = 'aye'

			elif labMeanPosition < 0.5:
				labPositionStr = 'no'	

			print "labPositionStr", labPositionStr	
			
			#Get green position

			grnPositions = []

			for vote in votes['votes']:
				# print vote
				voteParty = vote['member']['party']
				if voteParty == 'Australian Greens':
					position = vote['vote']
					if position == 'aye':
						grnPositions.append(1)
					elif position == 'no':
						grnPositions.append(0)	

			print grnPositions
			grnMeanPosition = sum(grnPositions) / float(len(grnPositions))			
			if grnMeanPosition > 0.5:
				grnPositionStr = 'aye'

			elif grnMeanPosition < 0.5:
				grnPositionStr = 'no'	

			print "grnPositionStr", grnPositionStr	

			

			for pol in crossBenchers:
				if pol in senatorsPresent:
					print pol, "present"

					#Get crossbenchers position

					for vote in votes['votes']:
						# print vote
						voteName = (vote['member']['first_name'] + "_" + vote['member']['last_name']).lower()
						if pol == voteName:
							senatorPosition = vote['vote']
							print voteName, "position was", senatorPosition

							if senatorPosition == govPositionStr:
								crossBencherResults.append("government")
							elif senatorPosition == labPositionStr:
								crossBencherResults.append("labor")
							elif senatorPosition == grnPositionStr:
								crossBencherResults.append("greens")
							else:
								crossBencherResults.append("independent")	
				else:
					crossBencherResults.append("absent")			
			
			writer.writerow(crossBencherResults)		