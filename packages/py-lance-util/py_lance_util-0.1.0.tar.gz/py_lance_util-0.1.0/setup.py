# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_lance_util',
 'py_lance_util.api',
 'py_lance_util.api.middleware',
 'py_lance_util.common',
 'py_lance_util.config',
 'py_lance_util.db',
 'py_lance_util.py_practice',
 'py_lance_util.py_practice.background',
 'py_lance_util.py_practice.controller',
 'py_lance_util.py_practice.model',
 'py_lance_util.py_practice.service',
 'py_lance_util.utils']

package_data = \
{'': ['*'], 'py_lance_util': ['deploy/*', 'sh/*']}

install_requires = \
['fastapi==0.88.0',
 'kazoo>=2.9.0,<3.0.0',
 'loguru==0.6.0',
 'pika==1.3.1',
 'pydantic==1.9.0',
 'pymysql>=1.0.2,<2.0.0',
 'redis==4.4.0',
 'sqlalchemy==1.4.32',
 'uvicorn==0.17.6']

setup_kwargs = {
    'name': 'py-lance-util',
    'version': '0.1.0',
    'description': 'pytdemo',
    'long_description': '[基于FastApi的python项目，封装常用工具（持续集成中......)]\n# 步骤\n\n## 构建Dockerfile\n\n### 基础镜像\n\n**构建python运行基础镜像Dockerfile**\n\n```dockerfile\nFROM amazonlinux:latest\n\nLABEL maintainer=“Lance”\n\nRUN yum update -y && yum install -y python3 python3-devel vim\n```\n\n**具体服务镜像Dockerfile**\n\n```dockerfile\nFROM registry.cn-hangzhou.aliyuncs.com/lance0515/lance-test:base_python\n\nLABEL maintainer="Lance"\n\nCOPY requirements.txt .\n\nRUN pip3 install -r requirements.txt\n\n# 配置默认放置 App 的目录\nRUN mkdir -p /app\n\nWORKDIR /app\n\nEXPOSE 28000-28004\n\nCOPY . .\n\nENV PYTHONPATH /app\n\nENTRYPOINT ["python3", "/app/main.py"]\n\n```\n\n## 推送到阿里云\n\n```dockerfile\n# 登录， 输入密码\ndocker login --username=**** registry.cn-hangzhou.aliyuncs.com\n# 对镜像打标签\ndocker tag [ImageId] registry.cn-hangzhou.aliyuncs.com/****/lance-test:[镜像版本号]\n# 发布\ndocker push registry.cn-hangzhou.aliyuncs.com/****/lance-test:[镜像版本号]\n```\n\n## 服务器下载\n\n```dockerfile\n# 登录\ndocker login --username=**** registry.cn-hangzhou.aliyuncs.com\n\ndocker pull registry.cn-hangzhou.aliyuncs.com/****/lance-test:[镜像版本号]\n```\n\n## docker-compose 实例化容器\n\n**docker-compose.yml**\n\n> 通过docker-compose启动容器\n\n```\nversion: "3"\nservices:\n  py-server:\n    image: registry.cn-hangzhou.aliyuncs.com/lance0515/lance-test:${BASE_VERSION}\n    container_name: py-server\n    ports:\n      - 28000:8000\n      - 28004:8004\n    volumes:\n      - ${BASE_PROJECT_PATH}:/app\n\n```\n\n<!--在.env文件配置docker-compose涉及到的变量-->\n**.env**\n\n```\nBASE_VERSION=v1.0            # 打tag时镜像实际版本号\nBASE_PROJECT_PATH=/data/app  # 项目在服务器实际地址\n```\n\n**## 自动拉取代码并重启服务**\n\n> 通过脚本自动拉取代码  \n> **auto_pull.sh**\n\n```shell\n#! /bin/bash \necho "--------------------------------"\necho "----------开始执行脚本----------"\ndate\npwd;\necho "切换到git目录"\n##切换到放置git代码的目录绝对路径\ncd /home/lance/python/python-server;\npath=`pwd`\necho $path\nif [ "$path" == "/home/lance/python/python-server" ]\nthen\n        echo "目录切换成功，准备拉取最新代码"\nelse\n        echo "目录切换失败，退出程序"\n        exit 0;\nfi\ngit pull;\necho "准备重启容器"\n# npm run build;\nsleep 30\ndocker restart py-server\necho "成功"\n```\n\n## 结合github push自动拉取代码\n\n**通过github设置webhook，回调执行auto_pull.sh脚本**\n',
    'author': 'feilong Chen',
    'author_email': 'chenfeilong@cloudwalk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
