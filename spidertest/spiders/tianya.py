from scrapy import Request
from scrapy.spiders import Spider
from spidertest.items import NewsItem, SecondItem
from inline_requests import inline_requests
import numpy as np
import re

class Tianya(Spider):
    name = 'tianya'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    start_urls = ['https://www.8btc.com/article/']
    handle_httpstatus_list = [404, 500] # allow spider to handle 404 status
    
    @inline_requests
    def parse(self, response):
        title_v = []
        auth_v = []
        url_prefix = 'https://www.8btc.com/article/'
        auth_prefix = 'https://www.8btc.com'
        num = 0
        while num <= 500000:
            print(num)
            url = url_prefix + str(num)
            page = yield Request(url,dont_filter = True)
            header = page.xpath('//div[@class="main__header"]')
            if header: # not 404
                news_item = NewsItem()

                headline = page.xpath('//div[@class="main__header"]/div[@class="header__main"]/div[@class="bbt-container"]/h1').xpath('string(.)').extract()
                
                if headline and headline[0].strip():
                    if headline in title_v: #prevent repettious reading
                        continue
                    else:
                        news_item['headline'] = headline[0].strip()
                        title_v.append(headline)
                else:
                    news_item['headline'] = ""

                author = page.xpath('//div[@class="main__header"]/div[@class="header__main"]/div[@class="bbt-container"]/div[@class="header__info"]/span[@class="header__info-item"]/a/@href').extract()[-1]
                news_item['author'] = author

                time = page.xpath('//div[@class="main__header"]/div[@class="header__main"]/div[@class="bbt-container"]/div[@class="header__info"]/span[@class="header__info-item"]/time/text()').extract()[-1]
                news_item['time'] = time

                passage = page.xpath('//div[@class="main__body main__body--normal"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-16"]/div[@class="bbt-html"]').xpath('string(.)').extract()
                if passage and passage[0].strip():
                    news_item['passage'] = passage[0].strip()
                else:
                    news_item['passage'] = ""
                #news_item['headline'] = headline
                
                #labels
                labels = page.xpath('//div[@class="main__body main__body--normal"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-16"]/div[@class="tag-module"]').xpath('string(.)').extract()
                if labels and labels[0].strip():
                    label_list = labels[0].strip().split('\n')[1:]
                    label_list = [label.strip() for label in label_list if label.strip()]
                    news_item['labels'] = label_list
                else:
                    news_item['labels'] = [] # no label
                
               
                #read_num
                read_num = page.xpath('//div[@class="main__header"]/div[@class="header__main"]/div[@class="bbt-container"]/div[@class="header__info"]/span[@class="header__info-item"][2]/text()').extract()[-1]
                #print(read_num)
                if read_num:
                    news_item['read_num'] = read_num
                else:
                    news_item['read_num'] = 0
                
                #comments
                comments = page.xpath('//div[@class="main__body main__body--normal"]//div[@class="share-module_left"]//a[@class="link-dark-minor share-module__item"]/text()').extract()
                #print(comments)
                if comments:
                    comment_num = comments[0].strip()[0]
                    news_item['comments'] = comment_num
                else:
                    news_item['comments'] = 0
                
                #likes
#                likes = page.xpath('//div[@class="main__body main__body--normal"]/div[@class="bbt-container"]/div[@class="bbt-col-xs-16"]/div[@class="share-module"]/div[@class="share-module__fix fixed"]/div[@class="bbt-container"]//button[@class="bbt-btn bbt-btn--primary share-module__item"]/text()').extract()
                likes = page.xpath('//button[@class="bbt-btn bbt-btn--primary share-module__item"]/text()').extract()               
                print(likes)
                if likes:
                    like_num = likes[0].strip()[-1]
                    news_item['likes'] = like_num
                else:
                    news_item['likes'] = 0
                
                
                
                #btc_price 文章发布时的btc价格
                btc_price = page.xpath('//div[@class="main__body main__body--normal"]//div[@class="copyright-module__header bbt-clearfix"]/span/span/text()').extract()
                if btc_price:
                    price = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",btc_price[0]) 
                    print(btc_price)
                    news_item['btc_price'] = price[1:]
                else:
                    news_item['btc_price'] =  np.nan
                
                
                #作者的相关信息
                news_item['author_views'] = 0
                news_item['author_followers'] = 0
                news_item['author_publishes'] = 0
                
                auth_url = auth_prefix + author
                auth_page = yield Request(auth_url,dont_filter = True)
                auth_header = auth_page.xpath('//div[@class="author-module"]')
                if auth_header:
                    auth_views = auth_page.xpath('//div[@class="author-overview bbt-clearfix"]/div[@class="author-overview__info"]/div[@class="author-overview__info-name"]/span[@class="author-overview__info-item"][1]/span/text()').extract()
                    #auth_likes = auth_page.xpath('//div[@class="author-overview bbt-clearfix"]/div[@class="author-overview__info"]/div[@class="author-overview__info-name"]/span[@class="author-overview__info-item"][2]/span/text()').extract()[0]
                    auth_follows = auth_page.xpath('//div[@class="author-overview bbt-clearfix"]/div[@class="author-overview__info"]/div[@class="author-overview__info-name"]/span[@class="author-overview__info-item"][3]/span/text()').extract()
                    auth_publishes = auth_page.xpath('//div[@class="author-module"]//ul[@class="bbt-tab__menu bbt-clearfix"]//li[@class="active"]/span/text()').extract()
                    print(auth_views,auth_follows,auth_publishes)
                    
                if auth_views:
                    news_item['author_views'] = auth_views[0].strip()
                if auth_follows:
                    news_item['author_followers'] = auth_follows[0].strip()
                if auth_publishes:
                    news_item['author_publishes'] = auth_publishes[0].strip()
                
                 
                
                
                    
                yield news_item
            num += 1





'''
        final_buttom = response.xpath('//div[@class="short-pages-2 clearfix"]/div/a/text()').extract()[-1]
        list_page = response
        while final_buttom == "下一页":
            url_list = list_page.xpath('//td[@class="td-title faceblue"]/a/@href').extract()
            print(url_list)
            for url in url_list:
                blog_url = 'http://bbs.tianya.cn' + url
                first_page = yield Request(blog_url)

                first_item = FirstItem()
                title = first_page.xpath('//span[@class="s_title"]/span/text()').extract()
                if title and title[0].strip():
                    first_item['title'] = title[0].strip()
                else:
                    first_item['title'] = ""
                print(first_item['title'])
                print(blog_url)
                passage = first_page.xpath('//div[@class="bbs-content clearfix"]').xpath('string(.)').extract()
                if passage and passage[0].strip():
                    first_item['passage'] = passage[0].strip()
                else:
                    first_item['passage'] = ""
                first_item['response'] = []

                next_page = first_page
                while True:
                    first_item['response'] += [sen.strip() for sen in
                                               next_page.xpath('//div[@class="bbs-content"]').xpath('string(.)').extract() if sen.strip()]
                    if not next_page.xpath('//a[@class="js-keyboard-next"]/@href').extract(): # no choice for next page
                        break
                    next_url = "http://bbs.tianya.cn" + next_page.xpath('//a[@class="js-keyboard-next"]/@href').extract()[0]
                    next_page = yield Request(next_url)

                yield first_item
            final_buttom = list_page.xpath('//div[@class="short-pages-2 clearfix"]/div/a/text()').extract()[-1]
            next_url = "http://bbs.tianya.cn" + list_page.xpath('//div[@class="short-pages-2 clearfix"]/div/a/@href').extract()[-1]
            print(next_url)
            list_page = yield Request(next_url) #next page
            '''