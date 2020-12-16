for ((i = 0; i <= $1; i++))
do
echo "Generating LRU output number $i"
../scache/lru 56G ../step_genout/gen_out/out_test$i.txt > ./lru_out/lru_out$i.txt
done
