iteration=0
batch_size=100000
tail_num=1
src_filename=$1

function floor_it(){
    floor=`echo "scale=0;$1/1"|bc -l ` # 向下取整
    echo $floor
}

function ceil_it(){
    floor=`echo "scale=0;$1/1"|bc -l ` # 向下取整
    add=`awk -v num1=$floor -v num2=$1 'BEGIN{print(num1<num2)?"1":"0"}'`
    echo `expr $floor  + $add`
}

line_num_total=$(cat ${src_filename} |wc -l)
echo counting lines of ${src_filename}
echo total lines of ${src_filename} is: ${line_num_total}

total_iteration=$[${line_num_total}/16/$batch_size]
echo total_iteration: $total_iteration
ceil_iteration=$(ceil_it $total_iteration)
echo ceil_iteration: $ceil_iteration
while [ $iteration -lt $[${ceil_iteration}+1] ]
do
    cat ${src_filename} |tail -n +$tail_num |head -n $[${batch_size}*16] >> ./post_split/zhihu_qa_${iteration}.jsonl
    iteration=$[${iteration}+1]
    tail_num=$[${tail_num}+$[${batch_size}*16]]
done