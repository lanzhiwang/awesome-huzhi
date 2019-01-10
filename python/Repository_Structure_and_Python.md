## Python 项目结构



### 一般 Python 项目结构

```bash
$ tree -a .
.
├── docs
│   ├── conf.py
│   └── index.rst
├── LICENSE
├── Makefile
├── README.rst
├── requirements.txt
├── sample
│   ├── core.py
│   ├── helpers.py
│   └── __init__.py
├── setup.py
└── tests
    ├── context.py
    ├── test_advanced.py
    └── test_basic.py

3 directories, 13 files
$ 


```



### Django 项目结构

```bash
$ django-admin startproject mysite
$ ll -a
total 12
drwxrwxr-x 3 lanzhiwang lanzhiwang 4096 10月 30 21:48 ./
drwxrwxr-x 4 lanzhiwang lanzhiwang 4096 10月 30 21:47 ../
drwxrwxr-x 3 lanzhiwang lanzhiwang 4096 10月 30 21:48 mysite/
$ tree -a .
.
└── mysite
    ├── manage.py
    └── mysite  # 出现嵌套的 mysite 目录
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

2 directories, 5 files
$ 
$ django-admin startproject mysite .
$ ll
total 16
drwxrwxr-x 3 lanzhiwang lanzhiwang 4096 10月 30 21:50 ./
drwxrwxr-x 4 lanzhiwang lanzhiwang 4096 10月 30 21:47 ../
-rwxrwxr-x 1 lanzhiwang lanzhiwang  804 10月 30 21:50 manage.py*
drwxrwxr-x 2 lanzhiwang lanzhiwang 4096 10月 30 21:50 mysite/
$ tree -a .
.
├── manage.py
└── mysite  # 只有一级目录 mysite 
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 5 files
$ 

```



[参考](https://www.kennethreitz.org/essays/repository-structure-and-python)

