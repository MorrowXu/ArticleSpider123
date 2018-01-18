# -*- coding: utf-8 -*-
import re
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # 修改默认编码

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']

    def parse(self, response):
        title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0] # 文章标题
                                                                         #extract_first('NoneArray') 防止数组为空抛出异常 ''为传入的默认值
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip()[:-1].strip() # 文章创建时间
        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0] # 点赞数   contains() xpath内置函数,包含
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0].split(' ')[1]
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_fav_nums = re.match(r'.*?(\d+).*', fav_nums)
        if match_fav_nums:
            fav_nums = match_fav_nums.group(1) # 收藏数
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].split(' ')[1]
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_comment_nums = re.match(r'.*?(\d+).*', comment_nums)
        if match_comment_nums:
            comment_nums = match_comment_nums.group(1) # 评论数

        content = response.xpath("//div[@class='entry']").extract()[0] # 正文源码
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')] # 去掉列表中以'评论'结尾的元素
        tags = '-'.join(tag_list) # 文章类型

        #通过css选择器提取字段
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip() # py2如果不重置默认编码,这里replace会报错
        praise_nums = response.css("span[class~='vote-post-up'] h10::text").extract()[0]
        fav_nums = response.css("span[class~='bookmark-btn']::text").extract()[0]
        match_fav_nums = re.match(r'.*?(\d+).*', fav_nums)
        if match_fav_nums:
            fav_nums = match_fav_nums.group(1)
        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_comment_nums = re.match(r'.*?(\d+).*', comment_nums)
        if match_comment_nums:
            comment_nums = match_comment_nums.group(1)
        content = response.css("div.entry").extract()[0]
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')]  # 去掉列表中以'评论'结尾的元素
        tags = '-'.join(tag_list)



        print title
        print create_date
        print praise_nums
        print fav_nums
        print comment_nums
        print tags
        print content[:500].replace(u'\xa0', u' ')  # \xa0在gbk代表空格


        pass