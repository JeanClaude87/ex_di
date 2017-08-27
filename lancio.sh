#!/bin/bash

### variables SGE
### shell du job
#$ -S /bin/bash

### nom du job (a changer)
#$ -N SommeVecVecPAR

### file d'attente (a changer)
#$ -q "E5-2667v4deb128nl,E5-2667v4deb256A,E5-2667v2d2deb128,E5-2667v2h6deb128,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128E,E5-2670deb128F,E5-2670deb128nl"

### parallel environment & nb cpu (NSLOTS)
#$ -pe mpi16_debian 16

### charger l'environnement utilisateur pour SGE
#$ -cwd

### exporter les variables d'environnement sur tous les noeuds d'execution
#$ -V

### mails en debut et fin d'execution
#$ -m be     
 
# donné par le système de batch
HOSTFILE=${TMPDIR}/machines
 
# aller dans le repertoire de travail/soumission
# important, sinon, le programme est lancé depuis ~/
WORKDIR="/home/pnaldesi"
cd ${WORKDIR}

 
### configurer l'environnement
source /usr/share/modules/init/bash
module use /applis/PSMN/Modules
module load Base/psmn
module load openmpi/1.6.4-intel-14.0.1/
###module load python/2.7

for L in $(seq 8 2 10)
	do

	for D in $(seq -f "%0.1f" 0.5 0.5 1.0)
		do

		for n_real in $(seq 1 1 2)
			do
		
			python wrap.py $L $D $n_real


			done
		done
	done
