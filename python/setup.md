`setup` 函数常用的参数如下：

|参数|说明|相关选项|
|:--|:--|:--|
|name|包名称||
|version|包版本||
|author|程序的作者||
|author_email|程序的作者的邮箱地址||
|maintainer|维护者||
|maintainer_email|维护者的邮箱地址||
|url|程序的官网地址||
|license|程序的授权信息||
|description|程序的简单描述||
|long_description|程序的详细描述||
|platforms|程序适用的软件平台列表||
|classifiers|程序的所属分类列表||
|keywords|程序的关键字列表||
|packages|需要处理的包目录(通常为包含 `__init__.py` 的文件夹)|find_packages()、package_dir|
|package_dir|指定哪些目录下的文件被映射到哪个源码包||
|py_modules|需要打包的 Python 单文件列表||
|download_url|程序的下载地址||
|package_data|指定包内需要包含的数据文件|include_package_data、exclude_package_data、data_files、MANIFEST.in（manifest template）|
|include_package_data|自动包含包内所有受版本控制(cvs/svn/git)的数据文件||
|exclude_package_data|当 include_package_data 为 True 时该选项用于排除部分文件||
|data_files|打包时需要打包的数据文件，如图片，配置文件等||
|ext_modules|指定扩展模块，用于构建 C 和 C++ 扩展扩展包||
|scripts|指定可执行脚本,安装时脚本会被安装到系统 PATH 路径下|entry_points、cmdclass|
|entry_points|动态发现服务和插件||
|cmdclass|添加自定义命令||
|requires|指定依赖的其他包||
|provides|指定可以为哪些模块提供依赖||
|install_requires|安装时需要安装的依赖包|dependency_links|
|dependency_links|指定依赖包的下载地址||
|setup_requires|指定运行 setup.py 文件本身所依赖的包||
|extras_require|当前包的高级/额外特性需要依赖的分发包||
|zip_safe|不压缩包，而是以目录的形式安装||
||||
|--|||

更多参数可见：[https://setuptools.readthedocs.io/en/latest/setuptools.html](https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata)

[参考1](https://blog.konghy.cn/2018/04/29/setup-dot-py/)

[参考2](https://lingxiankong.github.io/2013-12-23-python-setup.html)

[参考3 - 重点](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/)


