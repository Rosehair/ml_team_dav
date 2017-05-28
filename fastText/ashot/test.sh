if [ -z $2 ]
then
	exit
fi
./fasttext test $1 $2

