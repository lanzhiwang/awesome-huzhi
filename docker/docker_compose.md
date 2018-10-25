## Docker Compose

### Docker Compose 基础操作

```bash
$ docker-compose --version
docker-compose version 1.13.0, build 1719ceb
$ docker-compose --help
$ cat docker-compose.yml
wordpress:
  image: wordpress
  links:
   - mysql
  ports:
   - "80:80"
  environment:
   - WORDPRESS_DB_NAME=wordpress
   - WORDPRESS_DB_USER=wordpress
   - WORDPRESS_DB_PASSWORD=wordpresspwd
mysql:
  image: mysql
  environment:
   - MYSQL_ROOT_PASSWORD=wordpressdocker
   - MYSQL_DATABASE=wordpress
   - MYSQL_USER=wordpress
   - MYSQL_PASSWORD=wordpresspwd
$
$ sudo docker-compose up -d
$ sudo docker-compose up -d --build
$ sudo docker-compose ps
$ sudo docker-compose stop wordpress
$ sudo docker-compose start wordpress


$ cat mesos.yml
zookeeper:
  image: garland/zookeeper
  ports:
   - "2181:2181"
   - "2888:2888"
   - "3888:3888"
mesosmaster:
  image: garland/mesosphere-docker-mesos-master
  ports:
   - "5050:5050"
  links:
   - zookeeper:zk
  environment:
   - MESOS_ZK=zk://zk:2181/mesos
   - MESOS_LOG_DIR=/var/log/mesos
   - MESOS_QUORUM=1
   - MESOS_REGISTRY=in_memory
   - MESOS_WORK_DIR=/var/lib/mesos
marathon:
  image: garland/mesosphere-docker-marathon
  links:
   - zookeeper:zk
   - mesosmaster:master
  command: --master zk://zk:2181/mesos --zk zk://zk:2181/marathon
  ports:
   - "8088:8080"
mesosslave:
  image: garland/mesosphere-docker-mesos-master:latest
  ports:
   - "5051:5051"
  links:
   - zookeeper:zk
   - mesosmaster:master
  entrypoint: mesos-slave
  environment:
   - MESOS_HOSTNAME=172.17.2.15
   - MESOS_MASTER=zk://zk:2181/mesos
   - MESOS_LOG_DIR=/var/log/mesos
   - MESOS_LOGGING_LEVEL=INFO

$ sudo docker-compose -f mesos.yml up -d


# docker-compose.yml文件示例
version: "3"
services:
  #insight所有前端项目
  insight-fe:
    image: openresty:latest
    command: openresty -p /home/work/app/insight-fe/openresty/ -c /home/work/app/insight-fe/openresty/conf/nginx.conf -g "daemon off;" 
    user: root
    working_dir: /home/work
    ports:
      # insight agg2
      - "80:8080"
      # insight passport
      - "8081:8081"
      # insight backend
      - "8899:8899"
      # insight data-gate
      # - "8666:8666"
    volumes:
      - ./app:/home/work/app/
    links:
      - insight-api-gate

  #insight后端API Gate
  insight-api-gate:
    image: openresty:latest
    command: openresty -p /home/work/app/app-nginx-conf/ -c /home/work/app/app-nginx-conf/conf/nginx.conf -g "daemon off;" 
    user: root
    working_dir: /home/work
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-auth
      - insight-backend-php
      - insight-index-web
      - insight-database

  #insight Auth
  insight-auth:
    image: openresty:latest
    command: openresty -p /home/work/app/insight-auth/ -c /home/work/app/insight-auth/conf/nginx.conf -g "daemon off;"
    user: root
    working_dir: /home/work
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-backend-php
      - insight-database

  # insight index-web 暂时独占一个docker
  insight-index-web:
    image: openresty:latest
    command: openresty -p /home/work/app/index-web/openresty/ -c /home/work/app/index-web/openresty/conf/nginx.conf -g "daemon off;"
    user: root
    working_dir: /home/work
    ports:
      - "8626:8626"
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-backend-php
      - insight-database

  # insight后端PHP，所有php模块均在此
  insight-backend-php:
    image: php-fpm:latest
    command: php-fpm -c /home/work/app/php-backend/php-fpm/conf/php.ini -y /home/work/app/php-backend/php-fpm/conf/php-fpm.conf -F -R
    volumes:
      - ./app:/home/work/app/
      - ./var:/home/work/var/
    links:
      - insight-database

  # 数据库mysql和redis等基础服务
  insight-database:
    image: mysql-redis:latest
    command: /usr/sbin/init 
    privileged: true
    user: root 
    working_dir: /root
    ports:
      - "8123:8123"
      - "8124:8124"
    volumes:
      - ./data:/data/

```
