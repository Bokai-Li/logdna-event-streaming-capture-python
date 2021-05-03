#ibmcloud ks cluster config --cluster c1v3hlid03o6k0tq1vq0
output=$(curl -s 150.238.252.215:31001/$1)
echo $output
IFS=":" read text jobNo <<< "$output"
kubectl logs kafka-java-console-sample --since=1m > app.log
alertNo=1
count=0
echo $1
for VARIABLE in `seq 1 $1`
do
    if grep -q "Alert:JOB${jobNo}NO${alertNo}" "./app.log"; then
        echo "Found: Alert:JOB${jobNo}NO${alertNo}"
        ((count+=1))
    else
        echo "Missing: Alert:JOB${jobNo}NO${alertNo}"
    fi
    ((alertNo+=1))
done
echo ${count}/${1}
