echo "Started final phase"
python3 2_caches.py $1 $2 $3
python3 compare.py $1 $2 $3
echo "That's all!"
