#!/bin/bash

### nom du job (a changer)
#$ -N L_LLL-D_DDD-nr_nnn

### parallel environment & nb cpu (NSLOTS)

###$ -pe mpi16_debian

#$ -q "h6-E5-2667v4deb128,h48-E5-2667v2deb128"

module load Python/3.6.1

### exporter les variables d'environnement sur tous les noeuds d'execution
#$ -V

###$ -e /dev/null
###$ -o /dev/null
 
WORKDIR="/home/pnaldesi/exact_di/ex_di/code"
cd ${WORKDIR}

echo $SHELL

for((i=0; i<kkk; i++))
	do
	for((j=0; j<20; j++))
		do		
			python wrap.py LLL DDD nnn
			wait
		done
	done


