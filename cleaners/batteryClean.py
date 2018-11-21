###############################################################
## batteryclean.py for systemMon.py 
## last updated 20.11.2018  20:20
## purpose : use machineID from machineTagger.py to make uniquelogID
## authors: luckyducky + lamehacker + cpitts
################################################################

import csv
import re
import pandas as pd

#function to define structure of logID
def format_logId():
    if log_count <= 9 and log_count >= 0:
        placeholder='000'
    elif log_count <=99 and log_count >=10:
        placeholder='00'
    elif log_count > 99:
        placeholder='0'
        
    a=(captureTime[1])
    date=a[13:23]    
    uniqueLogId.append(machineID + str(date) + '['+ placeholder +str(log_count) + ']')


# for holding purposes manually entering machine ID from preferences (needs to be entered as a string)
machineID = 'enter machineID from machineTracker.py'
captureTime = ['timeStamp']
supported = ['supported']
detected = ['detected']
charge = ['charge']
remaining = ['remaining']
status = ['status']
plugged = ['plugged']
uniqueLogId=['LogID'] 


i = 10
log_count = 0
#using with open (not f=open) for error reduction. with open also automatically closes file
with open('battery.log') as f:
    for line in f:
    # passes '<log>' #the lines below within if and elif i==int pull into lists based on string of tags
    # if you examine battery.log you will see that the row number i == int -> string.append is matched with above defined variables
        if str(line).startswith('<log>') == True:
            i = 1
            continue
        if str(line).startswith('</log>') == True:
            log_count += 1
            format_logId()
            i = 8
            continue
        if i == 1:
            captureTime.append(line)
        elif i == 2:
            supported.append(line)
        elif i == 3:
            detected.append(line)
        elif i == 4:
            charge.append(line)
        elif i == 5:
            remaining.append(line)
        elif i == 6:
            status.append(line)
        elif i == 7:
            plugged.append(line)
        i += 1


# creates dataframe using list(zip('name of lists to be zipped into dataFrame'))
df = pd.DataFrame(list(zip(uniqueLogId, captureTime, supported, detected, charge, remaining, status, plugged)))

# defining items for regex to remove from dataframe
stuffToIgnore = ['<captureTime>', '</captureTime>',
                 '<supported>', '</supported>',
                 '<detected>', '</detected>',
                 '<charge>', '</charge>',
                 '<status>', '</status>',
                 '<plugged>', '</plugged>',
                 '<remaining>', '</remaining>',
                 '\n']
# regex removing items per defined in stuffToIgnore
for stuff in stuffToIgnore:
    df = df.replace(stuff, "", regex=True)

df.to_csv('battery.csv', index=False, header=False)

# for visual inspection - not needed for funcionatlity
print(df)
