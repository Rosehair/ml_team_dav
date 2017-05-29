if [ -z $1 ]
then
	exit
fi

cat $1 | 
tr "[:upper:]" "[:lower:]" |
sed  "s/[\{\}\*.\!?:\",/\(\)-]/ /g" |
sed "s/\bcan't /can not /g" |
sed "s/n't / not /g" | 
sed "s/'re / are /g" | 
sed "s/'m / am /g" | 
sed "s/'s//g" | 
sed "s/'//g" | 
sed "s/\bis \|\bare \|\bam \|\ba \|\ban \|\bthe / /g" |
sed "s/\b[^i] / /g" |
sed "s/\( [0-9]\+\)/ /g" |
sed "s/  */ /g" 
