# -*- coding: utf-8 -*-
import re
import scrapy
import sys
reload(sys)
from scrapy.http import Request
from  ArticleSpider.items import JobBoleArticleItem

try:
    import urlparse  # python2
except:
    from urllib import parse    # python3
sys.setdefaultencoding('utf-8') # 修改默认编码

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy进行具体字段的解析
        2. 获取下一页的url并交给scrapy进行下载, 下载完成后交给parse函数
        """
        # 解析列表页中的所有文章url并交给scrapy下载后进行解析
        post_node = response.css('#archive .floated-thumb .post-thumb a')
        for post_url in post_node:
            image_url = post_url.css("img::attr(src)").extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            # Request(url=urlparse.urljoin(response.url, post_url), callback=self.parse_detial)  如果href里url不带域名记得加域名,urlparse确保了href后的值有主域名
            print urlparse.urljoin(response.url, post_url)
            yield Request(url=urlparse.urljoin(response.url, post_url), meta={'front_image_url': image_url}, callback=self.parse_detial)
            # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detial) # python3

        # 提取下一页的url并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first('') # 拿到下一页的url
        if next_url:
            print urlparse.urljoin(response.url, next_url)
            yield Request(url=urlparse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detial(self, response):
        """
        提取文章的具体字段
        """
        article_item = JobBoleArticleItem()




        #-------------------------通过xpath选择器提取字段-------------------------
        # title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0] # 文章标题
        #                                                                  #extract_first('NoneArray') 防止数组为空抛出异常 ''为传入的默认值
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip()[:-1].strip() # 文章创建时间
        # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0] # 点赞数   contains() xpath内置函数,包含
        # # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0].split(' ')[1]
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_fav_nums = re.match(r'.*?(\d+).*', fav_nums)
        # if match_fav_nums:
        #     fav_nums = int(match_fav_nums.group(1)) # 收藏数
        # else:
        #     fav_nums = 0
        # # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].split(' ')[1]
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_comment_nums = re.match(r'.*?(\d+).*', comment_nums)
        # if match_comment_nums:
        #     comment_nums = int(match_comment_nums.group(1)) # 评论数
        # else:
        #     comment_nums = 0
        #
        # content = response.xpath("//div[@class='entry']").extract()[0] # 正文源码
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')] # 去掉列表中以'评论'结尾的元素
        # tags = ','.join(tag_list) # 文章类型

        #-------------------------通过css选择器提取字段-------------------------
        front_image_url = response.meta.get('front_image_url', '') # 对字典使用get方法,设置默认值为空,防止抛异常
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip() # py2如果不重置默认编码,这里replace会报错
        praise_nums = response.css("span[class~='vote-post-up'] h10::text").extract()[0]
        fav_nums = response.css("span[class~='bookmark-btn']::text").extract()[0]
        match_fav_nums = re.match(r'.*?(\d+).*', fav_nums)
        if match_fav_nums:
            fav_nums = int(match_fav_nums.group(1)) # 收藏数
        else:
            fav_nums = 0
        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_comment_nums = re.match(r'.*?(\d+).*', comment_nums)
        if match_comment_nums:
            comment_nums = int(match_comment_nums.group(1)) # 评论数
        else:
            comment_nums = 0
        content = response.css("div.entry").extract()[0]
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith(u'评论')]  # 去掉列表中以'评论'结尾的元素
        tags = ','.join(tag_list)

        article_item['title'] = title
        article_item['url'] = response.url
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content
        yield article_item




        print title
        print create_date
        print praise_nums
        print fav_nums
        print comment_nums
        print tags
        print front_image_url
        print content[:500].replace(u'\xa0', u' ')  # \xa0在gbk代表空格


        pass