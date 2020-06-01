# DjangoFilm
基于ubuntu16.04、python3.5、Django2.2、Spark2.3、redis5.0的图书推荐系统

## 安装
```
pip install django==2.2
pip install redis5.0
pip install pyspark==2.3
pip install Pillow
```  

### 安装redis
下载安装包\解压\启动
```
wget http://download.redis.io/releases/redis-5.0.4.tar.gz
tar xzf redis-5.0.4.tar.gz
cd redis-5.0.4
make
```  
启动服务  
`src/redis-server`   
运行src文件夹下面的redis-cli，启动redis的命令行
```
src/redis-cli
set foo bar
get foo
```

## 生成数据库迁移文件
` python manage.py migrate`

## 创建管理员
`python mamage.py createsuperuser`

## 注册登录，导入数据
在主页中的‘上传文件’中选择项目的uploads文件夹下的csv文件进行图书数据的导入  

