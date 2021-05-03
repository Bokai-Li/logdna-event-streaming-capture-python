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
table=[["Job ID","found", "total", "avg latency"]]
latency=[]
pattern1 = "INFO Message timestamp: ts\((.*?)\),"
pattern2 = "\.ts\((.*?)\) JOB"
# os.system("kubectl logs kafka-java-console-sample > total.log")
with open('total.log') as fp:
     for line in fp:
         for jobNo in missing:
             if jobNo+"NO" in line:
                 entry=[jobNo]
                 ts1 = re.search(pattern1, line).group(1)
                 ts2 = re.search(pattern2, line).group(1)
                 entry.append(int(ts1)-int(ts2))
                 missing.remove(jobNo)
                 table.append(entry)
                 continue;
table.append(missing)
with open('missReport.txt', 'w') as f:
    f.write(tabulate(table))
