# Tab报表项目 (基于授权码解决License受限问题)

Tab报表项目的目标是解决Tableau Server 用户licence 过少的问题(目前公司只购买了10个用户的license).
解决方案如下所述.

1. 分配一个统一的Tableau Server 账号作为登录账号
2. 本服务使用统一的账号登录Tableau Server, 并缓存tableau授权凭证
3. Tableau 为每个邮箱分配一个授权码, 对应用户所能访问数据的区域和报表
4. 用户使用公司的email/密码登录本服务, 并从数据库中获取用户的授权码(TOKEN)
5. 本服务将tableau授权凭证写入用户的cookie
6. 本服务根据授权码从数据库获取该用户有访问权限的报表列表, 并展示给用户
7. 用户点击需要查看的报表链接, 本服务将授权码作为参数(TOKEN)传给相应的报表视图(View)
8. 报表视图(View)根据授权码(TOKEN)过滤展示数据


## 依赖
* mysql-connector
* flask
* flask-sslify
* requests
* redis
* gunicorn


## 参考文档
* https://onlinehelp.tableau.com/current/api/js_api/en-us/JavaScriptAPI/js_api.htm


## 部署

### 启动 Redis
* 在 ETL服务器安装redis: yum install redis
* 启动redis: redis-server redis.conf

### 复制代码到 ETL服务器
* scp tab_report.tar user@etl_server_ip:uni_deploy/
* ssh user@etl_server_ip
* sudo su -
* scp -P222 /home/deployer/uni_deploy/tab_report.tar user@etl_server_ip:/home/tao.liu1

### 复制邮箱登录代码到 Titan服务器
* scp tab_report.tar user@titan_server_ip:

### 安装 gunicorn
* pip install gunicorn

### 安装 supervisor
- 分别在 ETL server 和 Titan 上安装: pip install supervisor
- 修改/etc/supervisord.conf, 添加服务配置

### 映射外网地址
- 因为公司email服务器访问带宽有限, 在工作时间段访问速度不稳定. 因此需要一个访问email服务器的中继节点.
- 目前的email中继服务部署在Titan server, 需要一个外网访问地址映射, 参见`conf.py`.

## 启动
```
test: python report.py
production: sudo supervisorctl start tab_report
```

## 启动 mail relay
```
test: python mail_relay.py
production: sudo supervisorctl start mail_relay
```
