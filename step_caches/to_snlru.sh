for ((i = $1; i <= $2; i++))
do
echo "Generating SNLRU output number $i"
./SNLRU ../step_genout/gen_out/out_test$i.txt $3 $4 0.56 0.44 > ./snlru_out/snlru_out$i.txt
done
