for ((i = $1; i <= $2; i++))
do
echo "Generating segment LRU output number $i"
./lru2 ../step_genout/gen_out/out_test$i.txt $3 $4 $5 > ./lru2_out/lru2_out$i.txt
done
