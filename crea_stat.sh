#!/bin/sh
rm script_wait.sh

printf "%s\n" "#!/bin/bash" >> script_wait.sh

LL=($(seq 8 2 16))
nr=(1 2 3 4 5)


len=${#LL[@]%.*} 

for((i=0;i<$len;i++))
	do
		L=${LL[i]}
		
	for D in $(seq -f "%0.1f" 0.5 0.5 1.0)
		do

		for((n_real=0;n_real<${nr[i]};n_real++))
			do
		
		awk -v Gamma=$n_real -v Beta=$D -v Alpha=$L ' 
			{if (($1=="L") && ($2=="=")) 		$3="     " Alpha;	}
			{if (($1=="D") && ($2=="=")) 		$3="     " Beta;	}
			{if (($1=="n_real") && ($2=="=")) 	$3="     " Gamma;	} { print $0;} 
			'  code/lancio.sh  > temp2.inp;
			
			cp temp2.inp uga-L_$L-D_$D-nr_$n_real.inp 
			rm temp2.inp

			printf 	"%s\n" "qsub uga-L_$L-D_$D-nr_$n_real.inp" >> script_wait.sh

			done
		done
	done	

