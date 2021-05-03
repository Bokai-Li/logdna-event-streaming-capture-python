from tabulate import tabulate
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
summary=[["total jobs", "caputured","missing","latency<15s","latency>30s"]]
totalJobs=line_count-4
missingIn15s=len(missing)
stillMissing=len(missing2)
percentage=(totalJobs-stillMissing)/totalJobs*100
entry = [totalJobs,totalJobs-stillMissing,stillMissing,totalJobs-missingIn15s,missingIn15s-stillMissing]
summary.append(entry)
with open('summary.txt', 'w') as f:
    f.write(tabulate(summary))
    f.write("\nSuccess rate for jobs:"+str(percentage)+"%\n")
