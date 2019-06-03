# BootCampHomework03-2019-06-05

# Output: PyBank
```
Financial Analysis
----------------------------
Total Months: 86
Total: $38,382,578.00
Average  Change: $-2,315.12
Greatest Increase in Profits: Feb-2012 ($1,926,159.00)
Greatest Decrease in Profits: Sep-2013 ($-2,196,167.00)
```
## Notes on the assignment (for my own memory, mostly!):
* Code can be found inline below, and within the [`python-challenge` repo](https://github.com/ekenigsberg/BootCampHomework03-2019-06-05/tree/master/python-challenge/PyBank) replicated inside this formally-named repo
* The sample output in the assignment wasn't CSV-formatted, so I had Python create TXT output
* Note the currency formatting using thousands separators and two decimal places (as usual, [Stack Overflow](https://stackoverflow.com/questions/36626017/format-a-number-with-comma-separators-and-round-to-2-decimal-places-in-python-2) provided the single most helpful link)
* Computing average change was bit trickier than it would first seem:
  - the numerator is not the sum of the amounts (it's the sum of the **changes**)
  - the denominator is the number of months **minus one**
  - double-checking against Excel was helpful

# Output: PyPoll
```
ELECTION RESULTS
---------------------------------
TOTAL VOTES: 3,521,001
----------+---------+------------
CANDIDATE | PERCENT | TOTAL VOTES
Khan      |   63.0% |   2,218,231
Correy    |   20.0% |     704,200
Li        |   14.0% |     492,940
O'Tooley  |    3.0% |     105,630
----------+---------+------------
WINNER: Khan
---------------------------------
```
## Notes on the assignment:
* Code can be found inline below, and within the [`python-challenge` repo](https://github.com/ekenigsberg/BootCampHomework03-2019-06-05/tree/master/python-challenge/PyPoll) replicated inside this repo
* I gussied up the output by aligning text values with `ljust()` and numeric values with `rjust()`
* If the column headers are changed, the rest of the table dynamically resizes itself:
   ```python
   strHeads = ['CANDIDATE ', ' PERCENT ', ' TOTAL VOTES']
   intHeadLens = [len(str) for str in strHeads]
   ```
* The table borders are generated with a simple function
  - I started to fiddle with drawing the borders using [UTF8 box borders](https://stackoverflow.com/questions/46063974/printing-extended-ascii-characters-in-python)\-\-it requires adding an `encoding=UTF-8` parameter to the `open()` function\-\-but I couldn't get it to work quite right, so I set it aside.
* More credit to Stack Overflow for [an efficient answer](https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary/280156#280156) to "How do I show the key tied to the max value in a dictionary?"
* Wow, keeping running totals with a dictionary is really efficient

# Code: PyBank
```python
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
#          2) the denominator for Average Change is Total Months minus 1
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
```

# Code: PyPoll
```python
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
    txtSummOut.write(                   # write top of table
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
    txtSummOut.write(                   # write bottom of table
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
```
