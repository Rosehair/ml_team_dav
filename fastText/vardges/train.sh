if [ -z $2 ]
then
	exit
fi
./fasttext supervised -input $1 -output $2 -lr 2 -epoch 2 -wordNgrams 3 -dim 150

