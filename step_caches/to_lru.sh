for ((i = $1; i <= $2; i++))
do
echo "Generating LRU output number $i"
./lru ../step_genout/gen_out/gen_out/out_test$i.txt $3 $4 > ./lru_out/lru_out$i.txt
done
