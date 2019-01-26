## MongoDB

### Install

* mongodb-org-4.0.5-1.el7.x86_64
* mongodb-org-server-4.0.5-1.el7.x86_64
* mongodb-org-mongos-4.0.5-1.el7.x86_64
* mongodb-org-tools-4.0.5-1.el7.x86_64
* mongodb-org-shell-4.0.5-1.el7.x86_64

```
[root@dc01 ~]# rpm -ql mongodb-org-4.0.5-1.el7.x86_64
(没有包含文件)
[root@dc01 ~]# 
[root@dc01 ~]# rpm -ql mongodb-org-server-4.0.5-1.el7.x86_64
/etc/mongod.conf
/lib/systemd/system/mongod.service
/usr/bin/mongod
/usr/share/doc/mongodb-org-server-4.0.5
/usr/share/doc/mongodb-org-server-4.0.5/LICENSE-Community.txt
/usr/share/doc/mongodb-org-server-4.0.5/MPL-2
/usr/share/doc/mongodb-org-server-4.0.5/README
/usr/share/doc/mongodb-org-server-4.0.5/THIRD-PARTY-NOTICES
/usr/share/man/man1/mongod.1
/var/lib/mongo
/var/log/mongodb
/var/log/mongodb/mongod.log
/var/run/mongodb
[root@dc01 ~]# 
[root@dc01 ~]# rpm -ql mongodb-org-mongos-4.0.5-1.el7.x86_64
/usr/bin/mongos
/usr/share/man/man1/mongos.1
[root@dc01 ~]# 
[root@dc01 ~]# rpm -ql mongodb-org-tools-4.0.5-1.el7.x86_64
/usr/bin/bsondump
/usr/bin/install_compass
/usr/bin/mongodump
/usr/bin/mongoexport
/usr/bin/mongofiles
/usr/bin/mongoimport
/usr/bin/mongorestore
/usr/bin/mongostat
/usr/bin/mongotop
/usr/share/man/man1/bsondump.1
/usr/share/man/man1/mongodump.1
/usr/share/man/man1/mongoexport.1
/usr/share/man/man1/mongofiles.1
/usr/share/man/man1/mongoimport.1
/usr/share/man/man1/mongorestore.1
/usr/share/man/man1/mongostat.1
/usr/share/man/man1/mongotop.1
[root@dc01 ~]# 
[root@dc01 ~]# rpm -ql mongodb-org-shell-4.0.5-1.el7.x86_64
/usr/bin/mongo
/usr/share/man/man1/mongo.1
[root@dc01 ~]# 
[root@dc01 ~]# 

```

### Cluster

MongoDB Cluster Architecture：

![](./MongoDb_Cluster.svg)

```
mongos-01：10.12.109.175
mongos-01：10.12.109.176
mongos-01：10.12.109.178

mkdir -p /var/lib/mongodb/set01
mkdir -p /var/lib/mongodb/set02
mkdir -p /var/lib/mongodb/set03
mkdir -p /var/lib/mongodb/set04
mkdir -p /var/lib/mongodb/set05
touch /var/log/mongodb/set01-24001.log
touch /var/log/mongodb/set02-24002.log
touch /var/log/mongodb/set02-24003.log
touch /var/log/mongodb/set02-24004.log
touch /var/log/mongodb/set02-24005.log
mkdir -p /var/lib/mongodb/config
touch /var/log/mongodb/config.log
touch /var/log/mongodb/mongos.log

# 在每台机器上执行下列命令 Create the Config Server Replica Set
nohup mongod --configsvr --bind_ip_all --port 28017 --replSet configSet --dbpath /var/lib/mongodb/config --logpath /var/log/mongodb/config.log &

# Connect to one of the config servers
mongo --host 10.12.109.176 --port 28017

# Initiate the replica set
rs.initiate(
  {
    _id: "configSet",
    configsvr: true,
    members: [
      { _id : 0, host : "10.12.109.175:28017" },
      { _id : 1, host : "10.12.109.176:28017" },
      { _id : 2, host : "10.12.109.178:28017" }
    ]
  }
)

# 在每台机器上执行下列命令 Create the Shard Replica Sets
nohup mongod --shardsvr --replSet set01 --bind_ip_all --port 24001 --dbpath /var/lib/mongodb/set01 --logpath /var/log/mongodb/set01-24001.log --logappend --oplogSize 1024 &

nohup mongod --shardsvr --replSet set02 --bind_ip_all --port 24002 --dbpath /var/lib/mongodb/set02 --logpath /var/log/mongodb/set02-24002.log --logappend --oplogSize 1024 &

nohup mongod --shardsvr --replSet set03 --bind_ip_all --port 24003 --dbpath /var/lib/mongodb/set03 --logpath /var/log/mongodb/set02-24003.log --logappend --oplogSize 1024 &

nohup mongod --shardsvr --replSet set04 --bind_ip_all --port 24004 --dbpath /var/lib/mongodb/set04 --logpath /var/log/mongodb/set02-24004.log --logappend --oplogSize 1024 &

nohup mongod --shardsvr --replSet set05 --bind_ip_all --port 24005 --dbpath /var/lib/mongodb/set05 --logpath /var/log/mongodb/set02-24005.log --logappend --oplogSize 1024 &

# Connect to one member of the shard replica set
mongo --host 10.12.109.176 --port 24001

# Initiate the replica set
rs.initiate(
  {
    _id : "set01",
    members: [
	  { _id : 0, host : "10.12.109.175:24001" },
      { _id : 1, host : "10.12.109.176:24001" },
      { _id : 2, host : "10.12.109.178:24001" }
    ]
  }
)

# Connect to one member of the shard replica set
mongo --host 10.12.109.176 --port 24002

# Initiate the replica set
rs.initiate(
  {
    _id : "set02",
    members: [
	  { _id : 0, host : "10.12.109.175:24002" },
      { _id : 1, host : "10.12.109.176:24002" },
      { _id : 2, host : "10.12.109.178:24002" }
    ]
  }
)

# Connect to one member of the shard replica set
mongo --host 10.12.109.176 --port 24003

# Initiate the replica set
rs.initiate(
  {
    _id : "set03",
    members: [
	  { _id : 0, host : "10.12.109.175:24003" },
      { _id : 1, host : "10.12.109.176:24003" },
      { _id : 2, host : "10.12.109.178:24003" }
    ]
  }
)

# Connect to one member of the shard replica set
mongo --host 10.12.109.176 --port 24004

# Initiate the replica set
rs.initiate(
  {
    _id : "set04",
    members: [
	  { _id : 0, host : "10.12.109.175:24004" },
      { _id : 1, host : "10.12.109.176:24004" },
      { _id : 2, host : "10.12.109.178:24004" }
    ]
  }
)

# Connect to one member of the shard replica set
mongo --host 10.12.109.176 --port 24005

# Initiate the replica set
rs.initiate(
  {
    _id : "set05",
    members: [
	  { _id : 0, host : "10.12.109.175:24005" },
      { _id : 1, host : "10.12.109.176:24005" },
      { _id : 2, host : "10.12.109.178:24005" }
    ]
  }
)


# Connect a mongos to the Sharded Cluster
nohup mongos --bind_ip_all --port 27017 --configdb "configSet/10.12.109.175:28017,10.12.109.176:28017,10.12.109.178:28017" --logpath /var/log/mongodb/mongos.log & 

# Connect to one of the mongos servers
mongo --host 10.12.109.176 --port 27017

# Add Shards to the Cluster
sh.addShard( "set01/10.12.109.175:24001")  # SECONDARY
sh.addShard( "set01/10.12.109.176:24001")  # PRIMARY
sh.addShard( "set01/10.12.109.178:24001")  # SECONDARY

sh.addShard( "set02/10.12.109.175:24002")  # SECONDARY
sh.addShard( "set02/10.12.109.176:24002")  # PRIMARY
sh.addShard( "set02/10.12.109.178:24002")  # SECONDARY

sh.addShard( "set03/10.12.109.175:24003")
sh.addShard( "set03/10.12.109.176:24003")
sh.addShard( "set03/10.12.109.178:24003")

sh.addShard( "set04/10.12.109.175:24004")
sh.addShard( "set04/10.12.109.176:24004")
sh.addShard( "set04/10.12.109.178:24004")

sh.addShard( "set05/10.12.109.175:24005")
sh.addShard( "set05/10.12.109.176:24005")
sh.addShard( "set05/10.12.109.178:24005")

# Enable Sharding for a Database
sh.enableSharding("<database>")

# Shard a Collection
sh.shardCollection("<database>.<collection>", { <key> : <direction> } )

```

### MongoDB 数据库的一般查询语句

```
{ name : "myName" }
{ size : { $gt : 5 } }
{ size : { $gte : 5 } }
{ name : { $in : [ 'item1', 'item2' ] } }
{ size : { $lt : 5 } }
{ size : { $lte : 5 } }
{ name : { $ne : "badName" } }
{ name : { $nin : [ 'item1', 'iem2' ] } }
{ $or : [ { size : { $lt : 5 } }, { size : { $gt : 10 } } ] }
{ $or : [ {}, {} ] }
{ $and : [ { size : { $lt : 5 }  }, { size : { $gt : 2 } } ] }
{ $not : { size : { $lt : 5 } } }
{ $nor : { size : { $gt : 5 } }, { name : "myName" } }
{ speciaField : { $exists : true|false } }
{ speciaField : { $type : <BSONtype> } }
{ number : { $mod : [ 2, 0 ] } }
{ myString : { $regex : 'some.*exp' } }
{ myArr : { $all : [ 'one', 'two', 'three' ] } }
{ myArr : { $elemMatch : { value : { $gt : 5 }, size : { $lt : 6 } } } }
{ myArr : { $size : 5 } }



[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   57G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G  8.6M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G     0  3.2G    0% /run/user/0
[root@dc01 ~]# 


[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   58G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G  8.6M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G     0  3.2G    0% /run/user/0
[root@dc01 ~]# 


mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  1.180GB
mongos> use myDatabase
switched to db myDatabase
mongos> show collections
inventory
mongos> db.inventory.find().count()
42412020
mongos> 
mongos> db.inventory.deleteMany({ item: "mat" })
{ "acknowledged" : true, "deletedCount" : 14137200 }
mongos> db.inventory.find().count()
28274820
mongos> 
mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  1.327GB
mongos> 

[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   59G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G  8.6M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G     0  3.2G    0% /run/user/0
[root@dc01 ~]# 

use myDatabase
db.runCommand ( { compact: 'inventory', force: true } )


sh.addShard( "set01/10.12.109.175:24001")  # SECONDARY
sh.addShard( "set01/10.12.109.176:24001")  # PRIMARY
sh.addShard( "set01/10.12.109.178:24001")  # SECONDARY

sh.addShard( "set02/10.12.109.175:24002")  # SECONDARY
sh.addShard( "set02/10.12.109.176:24002")  # PRIMARY
sh.addShard( "set02/10.12.109.178:24002")  # SECONDARY

sh.addShard( "set03/10.12.109.175:24003")
sh.addShard( "set03/10.12.109.176:24003")
sh.addShard( "set03/10.12.109.178:24003")

sh.addShard( "set04/10.12.109.175:24004")
sh.addShard( "set04/10.12.109.176:24004")
sh.addShard( "set04/10.12.109.178:24004")

sh.addShard( "set05/10.12.109.175:24005")
sh.addShard( "set05/10.12.109.176:24005")
sh.addShard( "set05/10.12.109.178:24005")


[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   58G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G  8.6M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G     0  3.2G    0% /run/user/0
[root@dc01 ~]# 

mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  1.028GB
mongos> 
mongos> 
mongos> db.inventory.deleteMany({})
{ "acknowledged" : true, "deletedCount" : 28274820 }
mongos> db.inventory.find().count()
0
mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  0.964GB
mongos> 

[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   58G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G  8.6M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G     0  3.2G    0% /run/user/0
[root@dc01 ~]# 




[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   57G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G  8.6M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G     0  3.2G    0% /run/user/0
[root@dc01 ~]# 

mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  0.000GB
mongos> 











[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   60G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G   33M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G   12K  3.2G    1% /run/user/0
[root@dc01 ~]# 

mongos> 
mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  2.949GB
mongos> 
mongos> use myDatabase
switched to db myDatabase
mongos> 
mongos> show collections
inventory
mongos> 
mongos> db.inventory.find().count()
104919227
mongos> 
mongos> db.serverStatus().mem
{ "bits" : 64, "resident" : 26, "virtual" : 256, "supported" : true }
mongos> 
mongos> 
mongos> db.inventory.deleteMany({ item: "mat" })
{ "acknowledged" : true, "deletedCount" : 34972742 }
mongos> 
mongos> db.inventory.find().count()
69946485
mongos> 
mongos> show dbs
admin       0.000GB
config      0.001GB
myDatabase  3.125GB
mongos> 
mongos> db.serverStatus().mem
{ "bits" : 64, "resident" : 25, "virtual" : 256, "supported" : true }
mongos> 

[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   60G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G   33M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G   12K  3.2G    1% /run/user/0
[root@dc01 ~]# 

db.repairDatabase()
db.repairDatabase()

[root@dc01 ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
/dev/mapper/cl-root  6.0T   61G  6.0T    1% /
devtmpfs              16G     0   16G    0% /dev
tmpfs                 16G     0   16G    0% /dev/shm
tmpfs                 16G   33M   16G    1% /run
tmpfs                 16G     0   16G    0% /sys/fs/cgroup
/dev/sda2           1014M  139M  876M   14% /boot
tmpfs                3.2G   12K  3.2G    1% /run/user/0
[root@dc01 ~]# 








```


### 修复 MongoDB 数据目录

```
# 停止 mongo 服务后进行修复操作
mongod --repair --dbpath /var/lib/mongodb/set01
mongod --repair --dbpath /var/lib/mongodb/set02
mongod --repair --dbpath /var/lib/mongodb/set03
mongod --repair --dbpath /var/lib/mongodb/set04
mongod --repair --dbpath /var/lib/mongodb/set05

```

### Replication Commands







### Administration Commands

* clean

Internal namespace administration command.

* clone

Deprecated. Copies a database from a remote host to the current host.

* cloneCollection

Copies a collection from a remote host to the current host.

* cloneCollectionAsCapped

Copies a non-capped collection as a new capped collection.

* collMod

Add options to a collection or modify a view definition.

* compact

Defragments a collection and rebuilds the indexes.

Rewrites and defragments all data and indexes in a collection. On WiredTiger databases, this command will release unneeded disk space to the operating system.  对集合中的所有数据和索引进行重写和碎片整理。 在WiredTiger数据库上，此命令将向操作系统释放不需要的磁盘空间。

* connPoolSync

Internal command to flush connection pool.

* convertToCapped

Converts a non-capped collection to a capped collection.

* copydb

Deprecated. Copies a database from a remote host to the current host.

* create

Creates a collection or a view.

* createIndexes

Builds one or more indexes for a collection.

* currentOp

Returns a document that contains information on in-progress operations for the database instance.

* drop

Removes the specified collection from the database.

* dropDatabase

Removes the current database.

* dropIndexes

Removes indexes from a collection.

* filemd5

Returns the md5 hash for files stored using GridFS.

* fsync

Flushes pending writes to the storage layer and locks the database to allow backups.

* fsyncUnlock

Unlocks one fsync lock.

* getParameter

Retrieves configuration options.

* killCursors

Kills the specified cursors for a collection.

* killOp

Terminates an operation as specified by the operation ID.

* listCollections

Returns a list of collections in the current database.

* listDatabases

Returns a document that lists all databases and returns basic database statistics.

* listIndexes

Lists all indexes for a collection.

* logRotate

Rotates the MongoDB logs to prevent a single file from taking too much space.

* reIndex

Rebuilds all indexes on a collection.

* renameCollection

Changes the name of an existing collection.

* repairDatabase

Rebuilds the database and indexes by discarding invalid or corrupt data.

Rebuilds the database and indexes by discarding invalid or corrupt data that may be present due to an unexpected system restart or shutdown. repairDatabase is analogous to a fsck command for file systems.  通过丢弃由于意外系统重新启动或关闭而可能存在的无效或损坏数据来重建数据库和索引。 repairDatabase类似于文件系统的fsck命令。

* setFeatureCompatibilityVersion

Enables or disables features that persist data that are backwards-incompatible.

* setParameter

Modifies configuration options.

* shutdown

Shuts down the mongod or mongos process.

* touch

Loads documents and indexes from data storage to memory.

### Diagnostic Commands 诊断命令

* availableQueryOptions

Internal command that reports on the capabilities of the current MongoDB instance.

* buildInfo

Displays statistics about the MongoDB build.

* collStats

Reports storage utilization statics for a specified collection.

* connPoolStats

Reports statistics on the outgoing connections from this MongoDB instance to other MongoDB instances in the deployment.

* connectionStatus

Reports the authentication state for the current connection.

* cursorInfo

Removed in MongoDB 3.2. Replaced with metrics.cursor.

* dataSize

Returns the data size for a range of data. For internal use.

* dbHash

Returns hash value a database and its collections.

* dbStats

Reports storage utilization statistics for the specified database.

* diagLogging

Removed in MongoDB 3.6. To capture, replay, and profile commands sent to your MongoDB deployment, use mongoreplay.

* driverOIDTest

Internal command that converts an ObjectId to a string to support tests.

* explain

Returns information on the execution of various operations.

* features

Reports on features available in the current MongoDB instance.

* getCmdLineOpts

Returns a document with the run-time arguments to the MongoDB instance and their parsed options.

* getLog

Returns recent log messages.

* hostInfo

Returns data that reflects the underlying host system.

* isSelf

Internal command to support testing.

* listCommands

Lists all database commands provided by the current mongod instance.

* netstat

Internal command that reports on intra-deployment connectivity. Only available for mongos instances.

* ping

Internal command that tests intra-deployment connectivity.

* profile

Interface for the database profiler.

* serverStatus

Returns a collection metrics on instance-wide resource utilization and status.

* shardConnPoolStats

Reports statistics on a mongos’s connection pool for client operations against shards.

* top

Returns raw usage statistics for each database in the mongod instance.

* validate

Internal command that scans for a collection’s data and indexes for correctness.

* whatsmyuri

Internal command that returns information on the current client.


