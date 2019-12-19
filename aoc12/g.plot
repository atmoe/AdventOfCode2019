set key off
set term png
set output "g.png"
splot 'moon1.txt' using 1:2:3 with points palette pointsize 1 pointtype 7
