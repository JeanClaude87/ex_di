#!/bin/bash

rm -f script_wait.sh
python setup.py build_ext --inplace

printf "%s\n" "#!/bin/bash" >> script_wait.sh

LL=(18)
DD=(1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0)
nr=(1)

lenl=${#LL[@]%.*} 
lend=${#DD[@]%.*} 

for((i=0; i<$lenl; i++))
	do
	L=${LL[i]}

	for((j=0; j<$lend; j++))
		do
		D=${DD[j]}
	
		echo $L $D ${nr[i]}

		for((n_real=0; n_real<${nr[i]}; n_real++))
			do
		
			sed -e "s/LLL/$L/g" -e "s/DDD/$D/g" -e "s/nnn/$n_real/g" < code/lancio.sh > temp.tmp

			mv temp.tmp uga-L_$L-D_$D-nr_$n_real.inp 	

			printf 	"%s\n" "qsub uga-L_$L-D_$D-nr_$n_real.inp" >> script_wait.sh

			done
		done
	done	

chmod +x script_wait.sh
#./script_wait.sh



