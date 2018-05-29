set fit quiet
set autoscale
set terminal postscript fontfile add '/Users/naldesi/Type1/sfrm1200.pfb'\
						fontfile add '/Users/naldesi/Type1/sfti1200.pfb' 			
set terminal postscript	eps color enhanced font "SFRM1200" 32	size 4,3

set style line 1 lt 1 lw 5 pt 1 ps 2 lc rgb 'black' 
set style line 2 lt 1 lw 5 pt 1 ps 2 lc rgb 'red'     

unset key
set yrange [0:0.05]

set fit errorvariables

DD = "0.25 0.5 0.75 1.0 1.25 1.5 1.75 2.0 2.25 2.5 2.75 3.0 3.25 3.5 3.75 4.0 4.25 4.5 4.75 5.0 5.25 5.5 5.75 6.0 6.5 7.0" #"7.5 8.0 8.5 9.0"
names = "SzSz_DE_t SzSz_Huse_t"

do for [i=1:words(names)] {

Nam = word(names, i)

do for [L=8:16:2] {

l=2

fitfile = sprintf('../plot/dati_fit/%s/L_%.0f.dat',Nam, L)

set print fitfile

do for [i=1:words(DD)] {

D = word(DD, i)

outfile =	sprintf('../plot/dati_fit/%s/plot/L_%.0f-D_%s.eps', Nam, L, D)

infile  = 	sprintf('../medie/%s/L_%.0f/D_%s.dat',Nam, L,D)

 set output	outfile

	f(x) = a*( exp(-x/abs(b)) + exp((x-L)/abs(b)))
	
	a=0.0001
	b=1
	
 	fit [l-1:L-l] log(f(x)) infile u 1:2:3 yerrors via a, b	

	print D, '  ', abs(b), '  ', b_err, '  ', a, '  ', a_err
	
	set yrange[*:*]
 	#plot 	infile u 1:(abs($2)) w lp ls 1, infile u 1:(abs($2)):3w errorbars ls 1 #, f(x) ls 2
 	plot 	infile u 1:(exp($2)) w lp ls 1, (abs(f(x))) ls 2
		
 set output

 
 }}}
  
 !rm fit.log