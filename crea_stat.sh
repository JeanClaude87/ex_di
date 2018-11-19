rm -f script_wait.sh
rm -f u*
rm -f ../L*

cd code
    python3 setup.py build_ext --inplace
    wait    
cd ..

printf "%s\n" "#!/bin/bash" >> script_wait.sh

LL=(18)

#DD=(2. 2.25 2.5 2.75 3. 3.25 3.5 3.75 4. 4.25 4.5 4.75 5.)
DD=(2. 3. 4. 5.) # 5. 

nr=(20 20 20 20) # *16
ncy=1

lenl=${#LL[@]} 
lend=${#DD[@]} 

for((i=0; i<$lenl; i++))
        do
        L=${LL[i]}

        for((j=0; j<$lend; j++))
                do
                D=${DD[j]}
        
                echo $L $D ${nr[i]}

                for((n_real=0; n_real<${nr[i]}; n_real++))
                        do
                
                        sed -e "s/kkk/$ncy/g" -e "s/LLL/$L/g" -e "s/DDD/$D/g" -e "s/nnn/$n_real/g" < code/lancio.sh > temp.tmp
                        mv temp.tmp uga-L_$L-D_$D-nr_$n_real.inp        

                        printf  "%s\n" "qsub uga-L_$L-D_$D-nr_$n_real.inp" >> script_wait.sh

                        done
                done
        done    

chmod +x script_wait.sh
#./script_wait.sh



