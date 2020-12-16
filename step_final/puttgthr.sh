cd ../step_ini
echo "Started phase 1"
python3 ini_gen.py $1 1 4 100
echo "Ended phase 1"
cd ../step_genout
echo "Started phase 2"
bash generation.sh $1
echo "Ended phase 2"
cd ../step_caches
echo "Started phase 3"
bash to_lru.sh $1
echo "Ended phase 3"
echo "Started phase 4"
bash to_scache.sh $1
echo "Ended phase 4"
cd ../step_final
echo "Started final phase"
python3 compare.py $1
echo "That's all!"