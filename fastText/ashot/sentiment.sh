if [ -z $2 ];
then
	exit
fi

./train.sh $1 model
./test.sh model.bin $2

