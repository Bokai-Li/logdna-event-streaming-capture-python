sum=0
count3 = 0
for i in range(1,31):
    file1 = open('missReport'+str(i)+'.0.txt', 'r')
    Lines = file1.readlines()
    count1 = 0
    count2 = 0
    count5 = 0
    # Strips the newline character
    for line in Lines:
        if "2021" in line:
            latency = line.split()[5]
            if float(latency)<30000:
                count1+=1
            elif float(latency)<120000:
                count2+=1
            else:
                count5+=1
            sum+=float(latency)
            count3+=1
    print(count1, count2, count5)
print(sum/count3)

