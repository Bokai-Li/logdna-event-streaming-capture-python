missing=[]
with open("report.txt","r") as fp:
    for line in fp:
        if "missing" in line:
            missing=line.split()[1:]

import os
import time
import subprocess
from tabulate import tabulate
import re
def avg(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)
def cmax(lst):
    if len(lst) == 0:
        return 0
    return max(lst)
def cmin(lst):
    if len(lst) == 0:
        return 0
    return min(lst)
table=[["Job ID","found", "total", "avg latency", "max latency", "min latency"]]
latency=[]
pattern1 = "INFO Message timestamp: ts\((.*?)\),"
pattern2 = "\.ts\((.*?)\) JOB"
#os.system("kubectl logs kafka-java-console-sample > total.log")
foundArray=[]
for jobNo in missing:
    print(missing)
    print("finding "+jobNo)
    alertNo=1
    count=0
    entry=[jobNo]
    latency=[]
    while(alertNo<=50):
        id = jobNo+"NO"+str(alertNo)+"End"
        with open("total.log","r") as fp:
            for line in fp:
                if id in line:
                    found=True
                    ts1 = re.search(pattern1, line).group(1)
                    ts2 = re.search(pattern2, line).group(1)
                    latency.append(int(ts1)-int(ts2))
                    count+=1
        alertNo+=1
        if count==50:
            print("found"+jobNo)
            foundArray.append(jobNo)
    entry.append(str(count))
    entry.append("/50")
    entry.append(avg(latency))
    entry.append(cmax(latency))
    entry.append(cmin(latency))
    table.append(entry)
for jobNo in foundArray:
    missing.remove(jobNo)
missing.insert(0,"missing")
table.append(missing)
with open('missReport.txt', 'w') as f:
    f.write(tabulate(table))
