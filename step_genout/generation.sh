cd ../scache
for ((i = $1; i <= $2; i++))
do
echo "Generating request number $i"
./generator ../step_ini/gen_ini/test$i.ini ../table.json $3 ../step_genout/gen_out/out_test$i.txt dsf
done
echo ""
cd ../step_genout
