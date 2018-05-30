rm -f script_wait.sh
rm -f u*
rm -f ../L*



cd code
       python setup.py build_ext --inplace
    wait    
# rm -rf *so *c *build *core __pycache__
cd ..

printf "%s\n" "#!/bin/bash" >> script_wait.sh

LL=(14)
#DD=(1)   
#DD=(1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0)
#DD=(0.5 1.5 2.5 3.5 4.5 5.5 6.5 7.5 8.5)


DD=(2. 2.25 2.5 2.75 3. 3.25 3.5 3.75 4. 4.25 4.5 4.75 5.)
#5.25 5.5 5.75 6. 6.5 7. 7.5 8. 8.5 9.)

#nr=(1 1 1 1 1) 
nr=(10) #*20
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



