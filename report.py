import os
import time
import subprocess
from tabulate import tabulate
import re
from datetime import datetime

def convertDateTime(timestamp):
    dt_object = datetime.fromtimestamp(timestamp/1000)
    return dt_object

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
os.system("kubectl create -f kafka-java-console-sample.yaml")
missing=["missing:"]
summary=[["Last job Time Stamp in UTC","Success Rate", "total jobs", "caputured","missing","<15s", "<120s",">120s","avg latency"]]
table=[["Job ID","found", "total", "avg latency", "max latency", "min latency"]]
latency=[]
pattern1 = "INFO Message timestamp: ts\((.*?)\),"
pattern2 = "\.ts\((.*?)\) JOB"
i = -1
totalJobs=0
ts2=0
#for latency
count0=0
count1=0
count2=0
count3=0
sumLatency=0

while(True):
    i+=1
    #report summary and reset
    if(i%400==0 and i!=0):
        time.sleep(180)
        missing=[]
        with open("report.txt","r") as fp:
            for line in fp:
                if "missing" in line:
                    missing=line.split()[1:]
        table=[["Job ID","Time Stamp in UTC", "found", "total", "avg latency", "max latency", "min latency"]]
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
            while(alertNo<=100):
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
                if count>=100:
                    print("found"+jobNo)
                    foundArray.append(jobNo)
            if(not ts2):
                ts2=0
            entry.append(convertDateTime(int(ts2)))
            entry.append(str(count))
            entry.append("/100")
            entry.append(avg(latency))
            entry.append(cmax(latency))
            entry.append(cmin(latency))
            table.append(entry)
        for jobNo in foundArray:
            if jobNo in missing:
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
                if "2021" in line:
                    latency = line.split()[5]
                    if float(latency)<30000:
                        count0+=1
                    elif float(latency)<120000:
                        count1+=1
                    else:
                        count2+=1
                    sumLatency+=float(latency)
                    count3+=1
        file = open("report.txt", "r")
        line_count = 0
        for line in file:
            if line != "\n":
                line_count += 1
        file.close()
        # totalJobs=line_count-4
        missingIn10s=len(missing)
        stillMissing=len(missing2)
        percentage=(totalJobs-stillMissing)/totalJobs*100
        entry = [convertDateTime(int(ts2)), percentage, totalJobs,totalJobs-stillMissing,stillMissing,count0,count1,count2,sumLatency/count3]
        summary.append(entry)
        with open('summary.txt', 'w') as f:
            f.write(tabulate(summary))
        #reset
        totalJobs=0
        os.rename('report.txt','report'+str(i/400)+'.txt')
        os.rename('missReport.txt','missReport'+str(i/400)+'.txt')
        os.system("ibmcloud ks cluster config --cluster c1v3hlid03o6k0tq1vq0")
        os.system("kubectl delete -f kafka-java-console-sample.yaml")
        os.system("kubectl create -f kafka-java-console-sample.yaml")
        missing=["missing:"]
        table=[["Time Stamp in UTC","Job ID","found", "total", "avg latency", "max latency", "min latency"]]
        latency=[]
        count0=0
        count1=0
        count2=0
        count3=0
        sumLatency=0

    # submit a job to API that logs to logDNA
    result = subprocess.run(['curl', '-s', '150.238.252.215:31001/100'], stdout=subprocess.PIPE)
    jobText=result.stdout.decode('utf-8')
    print(jobText)
    jobNo=jobText.split(":",1)[1][:-1]
    # # wait and get event stream consumer log
    time.sleep(1)

    missing.append("JOB"+str(jobNo))
    totalJobs+=1
    table.append(missing)
    with open('report.txt', 'w') as f:
        f.write(tabulate(table))
    table.remove(missing)
