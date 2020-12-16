cd ../scache
for ((i = 0; i <= $1; i++))
do
echo "Generating Scache output number $i"
./scache 56G 10 0 1 15 96 ../table.json ../step_genout/gen_out/out_test$i.txt > ../step_caches/scache_out/scache_out$i.txt
done
cd ../step_caches