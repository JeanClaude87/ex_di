#!/bin/bash

### PARAMETER START
L 		=	0
D 		=	0
n_real 	=	0

### nom du job (a changer)
#$ -N exdiag-L_${L}-D_${D}-nr_${n_real}

### file d'attente (a changer)
#$ -q "E5-2667v4deb128nl,E5-2667v4deb256A,E5-2667v2d2deb128,E5-2667v2h6deb128,E5-2670deb128A,E5-2670deb128B,E5-2670deb128C,E5-2670deb128D,E5-2670deb128E,E5-2670deb128F,E5-2670deb128nl"

### exporter les variables d'environnement sur tous les noeuds d'execution
#$ -V
 
WORKDIR="/home/pnaldesi/ex_di/code"
cd ${WORKDIR}

		
python wrap.py $L $D $n_real

