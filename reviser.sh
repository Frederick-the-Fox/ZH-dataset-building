iterator=0
total_num=684
echo "revise begin"
while [ $iterator -lt $total_num ]
do
    python reviser.py /mnt/yrfs/glm_data/zhihu_WangYC/post_split_ac/zhihu_${iterator}_ac.jsonl
    iterator=$[${iterator}+1]
    echo -e "\rtotal iteration: $total_num, this is iteration $iterator"

echo "revise done"