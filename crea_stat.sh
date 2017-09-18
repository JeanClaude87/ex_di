#!/bin/bash
rm -f script_wait.sh

#source /usr/share/modules/init/tcsh
#module use /applis/PSMN/Modules
#module load Base/psmn
#module load python/2.7


printf "%s\n" "#!/bin/bash" >> script_wait.sh


LL=(18)

DD=(1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0) #0.75 1.0 10.0 1.25 1.5 1.75 2.0 2.25 2.5 2.75 3.0 3.25 3.5 3.75 4.0 4.25 4.5 4.75 5.0 5.125 5.25 5.375 5.5 5.625 5.75 5.875 6.0 6.125 6.25 6.375 6.5 6.625 6.75 6.875 7.0 7.25 7.5 7.75 8.0 8.25 8.5 8.75 9.0 9.25 9.5 9.75)

nrD18=(20 20 20 20 20 20 20 20 20) #*5

lenl=${#LL[@]%.*} 
lend=${#DD[@]%.*} 

for((i=0; i<$lenl; i++))
	do
	L=${LL[i]}
  		
#  	if [ $L == 14 ]; then
#		nr=(1 163 1 82 163 1 163 1 163 1 163 1 163 5 163 1 163 1 163 1 164 163 164 1 164 163 164 1 164 163 164 1 164 164 164 1 164 1 164 1 164 1 164 1 164 1 164)
#	else
#		nr=(2) #1 0 1 28 0 31 0 30 0 28 0 10 0 1 0 1 0 1 0 3 2 23 0 28 25 29 0 32 26 33 0 36 38 42 0 36 0 45 1 45 1 46 1 42 1 1)
#	fi
	
	echo $nr

	for((j=0; j<$lend; j++))
		do
		D=${DD[j]}
	
		echo $L $D ${nr[j]}

		for((n_real=0; n_real<${nr[j]}; n_real++))
			do
		
			sed -e "s/LLL/$L/g" -e "s/DDD/$D/g" -e "s/nnn/$n_real/g" < code/lancio.sh > temp.tmp

			mv temp.tmp uga-L_$L-D_$D-nr_$n_real.inp 	

			printf 	"%s\n" "qsub uga-L_$L-D_$D-nr_$n_real.inp" >> script_wait.sh

			done
		done
	done	

chmod +x script_wait.sh
./script_wait.sh



