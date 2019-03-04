#mongodb:非关系型数据库
##一： 非关系型数据库NoSQL全称--Not Only Sql
非关系型数据库主要特点： 非关系型的、分布式的、开源的、水平可扩展的。
（模式自由，支持简易赋值、简单的API、大容量数据等）

##二：mongodb简介：
**mongodb是C++编写的基于分布式文件存储的数据库，一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最想关系数据库的非关系型数据库。存储方式和Redis类似，是bson(json的扩展)格式的kav-value存储方式，只是Redis是内存存储，而MongoDB是和普通的数据库目录一样存储在硬盘上**

####最大特点：支持的查询语言非常强大，语法有点类似于面向对象的查询语言，几乎可以实现类似关系数据库表单查询的绝大部分功能。它是一个面向集合的，模式自由的文档型数据库。
#####1.面向集合（Collection-Orented）
意思是数据被分组存储在数据集中，被称为一个集合（Collection）,每个集合在数据库中都有一个唯一的标识名，并且可以包含无限数目的文档（取决于磁盘大小）。集合的概念类似关系型数据库里面的table,不同的是它不需要定义任何模式；
#####2.模式自由（schema-free）
存储在MongoDB数据库中的文件，我们不需要知道他的任何结构定义。唯一的模式就是以字典的形式存储，但是字典的value可以任意定义，只要符合字典对象本身的定义。
#####3.文档型
意思是我们存储的数据是键值对的集合，键是字符串，值可以是任意数据类型，包括数组和文档.文件存储格式为BSON（一种json的扩展）
####使用场景：
#####1.网络数据：
mongodb非常适合实时插入，更新与查询，并具备网站实时数据存储所需要的复制及高度伸缩性；
#####2.缓存：
由于性能很高，mongodb也适合作为信息基础设施的缓存层，在系统重启之后，由mongodb他讲的持久化缓存层可以避免下沉的数据源过载；
#####3.大尺寸低价值的数据：
使用传统的关系型数据库存储一些数据时可能会比较昂贵，对于低价值，但是量大的数据来说，用传统的关系型数据库，性价比较低，但是用mongodb不存在这个问题（在mongodb之前，一般用传统的文件类型来存储这种数据）；
#####4.高收缩性的场景：
mongodb非常适合由数十或数百台服务器组成的数据库。mongodb的路线图中已经包含对MapReduce引擎的内置支持；
#####5.用于对象以及json数据的存储：
mongodb的bson数据格式非常适合文档化格式的存储和查询；
##三：安装mongodb
#####1.windows系统中安装：
	第一步：下载mangodb -- 在官方网站下载与电脑相应版本的安装包--https://www.mongodb.com/download-center/community（msi代表安装程序，zip代表压缩包）
	第二步：安装 -- 点击开下载的安装包，跟着步骤点击（msi文件，zip解压后在点击exe文件），最好指定一个文件夹作为安装目录，也可以直接点默认安装，最后一步可能会弹出一个有三个按钮的弹出框，内容是mongodb服务启动失败，点击最后一个ignore（忽略）。
	第三步：在放mongodb安装文件夹的同级文件夹建立一个data文件夹，在data文件夹下创建db文件夹
	第四步：启动服务和客户端--在cmd终端中进入放安装文件的路径中的bin文件夹，该文件夹下的mongod.exe是服务器，mongo.exe是客户端,先输入服务器文件名启动，在另外开一cmd终端相同步骤启动客户端
##四： mongodb的使用
#####1. mongodb数据库结构组成：数据库 --> 集合 --> 文档 -- >数据

		数据库 -- 多个集合组成的数据库  (类似mysql中的table)
		集合 -- 多个文档组成的集合  （类似mysql中的database）
		文档 -- mongodb逻辑存储的最小单元，是一个字典类型数据  （类似mysql中的记录）
        数据 -- BSON（Binary Json）json格式的扩展
#####2. mongodb命令：
		show dbs -- 查看数据库；
		use taobao -- 打开taobao这个数据库（数据库并没有添加，但我们在给数据库中的集合插入一条文档的时候就会自动创建一条文档、一个集合、一个数据库）
		show collections -- 查看集合 
		show tables -- 查看集合
		
		插入文档（goods集合只在插入文档的时候才会创建，文档以字典形式插入）
		db.goods.insert({'uid': 2, 'uname': 'luoshuxiao', 'type': 'clothes'})
		
		查询数据（文档）
		db.goods.find()
		db.goods.findone({'uid':2})
		
		删除数据（文档）
		db.goods.remove({'uid':2})
		
		清空集合
		db.goods.remove({})
		
		删除集合
		db.goods.drop()
		
		更新文档(第一个字典为查询到的某个文档，第二个字典文档将完全覆盖查询到的第一个文档)
		db.goods.update({'uid':2}, {'name': 'jon'})
		
		使用修改器 -- $inc修改文档（将第一个字典查询到的文档中的num的值加100）
		db.goods.update({'uid':2}, {'$inc': {'num': 100}})
		db.goods.update({'uid':2}, {'$inc': {'num': -100}}) （减100）
		
		添加一个字段 -- $set修改器
		db.goods.update({'uid': 2}, {'$set':{'color': 'red'}})
		
		删除一个字段 -- $unset修改器
		db.goods.update({'uid': 2}, {'$unset':{'color': true}})
		
		更新某个文档中某个key的值 -- $push
		db.goods.update({'uid': 2}, {'$push': {'email': 'abc'}})
		
		向某个文档中的key的多个值中添加值(不检查key是否存在) -- $pushAll
		db.goods.update({'uid': 2}, {'$pushAll': {'email': ['a','b','c','d']}})
		
		向某个文档中的key的多个值中添加一个不重复的元素(原来有就不添加) -- addToSet
		db.goods.update({'uid': 2}, {'$addToSet': {'email': 'e'}})
		
		向某个文档中的key的多个值中添加多个不重复的元素(原来有就不添加) -- addToSet
		db.goods.update({'uid': 2}, {'$addToSet': {'email': {'$each':['a','d','h','c']}}})
		
		删除数组元素
		db.goods.updaate({'uid': 2}, {'$pop': {'email': -1}})  #从左侧删除一个元素
		db.goods.updaate({'uid': 2}, {'$pop': {'email': 1}})  #从右侧删除一个元素
		db.goods.updaate({'uid': 2}, {'$pull': {'email': 'b'}})  #删除文档中指定的email中的b
		db.goods.updaate({'uid': 2}, {'$popAll': {'email': ['a','b','c']}})  #删除数组内指定的多个元素
		
		修改文档中某个key对应的value的多个值当中的某个值（通过下标修改）
		db.goods.update({'uid': 2}, {'$set': {'email.0': 'time.qq.com'}})
		
		比较运算：
		db.goods.find({'num': 200}).pretty()  （查询条件：等于）
		db.goods.find({'num': {$lt:200}}).pretty()  （查询条件：小于）
		db.goods.find({'num': {$lte:200}}).pretty()  （查询条件：小于等于）
		db.goods.find({'num': {$gt:200}}).pretty()  （查询条件：大于）
		db.goods.find({'num': {$gte:200}}).pretty()  （查询条件：大于等于）
		
		逻辑运算：
		db.goods.find({'uid':2, 'num': 200}).pretty()  （查询条件：并且）
		db.goods.find({$or:[{'uid':2}, {'num': 300}]}).pretty()  （查询条件：等于）

##五： pymongo -- python中使用mongodb

### 第一步：与mongodb建立连接
####1. 安装pymongo -- 
    pip install pymongo(在项目的虚拟环境中安装pymongo三方库)
####2. 导入pymongo -- 
    from pymongo import MongoClient
####3. 创建连接对象 -- 
    client = MongoClient() 或者 client = MongoClient('mongodb://127.0.0.1:27019')
####4. 创建数据库对象 -- 
    db = client.taobao 或者 db = client['taobao']
####5. 创建集合对象 -- 
    coll = db.goods 或者 coll = db['goods']
### 第二步： 操作数据 
####1.插入一条数据 --
    coll.insert_one({'uid': 3, 'num': 400, 'color': 'white'})
####2.插入多条数据 --
    coll.insert_many([{'x': i} for i in range(3)])
####3.查询所有文档 -- 
    coll.find()   -- 查询出来的是列表集合
####4.查询最上层的key-value --
    coll.find({'uid': 2})
####5.查询内层嵌套的 -- 
    coll,find({'key1.key2': 'value2'})  -- 外层key1的value值中的key2的值为value2的文档
####6.操作符查询 -- 
    coll.find({'date.num': {'$gt': 100}}) -- 外层date中的num的值大于100的文档
####7.逻辑运算查询 -- 
    coll.find({'uid': 2, 'num': 300}) -- 外层uid是2并且num是300的文档
    coll.find({'$or': [{'uid': 2},{'num':100}]}) --外层uid是2或者num是100的文档
####8.find_one查询 --
    cool.find_one({'uid':2}) -- 返回的是json数据，可直接使用
####9.排序查询sort(使用了列表) --
    pymongo.ASCENDING = 1
    pymongo.DESCENDING = -1
    coll.find().sort('uid') -- 默认查询结果升序输出，排序标准是uid的值
    coll.find().sort([
           ('uid', pymongo.ASCENDING),
           ('num', pymongo.DESCENDING)
    ]) -- 先按uid的升序排，如果有相等的，相等的再按num的降序排
####10.更新文档 --
update_one(filter, update, upsert=False) -- 返回结果是一个UpdateResult对象，如果查询到多个，则只更新第一个

	coll..update_one(
	 {“name”: “Juni”},
	 {
	 “$set”: {
	 “cuisine”: “American (New)”
	 },
	 “$currentDate”: {“lastModified”: True}
	 }
	)
update_many(filter, update, upsert=False) -- 查询到多少，就更新多少

	coll.update_many(
	 {“address.zipcode”: “10016”, “cuisine”: “Other”},
	 {
	 “$set”: {“cuisine”: “Category To Be Determined”},
	 “$currentDate”: {“lastModified”: True}
	 }
	)

replace_one(filter, replacement, upsert=False) -- 查询到就替换第一个

find_one_and_update(filter, update, projection=None, sort=None,return_document=ReturnDocument.BEFORE, **kwargs) -- 查询到一个并更新一个

####11.删除文档 -- 

	删除一个 -- coll.delete_one({'uid':2})
	删除多个 -- coll.delete_many({'num': 100})
	删除全部 -- coll.delete_many({})
	删除整个集合 -- coll.drop() -- (drop_collection()的别名)
