kubectl logs kafka-java-console-sample --since=5m > app.log
alertNo=1
count=0
for VARIABLE in `seq 1 $2`
do
    if grep -q "JOB${1}NO${alertNo}" "./app.log"; then
        echo "Found: JOB${1}NO${alertNo}"
        ((count+=1))
    else
        echo "Missing: JOB${1}NO${alertNo}"
    fi
    ((alertNo+=1))
done
echo ${count}/${2}
