#!/bin/bash
rm -f script_wait2.sh

#source /usr/share/modules/init/tcsh
#module use /applis/PSMN/Modules
#module load Base/psmn
#module load python/2.7


printf "%s\n" "#!/bin/bash" >> script_wait2.sh

#LL=(    8   10   12   14   16)
#nr=(10000 6000 6000 4000 1000)
#DD=(0.5 0.75 1.0 1.25 1.5 1.75 2.0 2.25 2.5 2.75 3.0 3.25 3.5 3.75 4.0 4.25 4.5 4.75 5.0 5.125 5.25 5.375 5.5 5.625 5.75 5.875 6.0 6.125 6.25 6.375 6.5 6.625 6.75 6.875 7.0 7.25 7.5 7.75 8.0 8.25 8.5 8.75 9.0 9.25 9.5 9.75 10.0)		

LL=(14)
nr=(50) ### x20
DD=(0.75 1.25 1.75 2.25 2.75 3.25 3.75 4.25 4.75 5.125 5.25 5.375 5.625 5.75 5.875 6.125 6.25 6.375 6.625 6.75 6.875 7.25 7.75 8.25 8.75 9.25 9.75)		

nrD14=(1 82 1 41 82 1 82 1 82 1 82 1 82 3 82 1 82 1 82 1 82 82 82 1 82 82 82 1 82 82 82 1 82 82 82 1 82 1 82 1 82 1 82 1 82 1 82)
nrD=(0 1 0 1 56 0 61 0 60 0 56 0 20 0 1 0 1 0 1 0 6 4 45 0 55 50 57 0 64 52 65 0 71 76 84 0 71 0 89 1 89 1 91 1 84 1 1)

lenl=${#LL[@]%.*} 
lend=${#DD[@]%.*} 

for((i=0; i<$lenl; i++))
	do
		L=${LL[i]}


	for((j=0; j<$lend; j++))
		do
			D=${DD[j]}
	
	echo $L $D
	
#	for D in $(seq -f "%0.1f" 0.5 0.5 1.0)

		for((n_real=0; n_real<${nrD[j]}; n_real++))
			do
		
			sed -e "s/LLL/$L/g" -e "s/DDD/$D/g" -e "s/nnn/$n_real/g" < code/lancio.sh > temp.tmp

			mv temp.tmp uga-L_$L-D_$D-nr_$n_real.inp 	

			printf 	"%s\n" "qsub uga-L_$L-D_$D-nr_$n_real.inp" >> script_wait2.sh

			done
		done
	done	

chmod +x script_wait2.sh
./script_wait2.sh



