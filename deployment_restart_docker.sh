
# docker run -d 80:8050

CID=$(docker ps | grep "yangai" | awk '{print $1}')
echo $CID

if [ "$CID" != "" ]
then
    echo "CID is"
    docker restart $CID
    echo ">>> Restarted old container $CID"

else
    echo "No Running Container"
fi