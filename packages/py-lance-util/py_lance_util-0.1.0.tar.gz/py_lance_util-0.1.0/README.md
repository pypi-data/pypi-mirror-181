[基于FastApi的python项目，封装常用工具（持续集成中......)]
# 步骤

## 构建Dockerfile

### 基础镜像

**构建python运行基础镜像Dockerfile**

```dockerfile
FROM amazonlinux:latest

LABEL maintainer=“Lance”

RUN yum update -y && yum install -y python3 python3-devel vim
```

**具体服务镜像Dockerfile**

```dockerfile
FROM registry.cn-hangzhou.aliyuncs.com/lance0515/lance-test:base_python

LABEL maintainer="Lance"

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# 配置默认放置 App 的目录
RUN mkdir -p /app

WORKDIR /app

EXPOSE 28000-28004

COPY . .

ENV PYTHONPATH /app

ENTRYPOINT ["python3", "/app/main.py"]

```

## 推送到阿里云

```dockerfile
# 登录， 输入密码
docker login --username=**** registry.cn-hangzhou.aliyuncs.com
# 对镜像打标签
docker tag [ImageId] registry.cn-hangzhou.aliyuncs.com/****/lance-test:[镜像版本号]
# 发布
docker push registry.cn-hangzhou.aliyuncs.com/****/lance-test:[镜像版本号]
```

## 服务器下载

```dockerfile
# 登录
docker login --username=**** registry.cn-hangzhou.aliyuncs.com

docker pull registry.cn-hangzhou.aliyuncs.com/****/lance-test:[镜像版本号]
```

## docker-compose 实例化容器

**docker-compose.yml**

> 通过docker-compose启动容器

```
version: "3"
services:
  py-server:
    image: registry.cn-hangzhou.aliyuncs.com/lance0515/lance-test:${BASE_VERSION}
    container_name: py-server
    ports:
      - 28000:8000
      - 28004:8004
    volumes:
      - ${BASE_PROJECT_PATH}:/app

```

<!--在.env文件配置docker-compose涉及到的变量-->
**.env**

```
BASE_VERSION=v1.0            # 打tag时镜像实际版本号
BASE_PROJECT_PATH=/data/app  # 项目在服务器实际地址
```

**## 自动拉取代码并重启服务**

> 通过脚本自动拉取代码  
> **auto_pull.sh**

```shell
#! /bin/bash 
echo "--------------------------------"
echo "----------开始执行脚本----------"
date
pwd;
echo "切换到git目录"
##切换到放置git代码的目录绝对路径
cd /home/lance/python/python-server;
path=`pwd`
echo $path
if [ "$path" == "/home/lance/python/python-server" ]
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
```

## 结合github push自动拉取代码

**通过github设置webhook，回调执行auto_pull.sh脚本**
