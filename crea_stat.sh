rm -f script_wait.sh
rm -f u*
rm -f ../L*

cd code
        python setup.py build_ext --inplace
        wait    
cd ..

printf "%s\n" "#!/bin/bash" >> script_wait.sh

LL=(8 10 12 14 16)
#DD=(1)   
#DD=(1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0)
#DD=(0.5 1.5 2.5 3.5 4.5 5.5 6.5 7.5 8.5)
<<<<<<< HEAD
DD=(0.25 0.75 1.25 1.75 2.25 2.75 3.25 3.75 4.25 4.75 5.25 5.75)
=======
#DD=(0.25 0.75 1.25 1.75 2.25 2.75 3.25 3.75 4.25 4.75 5.25 5.75)

DD=(1.75 2.0 2.25 2.5 2.75 3.0 3.25 3.5 3.75 4.0)
>>>>>>> 23622f30b713fec1278aaa9765ac0f484ce37906

#nr=(1 1 1 1 1) 
nr=(60 50 40 30 20) #*50
ncy=1

lenl=${#LL[@]%.*} 
lend=${#DD[@]%.*} 

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
