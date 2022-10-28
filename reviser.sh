iterator=0
while [ $iterator -lt 684 ]
do
    python reviser.py /mnt/yrfs/glm_data/zhihu_WangYC/post_split/zhihu_${iterator}_qa.jsonl
    iterator=$[${iterator}+1]