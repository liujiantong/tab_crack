# 爱康报表项目 (基于授权码解决License受限问题)

爱康报表项目的目标是解决Tableau Server 用户licence 过少的问题(目前爱康公司只购买了10个用户的license). 
解决方案如下所述.

1. 分配一个统一的Tableau Server 账号作为登录账号
2. Tableau 为每个邮箱分配一个授权码, 对应用户所能访问数据的区域和报表
3. 用户使用爱康公司的email/密码登录本服务, 并从数据库中获取用户的授权码(TOKEN)
4. 本服务使用统一的账号登录Tableau Server
5. 本服务根据授权码从数据库获取该用户有访问权限的报表列表, 并展示给用户
6. 用户点击需要查看的报表链接, 本服务将授权码作为参数(TOKEN)传给相应的报表视图(View)
7. 报表视图(View)根据授权码(TOKEN)过滤展示数据


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
