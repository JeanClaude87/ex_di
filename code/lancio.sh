#!/bin/bash

### nom du job (a changer)
#$ -N L_LLL-D_DDD-nr_nnn

### file d'attente (a changer)
#$ -q "E5-2667v2d2deb128,E5-2667v2h6deb128,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128F,E5-2670deb128nl,E5-2670deb256A,E5-2670deb256C,E5-2670deb256D" 
###"E5-2667v4deb128nl,E5-2667v4deb256A,E5-2667v2d2deb128,E5-2667v2h6deb128,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128E,E5-2670deb128F,E5-2670deb128nl"

### exporter les variables d'environnement sur tous les noeuds d'execution
#$ -V

###$ -e /dev/null
#$ -o /dev/null
 
WORKDIR="/home/pnaldesi/ex_di/code"
cd ${WORKDIR}

echo $SHELL
<<<<<<< HEAD

for((i=0; i<20; i++))
	do
		
	python wrap.py LLL DDD nnn 

	done


