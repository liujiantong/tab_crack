# 区总报表项目

## 依赖
* mysql-connector
* flask
* flask-sslify
* requests

## 部署
* scp tab_report.tar deployer@211.151.25.6:uni_deploy/
* ssh deployer@211.151.25.6
* sudo su -
* scp -P222 /home/deployer/uni_deploy/tab_report.tar root@192.168.0.182:/home/tao.liu1

## 启动
```
python report.py or gunicorn -w 2 -b :5000 report:app
```
