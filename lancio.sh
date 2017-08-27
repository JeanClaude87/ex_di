#!/bin/bash

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
