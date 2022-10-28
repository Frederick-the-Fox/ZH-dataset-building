# 使用方法：bash run.sh answer_comment.jsonl
src_filename=$1
cmd="bash split.sh $src_filename 2>&1 | tee ./logs/split_log.txt"

echo $cmd
eval $cmd