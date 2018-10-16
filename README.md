# cyber-contact
contact on website by tornado, show how to use tornado_mysql.
make rpm package on centos7, but I think this project can run on anything linux.

## 功能
* 用户在网站上输入联系消息
* 消息列表


## REST API文档
http://contact.cyber-life.cn/swagger/spec.html


## Demo
* http://contact.cyber-life.cn/contact/web/index
* http://contact.cyber-life.cn/contact/web/messages


## 安装软件包
### 安装 nginx
```
yum -y install nginx
systemctl start nginx
systemctl enable nginx
```
### 安装 mariadb-server
```
yum -y install mariadb mariadb-server
systemctl start mariadb
systemctl enable mariadb
```
### 安装 pip
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
### 安装 tornado
```
pip install --upgrade pip
pip install tornado==4.3
```
### 安装python依赖包
```
yum install git
git clone https://github.com/SerenaFeng/tornado-swagger.git
cd tornado-swagger
python setup.py install
pip install tornado_mysql
```

## 安装 cyber-contact
```
rpm -Uvh cyber-contact-1.0.0-3_git_ed98137.x86_64.rpm --force
```
