###############################################################################
# Cleaner for: systemMon.py
# Name: bootClean.py
#
# Author: LuckyDucky (https://github.com/itsalways5am), calebpitts, lamehacker
#
# Updated: Sun 2018-11-20 12:00
###############################################################################
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
    uniqueLogId.append(machineID+'-'+str(date)+ '[' + placeholder +str(log_count) + ']')

machineID= 'enter machineID from machineTracker.py'
captureTime = ['TimeStamp']
osFamily = ['OSFamily']
osRelease = ['OSRelease']
osPlatform = ['OSPlatform']
osDescription = ['OSDescription']
bootTime = ['BootTime']
uniqueLogId=['LogID']    

i = 10
log_count = 0
with open('bootTime.log') as f:
        
        for line in f:
            if line.startswith('<log>') == True:
                i = 1
                log_count += 1
                continue
            elif line.startswith('</log>') == True:
                format_logId()
                i = 7
                continue
                
            if i == 1:
                captureTime.append(line)
            elif i == 2:
                osFamily.append(line)
            elif i == 3:
                osRelease.append(line)
            elif i == 4:
                 osPlatform.append(line)
            elif i == 5:
                    osDescription.append(line)
            elif i == 6:
                    bootTime.append(line)
            i += 1

df = pd.DataFrame(list(zip(uniqueLogId, captureTime,bootTime, osFamily, osRelease, osPlatform, osDescription)))


stuffToIgnore = ['<captureTime>', '</captureTime>',
                 '<osFamily>', '</osFamily>',
                 '<osRelease>', '</osRelease>',
                 '<osPlatform>', '</osPlatform>',
                 '<osDescription>', '</osDescription>',
                 '<bootTime>', '</bootTime>',
                 '\n']

for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex=True)


df.to_csv('bootTime.csv', index=False, header=False)

print(df)


