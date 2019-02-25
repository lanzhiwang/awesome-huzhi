### Windows 常用命令

```
进入 D 盘
d:

返回上一级
cd ..

列出文件夹下所有文件及文件夹
dir

在当前文件夹下新建test文件夹
md test

d盘下新建文件夹
md d:\test\my

进入test文件夹
cd test

新建cc.txt文件
cd .> cc.txt

打印文件内容
type cc.txt

删除a.txt的文件
del a.txt

删除所有后缀为.txt的文件
del *.txt

删除名为test的空文件夹
rd test

删除D盘里的test文件夹，删除之前确认
rd /s D:\test

删除此文件夹下的所有文件，删除之前确认
rd test/s

主机名
hostname
```

### windows提权-快速查找exp
```
systeminfo > micropoor.txt

dir

type micropoor.txt

type micropoor.txt | find /i "KB4343669"

for %i in (KB977165 KB2160329 KB2503665 KB2592799 KB2707511 KB2829361 KB2850851 KB3000061 KB3045171 KB3077657 KB3079904 KB3134228 KB3143141 KB3141780 KB4343669) do @echo %i

for %i in (KB977165 KB2160329 KB2503665 KB2592799 KB2707511 KB2829361 KB2850851 KB3000061 KB3045171 KB3077657 KB3079904 KB3134228 KB3143141 KB3141780 KB4343669) do @type micropoor.txt

查找未打补丁的exp
for %i in (KB977165 KB2160329 KB2503665 KB2592799 KB2707511 KB2829361 KB2850851 KB3000061 KB3045171 KB3077657 KB3079904 KB3134228 KB3143141 KB3141780 KB4343669) do @type micropoor.txt | @find /i "%i" || @echo %i

del /f /q /a micropoor.txt

D:\>whoami
desktop-ogsr9rr\rzx-hz

D:\>
D:\>net user rzx-hz
用户名                 rzx-hz
全名
注释
用户的注释
国家/地区代码          000 (系统默认值)
帐户启用               Yes
帐户到期               从不

上次设置密码           2019/1/7 15:30:24
密码到期               从不
密码可更改             2019/1/7 15:30:24
需要密码               No
用户可以更改密码       Yes

允许的工作站           All
登录脚本
用户配置文件
主目录
上次登录               2019/2/25 13:34:26

可允许的登录小时数     All

本地组成员             *Administrators
全局组成员             *None
命令成功完成。


D:\>

MS11_80_k8.exe

```

