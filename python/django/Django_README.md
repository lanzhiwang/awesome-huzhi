# Django

* `django-admin startproject mysite`
* `django-admin startproject mysite .`

```bash
(venv) huzhi@huzhideMacBook-Pro django-example % pwd
/Users/huzhi/work/code/django-example
(venv) huzhi@huzhideMacBook-Pro django-example % django-admin startproject mysite
(venv) huzhi@huzhideMacBook-Pro django-example % ll
total 0
drwxr-xr-x   3 huzhi  staff   96  4 24 19:05 ./
drwxr-xr-x  26 huzhi  staff  832  4 24 18:33 ../
drwxr-xr-x   4 huzhi  staff  128  4 24 19:05 mysite/
(venv) huzhi@huzhideMacBook-Pro django-example % tree .
.
└── mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

2 directories, 6 files
(venv) huzhi@huzhideMacBook-Pro django-example %
(venv) huzhi@huzhideMacBook-Pro django-example % ll
total 0
drwxr-xr-x   3 huzhi  staff   96  4 24 19:05 ./
drwxr-xr-x  26 huzhi  staff  832  4 24 18:33 ../
drwxr-xr-x   4 huzhi  staff  128  4 24 19:05 mysite/
(venv) huzhi@huzhideMacBook-Pro django-example %
(venv) huzhi@huzhideMacBook-Pro django-example % rm -rf mysite
(venv) huzhi@huzhideMacBook-Pro django-example %
(venv) huzhi@huzhideMacBook-Pro django-example % django-admin startproject mysite .
(venv) huzhi@huzhideMacBook-Pro django-example %
(venv) huzhi@huzhideMacBook-Pro django-example % tree .
.
├── manage.py
└── mysite
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 6 files
(venv) huzhi@huzhideMacBook-Pro django-example %

```

* `django-admin startproject mysite`

```bash
(venv) huzhi@huzhideMacBook-Pro django-example % pwd
/Users/huzhi/work/code/django-example
(venv) huzhi@huzhideMacBook-Pro django-example % django-admin startproject mysite
(venv) huzhi@huzhideMacBook-Pro django-example % tree .
.
└── mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

2 directories, 6 files

# python manage.py startapp blog
# manage.py 是对 django-admin 的简单封装
(venv) huzhi@huzhideMacBook-Pro django-example % django-admin startapp blog
(venv) huzhi@huzhideMacBook-Pro django-example % tree .
.
├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

4 directories, 13 files
(venv) huzhi@huzhideMacBook-Pro django-example %

```

* `django-admin startproject mysite .`

```bash
(venv) huzhi@huzhideMacBook-Pro django-example % pwd
/Users/huzhi/work/code/django-example
(venv) huzhi@huzhideMacBook-Pro django-example % django-admin startproject mysite .
(venv) huzhi@huzhideMacBook-Pro django-example % tree .
.
├── manage.py
└── mysite
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 6 files

# python manage.py startapp blog
(venv) huzhi@huzhideMacBook-Pro django-example % django-admin startapp blog
(venv) huzhi@huzhideMacBook-Pro django-example % tree .
.
├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

3 directories, 13 files
(venv) huzhi@huzhideMacBook-Pro django-example %

```

> manage.py 是对 django-admin 的简单封装



* URL 处理



```
U「lpatte「ns = [
```









## 基于类的视图

```python
UpdateView

object

DeleteView

BaseUpdateView

BaseDetailView
```

