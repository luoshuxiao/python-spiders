#爬虫框架：scrapy
**特点：爬取效率高、扩展性前、python编写跨平台运行**

##一： 数据流由执行引擎控制，过程如下：
	1.引擎打开一个网站（open a domain）, 找到处理该往回走哪的spider并向该spider请求一个要爬取的URL；
	2. 引擎从Spider中获取到第⼀个要爬取的URL并在调度器(Scheduler)以Request调度。
	3、引擎向调度器请求下⼀个要爬取的URL。
	4、调度器返回下⼀个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)⽅向)转发给下载器(Downloader)。
	5、一旦页面下载完成，下载器⽣成⼀个该⻚⾯的Response，并将其通过下载中间件(返回(response)⽅向)发送给引擎。
	6、引擎从下载器中接收到Response并通过Spider中间件(输⼊⽅向)发送给Spider处理。
	7、Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
	8、引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度器。
	9、(从第⼆步)重复直到调度器中没有更多地request，引擎关闭该⽹站。
##二： 安装scrapy(以下是windows步骤，linux系统或者苹果电脑不用，直接pip install scrapy)
###1.下载安装scrapy的依赖库--twisted：https://www.lfd.uci.edu/~gohlke/pythonlibs/（python版本和电脑操作系统位数一定要匹配）
###2.在下载存放的目录安装 -- pip install Twisted-18.9.0-cp37-cp37m-win_amd64.whl
###3.安装scrapy -- pip install scrapy
**注意：可以先创建一个spider项目，给此项目配置一个纯净的python虚拟环境，然后将scrapy安装在此虚拟环境中，在这个项目下创建你需要的各种爬虫scrapy框架工程**
##三： 创建scrapy项目  --
     scrapy startproject taobao -- （taobao是根据具体情况取的项目名）
     scrapy genspider goods www.taobao.com  -- (goods是spider文件--goods.py ; www.taobao.com是你要爬取的网站的一级域名)
##四： selector选择器（基于lxml构建，支持xpath,css,re）
###1.进入scrapy框架 shell脚本编程 --
 在终端中输入命令：scrapy shell 域名 -- 即获得了该网页的scrapy对象，并进入了scrapy脚步环境，可以进行scrapy编程，当然进入脚本文件只是为了方便演示，在开发中，方便测试一些代码的输出结果
###2.response.selector表示选择器对象 -- 
     response.selector.xpath('')   --  用xpath方法获取元素
     response.selector.css('')  -- 用css方法获取元素
     response.selector.re()  -- 用re方法获取数据（一般不这样直接在selector对象后用）

**注意：selector对象获取的数据后面要调用extract()或者extract_first()方法将对象转换成字符串**
###3.selector对象可以连续调用xpath或者css方法 -- 
     response.selector.css('#chapter').xpath('.//a')
     response.css('.author.box').xpath('./a[2]/text()').extract()
###4.extract()[0]与extract_first()区别 -- [0]可能会报错
     result.xpath('./a[1]/text()')[0] 
     result.xpath('./a[3]/text()').extract()
     result.xpath('./a[3]/text()').extract()[0]
     result.xpath('./a[3]/text()').extract_first()
##五： 框架的重要组成--
###1.spider -- 
	name : 爬取的名字
	allowed_domains:允许爬取的域名，不在此范围的连接不会被跟进爬取
	start_urls: 起始url列表，当我们没有重写start_requests()时，从这里面的url开始爬取
	custom_settings: 用来存放蜘蛛专属配置的字典，这里的设置会覆盖全局的设置
	crawl: 由from_crawl()方法设置的和蜘蛛对应的Crawler对象，Crawler对象包含了很
	多项⽬组件，利⽤它我们可以获取项⽬的配置信息，如调⽤crawler.settings.get()⽅法。
	settings：⽤来获取爬⾍全局设置的变量
	start_requests()：此⽅法⽤于⽣成初始请求，它返回⼀个可迭代对象。该⽅法默认是使⽤
	GET请求访问起始URL，如果起始URL需要使⽤POST请求来访问就必须重写这个⽅法，发送
	POST请求使⽤FormRequest⽅法
	parse()：当Response没有指定回调函数时，该⽅法就会被调⽤，它负责处理Response对
	象并返回结果，从中提取出需要的数据和后续的请求，该⽅法需要返回类型为Request或Item
	的可迭代对象（⽣成器当前也包含在其中，因此根据实际需要可以⽤return或yield来产⽣返回
	值）
	closed()：当蜘蛛关闭时，该⽅法会被调⽤，通常⽤来做⼀些释放资源的善后操作
###2.Downloader Middleware --
	process_request(request, spider) -- 调度器将request发给下载器之前，对request修改
	process_response(request,response,spider) -- 下载器生成的response发给spider之前，对response修改
	process_exception(request,execption,spider) -- 中间件异常调用该函数
###3.pipeline （数据管道）-- 
根据实际情况可以自定义多种类型的管道，如mysql，mongodb,redis等等，scrapy对图片下载到本地保存有一个专用的管道 Image Pipeline,该管道中有三个方法：

	get_media_requests(self,item, info)： 返回图片下载的连接（yield Request(url)）
	item_completed(self, results, item, info)：判断图片是否下载成功
	file_path(self, request, response=None, info):返回图片保存的文件名（return file_name）
###4.items -- 
给数据构造相应的字段，可以设置多个类（相当于mysql中的表，mongodb中的集合）

	class YouyaoqiItem(scrapy.Item):
	    # define the fields for your item here like:
	    collection_name = 'youyaoqi'
	    comic_id = scrapy.Field()
	    name = scrapy.Field()
	    cover = scrapy.Field()
	    line2 = scrapy.Field()

##六： 编写流程 -- 
###1. 修改配置文件settings.py -- 
    将机器人协议设置为False -- ROBOTSTXT_OBEY = False
    设置编码规则 -- FEED_EXPORT_ENCODING = 'utf-8'
###2. 创建Item -- 
    在items.py中创建数据的容器，即修改框架定义的数据类，如下：

	class YouyaoqiItem(scrapy.Item):
	    # define the fields for your item here like:
	    comic_id = scrapy.Field()  # 表示给文档添加key为comic_id
	    name = scrapy.Field()  # 表示给文档添加key为name
	    cover = scrapy.Field()  # 表示给文档添加key为cover
	    line2 = scrapy.Field()  # 表示给文档添加key为line2
        # 表示文档的结构为：{'comic_id':value, 'name':value, 'cover':value, 'line2':value}
###3. 创建请求对象 -- 

在spiders.py文件下的goods.py文件中重构start_requests()方法 -- POST和GET请求重构不一样

POST请求：

	class ComicSpider(scrapy.Spider):
	    name = 'comic'
	    allowed_domains = ['www.u17.com']
	    start_urls = ['http://www.u17.com/']
	
	    def start_requests(self):
	        headers = {
	            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
	            'Content-Type': 'application/x-www-form-urlencoded',
	            'Accept': 'application/json, text/javascript, */*; q=0.01',
	            'X-Requested-With': 'XMLHttpRequest',
	            'Origin': 'http://www.u17.com',
	            'Referer': 'http://www.u17.com/comic_list/th99_gr99_ca99_ss99_ob0_ac0_as0_wm0_co99_ct99_p1.html?order=2',
	        }
	        url = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'
	        postdata = {
	            'data[group_id]': 'no',
	            'data[theme_id]': 'no',
	            'data[is_vip]': 'no',
	            'data[accredit]': 'no',
	            'data[color]': 'no',
	            'data[comic_type]': 'no',
	            'data[series_status]': 'no',
	            'data[order]': '2',
	            'data[page_num]': '1',
	            'data[read_mode]': 'no'
	        }
	        for page in range(416):
	            postdata["data[page_num]"] = str(page+1)
	            yield scrapy.FormRequest(
	                url=url,
	                headers=headers,
	                method='POST',
	                formdata=postdata,
	                callback=self.parse,)  # 调用对应的解析方法，可以自定义多个解析方法
	
	    def parse(self, response):
	        result = json.loads(response.text)
	        result_list = result['comic_list']
	        for i in result_list:
	            item = YouyaoqiItem()
	            item['comic_id'] = i['comic_id']
	            item['name'] = i['name']
	            item['cover'] = i['cover']
	            item['line2'] = i['line2']
	            yield item    
GET请求：

	class SportSpider(scrapy.Spider):
	    name = 'sport'
	    allowed_domains = ['bbs.hupu.com']
	    start_urls = ['http://bbs.hupu.com/gear']
	
	    def start_requests(self):
	        """构造请求"""
	        headers = {
	            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
	            'Accept': 'application/json, text/plain, */*',
	            'Accept-Encoding': 'gzip, deflate, sdch',
	            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
	            'Connection': 'keep-alive',
	            'X-Requested-With': 'XMLHttpRequest',
	            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	        }
	        for page in range(100):
	            yield scrapy.Request(
	                url=f'http://bbs.hupu.com/gear-{page+1}',
	                headers=headers,
	                method='GET',
	                callback=self.parse,)  # 调用对应的解析方法，可以自定义多个解析方法
	
	    def parse(self, response):
	        """解析响应"""
	        li_list = response.selector.xpath('//ul[@class="for-list"]//li')
	        for li in li_list:
	            item = HupuItem()
	            item['author'] = li.xpath('./div[2]/a[1]/text()').extract_first()
	            item['subject'] = li.css('.titlelink.box a::text').extract()
	            item['time'] = li.xpath('./div[2]/a[2]/text()').extract_first()
	            yield item

###4. 解析Response -- 
    在spiders.py文件下的goods.py文件中重构pare()方法 （步骤三中代码已有该函数）
###5. 创建管道 -- 
    在pipelines.py文件中创建管道类（自由选择mysql/mongodb/redis等等，图片数据的管道类写法较固定，不能任意更改），创建过后，需要在settings.py中配置管道
settings.py中配置：

        # 不需要用的管道注释掉
		ITEM_PIPELINES = {
		   # 'youyaoqi.pipelines.YouyaoqiMysqlPipeline': 300,
		   # 'youyaoqi.pipelines.YouyaoqiMongoPipeline': 320,
		   'youyaoqi.pipelines.YouyaoqiImgPipeline': 340,
		}
		# 图片管道，图片数据的存放地址（爬取前需要创建，与scrapy.cfg平级）
		IMAGES_STORE = './imgs'
		
		# mysql settings
		MYSQL_HOST = '127.0.0.1'
		MYSQL_PORT = 3306
		MYSQL_USERNAME = 'root'
		MYSQL_PASSWORD = '123456'
		MYSQL_DATABASE = 'youyaoqi'
		
		# MONGO settings
		MONGO_URI = 'mongodb://127.0.0.1:27017'
		MONGO_DB = 'youyaoqi'

pipelines.py文件中构造管道：    

	class YouyaoqiImgPipeline(ImagesPipeline):
	    """构造一个图片管道类"""
	    def get_media_requests(self, item, info):
	        """指明图片下载链接，包装成request对象"""
	        yield Request(item['cover'])
	
	    def file_path(self, request, response=None, info=None):
	        """生成下载下来的图片的文件名"""
	        url = request.url
	        file_name = url.split('/')[-1]
	        return file_name
	
	    def item_completed(self, results, item, info):
	        """判断图片是否下载成功，没有下载成功，抛出异常"""
	        image_paths = [x['path'] for ok, x in results if ok]
	        if not image_paths:
	            raise DropItem('Image Downloaded Failed')
	        return item

	class YouyaoqiMongoPipeline(object):
	    """构造一个mongodb管道类"""
	    def __init__(self, uri, database):
	        self.uri = uri
	        self.database = database
	
	    @classmethod
	    def from_crawler(cls, crawler):
	        return cls(
	            uri=crawler.settings.get('MONGO_URI'),
	            database=crawler.settings.get('MONGO_DB'),
	            )
	
	    def open_spider(self, spider):
	        self.client = pymongo.MongoClient(self.uri)
	        self.db = self.client[self.database]
	
	    def close_spider(self):
	        self.client.close()
	
	    def process_item(self, item, spider):
	        self.db['comic'].insert(dict(item))
	        return item
	
	class YouyaoqiMysqlPipeline(object):
	    """构造一个mysql管道类"""
	    def __init__(self, host, port, username, password, database):
	        self.host = host
	        self.port = port
	        self.username = username
	        self.password = password
	        self.database = database
	
	    @classmethod
	    def from_crawler(cls, crawler):
	        return cls(
	            host=crawler.settings.get('MYSQL_HOST'),
	            port=crawler.settings.get('MYSQL_PORT'),
	            database=crawler.settings.get('MYSQL_DATABASE'),
	            username=crawler.settings.get('MYSQL_USERNAME'),
	            password=crawler.settings.get('MYSQL_PASSWORD'),
	            )
	
	    def open_spider(self, spider):
	        self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8',
	                                  port=self.port)
	        self.cursor = self.db.cursor()
	
	    def close_spider(self):
	        self.db.close()
	
	    def process_item(self, item, spider):
	        sql = 'insert into comic (comic_id, name, cover, line2) values (%s, %s, %s, %s)'
	        self.cursor.execute(sql, (item['comic_id'], item['name'], item['cover'], item['line2']))
	        self.db.commit()
	        return item
##五： 运行scrapy框架 -- 
	scrapy crawl goods (goods为spiders.py文件下的爬虫文件goods.py,表示运行goods这个爬虫)
	scrapy crawl goods -o goods.json --
	   (数据输出到goods.json文件中，与scrapy.cfg文件同级，当然如果有配置管道，数据也会通过管道存入数据库，文件的格式可以为：csv, xml, pickle, marshal，json等)