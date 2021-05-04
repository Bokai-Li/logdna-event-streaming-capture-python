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
os.system("ibmcloud ks cluster config --cluster c1v3hlid03o6k0tq1vq0")
os.system("kubectl delete -f kafka-java-console-sample.yaml")
time.sleep(10)
os.system("kubectl create -f kafka-java-console-sample.yaml")
time.sleep(10)
missing=["missing:"]
summary=[["Success Rate", "total jobs", "caputured","missing","latency<15s","latency>30s"]]
table=[["Job ID","found", "total", "avg latency", "max latency", "min latency"]]
latency=[]
pattern1 = "INFO Message timestamp: ts\((.*?)\),"
pattern2 = "\.ts\((.*?)\) JOB"
i = -1
while(True):
    i+=1
    #report summary and reset
    if(i%480==0):
        missing=[]
        with open("report.txt","r") as fp:
            for line in fp:
                if "missing" in line:
                    missing=line.split()[1:]
        table=[["Job ID","found", "total", "avg latency", "max latency", "min latency"]]
        latency=[]
        pattern1 = "INFO Message timestamp: ts\((.*?)\),"
        pattern2 = "\.ts\((.*?)\) JOB"
        os.system("kubectl logs kafka-java-console-sample > total.log")
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
        #summary
        missing=[]
        with open("report.txt","r") as fp:
            for line in fp:
                if "missing" in line:
                    missing=line.split()[1:]
        missing2=[]
        with open("missReport.txt","r") as fp:
            for line in fp:
                if "missing" in line:
                    missing2=line.split()[1:]
        file = open("report.txt", "r")
        line_count = 0
        for line in file:
            if line != "\n":
                line_count += 1
        file.close()
        totalJobs=line_count-4
        missingIn15s=len(missing)
        stillMissing=len(missing2)
        percentage=(totalJobs-stillMissing)/totalJobs*100
        entry = [percentage, totalJobs,totalJobs-stillMissing,stillMissing,totalJobs-missingIn15s,missingIn15s-stillMissing]
        summary.append(entry)
        with open('summary.txt', 'w') as f:
            f.write(tabulate(summary))
        #reset
        os.rename('report.txt','report'+str(i/480)+'.txt')
        os.rename('missReport.txt','missReport'+str(i/480)+'.txt')
        os.system("kubectl delete -f kafka-java-console-sample.yaml")
        time.sleep(10)
        os.system("kubectl create -f kafka-java-console-sample.yaml")
        time.sleep(10)
        missing=["missing:"]
        table=[["Job ID","found", "total", "avg latency", "max latency", "min latency"]]
        latency=[]

    # submit a job to API that logs to logDNA
    result = subprocess.run(['curl', '-s', '150.238.252.215:31001/50'], stdout=subprocess.PIPE)
    jobText=result.stdout.decode('utf-8')
    print(jobText)
    jobNo=jobText.split(":",1)[1][:-1]
    # # wait and get event stream consumer log
    time.sleep(15)

    os.system("kubectl logs kafka-java-console-sample --since=3m > app.log")
    alertNo=1
    found=False
    count=0
    entry=["JOB"+str(jobNo)]
    latency=[]
    while(alertNo<=50):
        id = "JOB"+str(jobNo)+"NO"+str(alertNo)+"End"
        with open("app.log","r") as fp:
            for line in fp:
                if id in line:
                    found=True
                    ts1 = re.search(pattern1, line).group(1)
                    ts2 = re.search(pattern2, line).group(1)
                    latency.append(int(ts1)-int(ts2))
                    count+=1
        if(not found):
            missing.append("JOB"+str(jobNo))
            found=True
        alertNo+=1
    entry.append(str(count))
    entry.append("/50")
    entry.append(avg(latency))
    entry.append(cmax(latency))
    entry.append(cmin(latency))
    table.append(entry)
    table.append(missing)
    with open('report.txt', 'w') as f:
        f.write(tabulate(table))
    table.remove(missing)
