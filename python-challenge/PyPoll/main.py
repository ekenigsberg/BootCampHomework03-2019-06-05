import os
import csv

# declare vote count dictionary
dictVotes = {}
# declare string vars: Candidate, Count, and Percent
strCan = ''
strCnt = ''
strPct = ''
# declare vars: define summary table headers, and compute lengths of headers.
#               make each header wider than any value in that column.
strHeads = ['CANDIDATE ', ' PERCENT ', ' TOTAL VOTES']
intHeadLens = [len(str) for str in strHeads]
# declare function that spits out formatting rows for summary table
def BorderRow(strChar = '-'):
	strRow = ('-' * intHeadLens[0] + strChar + 
			  '-' * intHeadLens[1] + strChar + 
			  '-' * intHeadLens[2])
	return strRow
	
# open CSV
strDataIn = os.path.join("Resources", "election_data.csv")
with open(strDataIn, newline='') as csvDataIn:
	crData = csv.reader(csvDataIn, delimiter = ',')
	next(crData)
	# collect all candidate names and votes
	for row in crData:
		strCan = row[2]
		if strCan in dictVotes:    # is candidate already in dict?
			dictVotes[strCan] += 1 # if yes: increment candidate's count
		else:
			dictVotes[strCan] = 1  # if no: add row to dict
# print(dictVotes)                 # unrem for debugging

# write results to file (txt, not csv!)
strSummOut = os.path.join("election_summary.txt")
lngAllVotes = sum(dictVotes.values())  # sum up all votes
with open(strSummOut, 'w', newline='') as txtSummOut:
	txtSummOut.write(				   # write top of table
		'ELECTION RESULTS\n' +
		BorderRow() + '\n' +
		f'TOTAL VOTES: {lngAllVotes:,}\n' +
		BorderRow('+') + '\n' +
		f'{strHeads[0]}|{strHeads[1]}|{strHeads[2]}\n')
	for key, val in dictVotes.items(): # iterate through dictVotes
		strCan = key
		strPct = '{:,.1f}'.format(val / lngAllVotes * 100) + '% '
		strCnt = '{:,}'.format(val)
		# write candidate line with pipe char between columns
		txtSummOut.write(
			strCan.ljust(intHeadLens[0]) + '|' +
			strPct.rjust(intHeadLens[1]) + '|' +
			strCnt.rjust(intHeadLens[2]) + '\n')
	txtSummOut.write(				   # write bottom of table
		BorderRow('+') + '\n' +
		f'WINNER: {max(dictVotes, key=dictVotes.get)}\n' + # bitly.com/pymaxval
		BorderRow())

# output the freshly-created text file to screen
print() # spacer
strSummIn = strSummOut
with open(strSummIn, 'r', newline='\r\n') as txtSummIn:
	for line in txtSummIn:
		print(line)
print() # spacer