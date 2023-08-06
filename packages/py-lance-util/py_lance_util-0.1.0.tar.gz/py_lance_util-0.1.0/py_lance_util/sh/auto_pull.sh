#! /bin/bash -ilex
## author:jyeontu

echo "--------------------------------"
echo "----------开始执行脚本----------"
date
pwd;
echo "切换到git目录"
##切换到放置git代码的目录绝对路径
cd /data/python-server;
path=`pwd`
echo $path
if [ "$path" == "/data/python-server" ]
then
        echo "目录切换成功，准备拉取最新代码"
else
        echo "目录切换失败，退出程序"
        exit 0;
fi
git pull;
echo "准备重启容器"
# npm run build;
sleep 30
docker restart py-server
echo "成功"
