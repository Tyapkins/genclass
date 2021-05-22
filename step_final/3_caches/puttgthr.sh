echo "Generation for 3 caches"
cd ..
bash put_ini.sh $1 $2 100
bash put_gen.sh $1 $2 $3 $4
cd 3_caches
bash put_lru.sh $1 $2 $3 $4
bash put_lru2.sh $1 $2 $3 $4 0.15
bash put_snlru.sh $1 $2 $3 $4

