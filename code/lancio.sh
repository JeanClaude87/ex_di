#!/bin/bash

### nom du job (a changer)
#$ -N L_LLL-D_DDD-nr_nnn

### parallel environment & nb cpu (NSLOTS)

#$ -pe mpi16_debian 16

###$ -q "h48-E5-2667v2deb128,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128E,E5-2670deb128F,h6-E5-2667v4deb128"
#$ -q   "h48-E5-2667v2deb128,h6-E5-2667v4deb128,E5-2667v2deb128nl,E5-2667v4deb256A,E5-2670deb128A,E5-2670deb128B,E5-2670deb128nl"

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
	for((j=0; j<16; j++))
		do		
			mpirun -np 16 python3 wrap.py LLL DDD nnn
		done
	done


