echo "Generation for 2 caches"
cd ..
bash put_ini.sh $1 $2 100
bash put_gen.sh $1 $2 $3 $4
cd 2_caches
bash put_lru.sh $1 $2 $3 $4
bash put_lru2.sh $1 $2 $3 $4 0.15


