# ElasticSearch

- [基础内容]()

	- [索引管理]()
		- [新建索引]()
		- [更新副本]()
		- [读写权限]()
		- [查看索引]()
		- [删除索引]()
		- [索引的打开与关闭]()
		- [复制索引]()
		- [收缩索引]()
		- [索引别名]()

	- [文档管理]()
		- [新建文档]()
		- [获取文档]()
		- [更新文档]()
		- [查询更新]()
		- [删除文档]()
		- [查询删除]()
		- [批量操作]()
		- [版本控制]()
		- [路由机制]()

	- [映射]()
		- [映射分类]()
		- [动态映射]()
		- [日期检测]()
		- [静态映射]()
		- [字段类型]()
		- [元字段]()
		- [映射参数]()
		- [映射模板]()

	- [搜索与过滤]()
		- [搜索机制]()
		- [全文查询]()
		- [词项查询]()
		- [复合查询]()
		- [嵌套查询]()
		- [位置查询]()
		- [特殊查询]()
		- [搜索高亮]()
		- [搜索排序]()

	- [聚合]()
		- [指标聚合]()
		- [桶聚合]()

	- [cat api]()

	- [cluster api]()






## 基础内容

### 索引管理

1. 新建索引
2. 更新副本
3. 读写权限
4. 查看索引
5. 删除索引
6. 索引的打开与关闭
7. 复制索引
8. 收缩索引
9. 索引别名

### 文档管理

1. 新建文档
2. 获取文档
3. 更新文档
4. 查询更新
5. 删除文档
6. 查询删除
7. 批量操作
8. 版本控制
9. 路由机制

### 映射

1. 映射分类
2. 动态映射
3. 日期检测
4. 静态映射
5. 字段类型
6. 元字段
7. 映射参数
8. 映射模板

### 搜索与过滤

示例数据
```json
{"index":{ "_index": "books", "_type": "IT", "_id": "1" }}
{"id":"1","title":"Java编程思想","language":"java","author":"Bruce Eckel","price":70.20,"publish_time":"2007-10-01","description":"Java学习必读经典,殿堂级著作！赢得了全球程序员的广泛赞誉。"}

{"index":{ "_index": "books", "_type": "IT", "_id": "2" }}
{"id":"2","title":"Java程序性能优化","language":"java","author":"葛一鸣","price":46.50,"publish_time":"2012-08-01","description":"让你的Java程序更快、更稳定。深入剖析软件设计层面、代码层面、JVM虚拟机层面的优化方法"}

{"index":{ "_index": "books", "_type": "IT", "_id": "3" }}
{"id":"3","title":"Python科学计算","language":"python","author":"张若愚","price":81.40,"publish_time":"2016-05-01","description":"零基础学python,光盘中作者独家整合开发winPython运行环境，涵盖了Python各个扩展库"}

{"index":{ "_index": "books", "_type": "IT", "_id": "4" }}
{"id":"4","title":"Python基础教程","language":"python","author":"Helant","price":54.50,"publish_time":"2014-03-01","description":"经典的Python入门教程，层次鲜明，结构严谨，内容翔实"}

{"index":{ "_index": "books", "_type": "IT", "_id": "5" }}
{"id":"5","title":"JavaScript高级程序设计","language":"javascript","author":"Nicholas C. Zakas","price":66.40,"publish_time":"2012-10-01","description":"JavaScript技术经典名著"}
```
1. 搜索机制
2. 全文查询
3. 词项查询
4. 复合查询
5. 嵌套查询
6. 位置查询
7. 特殊查询
8. 搜索高亮
9. 搜索排序

### 聚合

1. 指标聚合
2. 桶聚合

### cat api

### cluster api
