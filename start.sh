#! /bin/sh
zipkin_run=`docker ps | grep openzipkin/zipkin | wc -l`

if [ $zipkin_run = 1 ];then
    echo "zipkin is runing"
else
    echo "try to start zipkin with docker"
    docker run --name my_zipkin -d -p 9411:9411 openzipkin/zipkin
fi

ps -ef | grep -e "python [A B C D E]" | awk '{print $2}' | xargs kill -9

echo "start service A"
python A.py &
echo "start service B"
python B.py &
echo "start service C"
python C.py &
echo "start service D"
python D.py &
echo "start service E"
python E.py &