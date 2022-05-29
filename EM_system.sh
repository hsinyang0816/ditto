# Download resource
[ -f blocker_model/pytorch_model.bin ] && echo "Model exists" || wget -O blocker_model/pytorch_model.bin 'https://www.dropbox.com/s/y9bmtj0kbzzi6zo/pytorch_model.bin?dl=1'
[ -f checkpoints/Structured/Amazon-Google/model.pt ] && echo "Model exists" || wget -O checkpoints/Structured/Amazon-Google/model.pt 'https://www.dropbox.com/s/79xil3arrq1vdn3/model.pt?dl=1'
# Transform csv to txt
python3 blocking/csv2txt.py --csv $1 --txt blocking/input/table_A.txt
python3 blocking/csv2txt.py --csv $2 --txt blocking/input/table_B.txt
# Blocker
echo "-----------------------------------------------------  Start Blocking  -----------------------------------------------------"
CUDA_VISIBLE_DEVICES=0 python3 blocking/blocker.py  --input_path blocking/input/  --left_fn table_A.txt  --right_fn table_B.txt  --output_fn ../../input/candidates.jsonl  --model_fn blocker_model  --k 5
# Matcher
echo "-----------------------------------------------------  Start Matching  -----------------------------------------------------"
CUDA_VISIBLE_DEVICES=0 python3 matcher.py  --task Structured/Amazon-Google  --input_path input/candidates.jsonl  --output_path $3  --lm roberta  --max_len 128  --use_gpu  --fp16  --checkpoint_path checkpoints/
