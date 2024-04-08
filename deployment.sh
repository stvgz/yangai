# !/bin/sh

# stop old container

# build new container
echo ">>> buld new container"

#  date +"%Y-%m-%d %T"
currentDate=`date +%Y-%m-%d`

docker build -t yangai:$currentDate .

echo ">>> built yangai:$currentDate"

echo ">>> Try old container id"

CID=$(docker ps | grep "yangai" | awk '{print $1}')
echo $CID

if [ "$CID" != "" ]
then
    echo "CID is"
    docker stop $CID
    echo ">>> Stopped old container $CID"

else
    echo "No Running Container"
fi


docker run -d -p 80:8050 yangai:$currentDate

echo ">>> Started new container"
