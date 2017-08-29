#!/bin/bash
rm -f script_wait.sh

printf "%s\n" "#!/bin/bash" >> script_wait.sh

LL=(8 10)
nr=(4 4)
DD=(0.75 1.25 1.75 2.25)


#nr=(10000 6000 6000 1000)
#DD=(0.5 0.75 1.0 1.25 1.5 1.75 2.0 2.25 2.5 2.75 3.0 3.25 3.5 3.75 4.0 4.25 4.5 4.75 5.0 5.125 5.25 5.375 5.5 5.625 5.75 5.875 6.0 6.125 6.25 6.375 6.5 6.625 6.75 6.875 7.0 7.25 7.5 7.75 8.0 8.25 8.5 8.75 9.0 9.25 9.5 9.75 10.0)		
#DD=(0.75 1.25 1.75 2.25 2.75 3.25 3.75 4.25 4.75 5.125 5.25 5.375 5.625 5.75 5.875 6.125 6.25 6.375 6.625 6.75 6.875 7.25 7.75 8.25 8.75 9.25 9.75)		

lenl=${#LL[@]%.*} 
lend=${#DD[@]%.*} 

for((i=1; i<$lenl; i++))
	do
		L=${LL[i]}


	for((j=1; j<$lend; j++))
		do
			D=${DD[j]}
	
	echo $L $D
	
#	for D in $(seq -f "%0.1f" 0.5 0.5 1.0)

		for((n_real=0; n_real<${nr[i]}; n_real++))
			do
		
			sed -e "s/LLL/$L/g" -e "s/DDD/$D/g" -e "s/nnn/$n_real/g" < code/lancio.sh > temp.tmp

			mv temp.tmp uga-L_$L-D_$D-nr_$n_real.inp 	

			printf 	"%s\n" "qsub uga-L_$L-D_$D-nr_$n_real.inp" >> script_wait.sh

			done
		done
	done	

chmod +x script_wait.sh
