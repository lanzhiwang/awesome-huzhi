```bash
lanzhiwang@lanzhiwang-desktop:~/work$ ./minio server /home/lanzhiwang/work/data/

Endpoint:  http://192.168.53.116:9000  http://10.0.3.15:9000  http://172.17.0.1:9000  http://127.0.0.1:9000
AccessKey: UAZ61857T74VG0UZ5HY3 
SecretKey: K6d5u5DXCGCZpkJygOYQ2J4pXTSjMI2+XVtTAaFo 

Browser Access:
   http://192.168.53.116:9000  http://10.0.3.15:9000  http://172.17.0.1:9000  http://127.0.0.1:9000

Command-line Access: https://docs.minio.io/docs/minio-client-quickstart-guide
   $ mc config host add myminio http://192.168.53.116:9000 UAZ61857T74VG0UZ5HY3 K6d5u5DXCGCZpkJygOYQ2J4pXTSjMI2+XVtTAaFo

Object API (Amazon S3 compatible):
   Go:         https://docs.minio.io/docs/golang-client-quickstart-guide
   Java:       https://docs.minio.io/docs/java-client-quickstart-guide
   Python:     https://docs.minio.io/docs/python-client-quickstart-guide
   JavaScript: https://docs.minio.io/docs/javascript-client-quickstart-guide
   .NET:       https://docs.minio.io/docs/dotnet-client-quickstart-guide

```



```bash
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc config host add myminio http://127.0.0.1:9000 BVQSMUM4H937HVXBRKUC UmjIONAPngrq+YChuJaYa+Jw1oD5Pv3IdEsc44em
mc: Configuration written to `/home/lanzhiwang/.mc/config.json`. Please update your access credentials.
mc: Successfully created `/home/lanzhiwang/.mc/share`.
mc: Initialized share uploads `/home/lanzhiwang/.mc/share/uploads.json` file.
mc: Initialized share downloads `/home/lanzhiwang/.mc/share/downloads.json` file.
Added `myminio` successfully.
lanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc mb myminio/test1
Bucket created successfully `myminio/test1`.
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc mb myminio/test2
Bucket created successfully `myminio/test2`.
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc mb myminio/test3
Bucket created successfully `myminio/test3`.
lanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc ls myminio
[2018-11-14 16:39:20 CST]     0B test1/
[2018-11-14 16:39:25 CST]     0B test2/
[2018-11-14 16:39:27 CST]     0B test3/
lanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp ./1.png myminio/test1/
./1.png:                  12.04 KB / 12.04 KB ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃ 100.00% 3.39 MB/s 0slanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp ./2.png myminio/test1/
./2.png:                  12.04 KB / 12.04 KB ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃ 100.00% 2.46 MB/s 0slanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp ./3.png myminio/test1/
./3.png:                  12.04 KB / 12.04 KB ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃ 100.00% 3.21 MB/s 0slanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp ./4.png myminio/test1/
./4.png:                  12.04 KB / 12.04 KB ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃ 100.00% 3.17 MB/s 0slanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp ./5.png myminio/test1/
./5.png:                  12.04 KB / 12.04 KB ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃ 100.00% 3.37 MB/s 0slanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp ./6.png myminio/test1/
./6.png:                  12.04 KB / 12.04 KB ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃ 100.00% 906.74 KB/s 0s

lanzhiwang@lanzhiwang-desktop:~/work$ ./mc ls myminio/test1/
[2018-11-14 16:40:15 CST]  12KiB 1.png
[2018-11-14 16:40:25 CST]  12KiB 2.png
[2018-11-14 16:40:37 CST]  12KiB 3.png
[2018-11-14 16:40:43 CST]  12KiB 4.png
[2018-11-14 16:40:49 CST]  12KiB 5.png
[2018-11-14 16:40:54 CST]  12KiB 6.png
lanzhiwang@lanzhiwang-desktop:~/work$ 

lanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ ./mc cp myminio/test1/1.png 1-other.png
lanzhiwang@lanzhiwang-desktop:~/work$ tree -a data1
data1
├── .minio.sys
│   ├── config
│   │   └── config.json
│   │       ├── part.1
│   │       └── xl.json
│   ├── format.json
│   ├── multipart
│   └── tmp
├── test1
│   ├── 1.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 2.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 3.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 4.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 5.png
│   │   ├── part.1
│   │   └── xl.json
│   └── 6.png
│       ├── part.1
│       └── xl.json
├── test2
└── test3

14 directories, 15 files
lanzhiwang@lanzhiwang-desktop:~/work$ 
lanzhiwang@lanzhiwang-desktop:~/work$ tree -a data2
data2
├── .minio.sys
│   ├── config
│   │   └── config.json
│   │       ├── part.1
│   │       └── xl.json
│   ├── format.json
│   ├── multipart
│   └── tmp
├── test1
│   ├── 1.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 2.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 3.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 4.png
│   │   ├── part.1
│   │   └── xl.json
│   ├── 5.png
│   │   ├── part.1
│   │   └── xl.json
│   └── 6.png
│       ├── part.1
│       └── xl.json
├── test2
└── test3

14 directories, 15 files
lanzhiwang@lanzhiwang-desktop:~/work$ 


在所有的节点上执行下列命令
$ export MINIO_ACCESS_KEY=minio
$ export MINIO_SECRET_KEY=miniostorage
$ minio server http://node{1...8}.example.com/mnt/export/{1...8}
#$ minio server http://hz{1...4}/root/minio-data

export MINIO_ACCESS_KEY=minio && export MINIO_SECRET_KEY=miniostorage

nohup ./minio server http://172.16.24.11/root/minio-data http://172.16.24.12/root/minio-data http://172.16.24.13/root/minio-data http://172.16.24.14/root/minio-data > /root/minio-output.log 2>&1 &


mc config host add myminio http://172.16.24.11:9000 minio miniostorage

```





```bash
[root@hz1 ~]# ./minio --help
NAME:
  minio - Cloud Storage Server.

DESCRIPTION:
  Minio is an Amazon S3 compatible object storage server. Use it to store photos, videos, VMs, containers, log files, or any blob of data as objects.

USAGE:
  minio [FLAGS] COMMAND [ARGS...]

COMMANDS:
  server   Start object storage server.
  gateway  Start object storage gateway. 使用 Azure、GCS、NAS 作为后端存储，不使用本地目录
  update   Check for a new software update.
  version  Print version.
  
FLAGS:
  --config-dir value, -C value  Path to configuration directory. (default: "/root/.minio")
  --quiet                       Disable startup information.
  --json                        Output server logs and startup information in json format.
  --help, -h                    Show help.
  
VERSION:
  2018-11-06T01:01:02Z
[root@hz1 ~]# 


[root@hz1 ~]# ./mc --help
NAME:
  mc - Minio Client for cloud storage and filesystems.

USAGE:
  mc [FLAGS] COMMAND [COMMAND FLAGS | -h] [ARGUMENTS...]

COMMANDS:
  ls       List files and folders.查看文件或者目录
  mb       Make a bucket or a folder. 创建 bucket
  cat      Display file and object contents.
  pipe     Redirect STDIN to an object or file or STDOUT.
  share    Generate URL for sharing. 生成上传或者下载的共享链接
  cp       Copy files and objects. 上传下载文件
  mirror   Mirror buckets and folders.
  find     Search for files and objects.
  select   Run select queries on objects.
  stat     Stat contents of objects and folders.
  diff     List differences in object name, size, and date between folders.
  rm       Remove files and objects.
  events   Manage object notifications.
  watch    Watch for file and object events.
  policy   Manage anonymous access to objects.
  admin    Manage Minio servers
  session  Manage saved sessions for cp command.
  config   Manage mc configuration file.
  update   Check for a new software update.
  version  Print version info.
  
GLOBAL FLAGS:
  --config-folder value, -C value  Path to configuration folder. (default: "/root/.mc")
  --quiet, -q                      Disable progress bar display.
  --no-color                       Disable color theme.
  --json                           Enable JSON formatted output.
  --debug                          Enable debug output.
  --insecure                       Disable SSL certificate verification.
  --help, -h                       Show help.
  
VERSION:
  2018-11-06T01:12:20Z
[root@hz1 ~]# 


```



[Systemd](https://github.com/minio/minio-service)

[Linux服务器上Minio生产环境的内核调优](https://blog.csdn.net/dingjs520/article/details/79111037)





缺点

* 社区不够成熟，业界参考资料较少
* 不支持动态增加节点，minio创始人的设计理念就是动态增加节点太复杂，后续会采用其它方案来支持扩容。 

