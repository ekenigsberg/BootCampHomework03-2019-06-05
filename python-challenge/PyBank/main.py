import os
import csv

# declare vars: iteration helper
fltPrevAmt = 0
# declare vars: totals
fltTotalAmt = 0
fltTotalChg = 0
intTotalMos = 0
# declare vars: max and min change
strMaxMo = ''
strMinMo = ''
fltMax = 0
fltMin = 0

# open CSV
strDataIn = os.path.join("Resources", "budget_data.csv")
with open(strDataIn, newline='') as csvDataIn:
	crData = csv.reader(csvDataIn, delimiter = ',')
	next(crData)
	# iterate through budget rows
	for row in crData:
		# update totals. NOTE: Total Change starts in SECOND month
		fltTotalAmt += float(row[1])
		if intTotalMos > 0:
			fltTotalChg += float(row[1]) - fltPrevAmt
		intTotalMos += 1
		# is new max change? update "max" vars
		if fltMax < float(row[1]) - fltPrevAmt:
			strMaxMo = row[0]
			fltMax = float(row[1]) - fltPrevAmt
		# is new min change? update "min" vars
		if fltMin > float(row[1]) - fltPrevAmt:
			strMinMo = row[0]
			fltMin = float(row[1]) - fltPrevAmt
		# set the lagging "previous month Amount" var
		fltPrevAmt = float(row[1])

# write results to file. The sample output shown in the instructions isn't 
# CSV-formatted, so I did it with ordinary file-outputting instead, for kicks.
# GOTCHAS: 1) Total Change does NOT equal Total Amount
# 		   2) the denominator for Average Change is Total Months minus 1
strSummOut = os.path.join("budget_summary.txt")
with open(strSummOut, 'w', newline='') as txtSummOut:
	txtSummOut.write(
		'Financial Analysis\n' +
		'----------------------------\n' +
		f'Total Months: {intTotalMos}\n' +
		f'Total: ${fltTotalAmt:,.2f}\n' +
		f'Average  Change: ${fltTotalChg/(intTotalMos - 1):,.2f}\n' +
		f'Greatest Increase in Profits: {strMaxMo} (${fltMax:,.2f})\n' +
		f'Greatest Decrease in Profits: {strMinMo} (${fltMin:,.2f})')

# output the freshly-created text file to screen
print() # spacer
strSummIn = strSummOut
with open(strSummIn, 'r', newline='\r\n') as txtSummIn:
	for line in txtSummIn:
		print(line)
print() # spacer