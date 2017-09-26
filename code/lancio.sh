#!/bin/bash

### nom du job (a changer)
#$ -N L_LLL-D_DDD-nr_nnn

### parallel environment & nb cpu (NSLOTS)
#$ -pe test_debian 16

### file d'attente (a changer)
#$ -q "E5-2667v2d2deb128,E5-2667v2deb128cssi,E5-2667v2deb128nlspe,E5-2667v2h6deb128,E5-2667v4deb128nl,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128F,E5-2670deb128nl,E5-2670deb256A,E5-2670deb256C,E5-2670deb256D,E5-2697Av4deb256,x5570deb24A,x5570deb24C,x5570deb24D,x5570deb24E,x5650lin24ibA,x5650lin24ibB" 

###"E5-2667v2d2deb128,E5-2667v2deb128cssi,E5-2667v2deb128nlspe,E5-2667v2h6deb128,E5-2667v4deb128nl,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128F,E5-2670deb128nl,E5-2670deb256A,E5-2670deb256C,E5-2670deb256D,E5-2697Av4deb256"
###,x5570deb24A,x5570deb24C,x5570deb24D,x5570deb24E,x5650lin24ibA,x5650lin24ibB" 

### exporter les variables d'environnement sur tous les noeuds d'execution
#$ -V

### configurer l'environnement
source /usr/share/modules/init/bash
module use /applis/PSMN/Modules
module load Base/psmn
module load openmpi/1.6.4-intel-14.0.1

###$ -e /dev/null
###$ -o /dev/null
 
WORKDIR="/home/pnaldesi/ex_di/code"
cd ${WORKDIR}

echo $SHELL

for((i=0; i<1; i++))

	do
		
	python wrap.py LLL DDD nnn 

	done


