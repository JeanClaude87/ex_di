#!/bin/bash

### nom du job (a changer)
#$ -N L_LLL-D_DDD-nr_nnn

### parallel environment & nb cpu (NSLOTS)

###$ -pe mpi8_debian 8

#$ -q "E5-2667v4deb128nl,E5-2667v4deb256A,E5-2670deb128A"

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


