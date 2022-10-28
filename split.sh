# split.sh用于分割清洗好的jsonl文件
# 使用方式 bash split.sh $src_filename
# by WangYC
# frederickwang99@gmail.com
# Oct.2nd 2022

batch_size=10000 #指定每个文件多少个json块
src_filename=$1 #answer_comment.jsonl
dst_dir='./post_split_ac/'
dst_name='ac'

echo "split begin"

function floor_it(){
    floor=`echo "scale=0;$1/1"|bc -l ` # 向下取整
    echo $floor
}

function ceil_it(){
    floor=`echo "scale=0;$1/1"|bc -l ` # 向下取整
    add=`awk -v num1=$floor -v num2=$1 'BEGIN{print(num1<num2)?"1":"0"}'`
    echo `expr $floor  + $add`
}

iteration=0
tail_num=1

echo counting lines of ${src_filename}
line_num_total=$(cat ${src_filename} |wc -l)
echo total lines of ${src_filename} is: ${line_num_total}

total_iteration=$[${line_num_total}/16/$batch_size]
echo total_iteration: $total_iteration
ceil_iteration=$(ceil_it $total_iteration)
echo ceil_iteration: $ceil_iteration
while [ $iteration -lt $[${ceil_iteration}+1] ]
do
    cat ${src_filename} |tail -n +$tail_num |head -n $[${batch_size}*16] >> ${dst_dir}/zhihu_${iteration}_${dst_name}.jsonl
    python reviser.py ${dst_dir}/zhihu_${iteration}_${dst_name}.jsonl
    echo -e "\r iteration $iteration, total: $[${ceil_iteration}+1] \c"
    iteration=$[${iteration}+1]
    tail_num=$[${tail_num}+$[${batch_size}*16]]
done
echo -e "split done"
