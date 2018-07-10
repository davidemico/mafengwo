
import json

from scrapy.spider import Spider, Request
from scrapy.selector import Selector

from mfwspider.items import MfwspiderItem


class Mfwspider(Spider):

    name = 'gonglve'

    domains_url = 'https://www.mafengwo.cn'

    start_url = 'http://www.mafengwo.cn/mdd/citylist/21536.html'

    cities_url = 'http://www.mafengwo.cn/mdd/citylist/21536.html?mddid=21536&page={page}'


    def start_requests(self):

        yield Request(self.start_url,callback=self.parse_city_info)


    # 解析城市区域
    def parse(self,response):

        ct = Selector(response)

        # 各城市在页面所在区域
        city_area = ct.xpath('//*[@id="citylistlist"]')
        # 各城市信息
        city_info = city_area.xpath('./li/div/a')


        for city in city_info:
            # 各城市链接
            city_href = city.xpath('./@href').extract()[0]
            # 城市名
            city_name = city.xpath('./div/text()').extract()
            city_name = self.deal_info(city_name)

            yield Request(self.domains_url + city_href,
                      callback=self.parse_city,
                      meta={'name': city_name, 'href': city_href})

    # 处理city_name
    def deal_info(self,city_name):

        return [i.replace('\n','').strip() for i in city_name][0]


    # 遍历所有分页
    def parse_city_info(self,response):

        ct = Selector(response)

        # 获取总页数
        total_pages = ct.xpath('//*[@id="citylistpagination"]/div/a[7]/@data-page').extract()[0]

        for page in range(1,int(total_pages)+1):
            yield Request(self.cities_url.format(page=page),callback=self.parse)


    def gong_lve(self,response):

        ct = Selector(response)
        item = MfwspiderItem()

        # 攻略id
        item['id'] = response.meta.get('href').split('/')[-1].split('.')[0]
        # 攻略标题
        item['title'] = response.meta.get('name')
        # 城市概览
        item['description'] = ct.xpath('//*[@id="wiki_part_1"]/p/text()').extract()
        # 首页图片
        try:
            item['imageUrl'] = ct.xpath('//*[@id="wiki_part_1"]/div[2]/a/img/@src').extract()[0]
        except:
            pass
        # 最佳旅行时间
        item['travelTime'] = ct.xpath('//*[@id="wiki_part_2"]/p/text()').extract()
        # 消费水平
        item['price'] = ct.xpath('//*[@id="wiki_part_3"]/p/text()').extract()
        # 穿衣指南
        item['tips'] = ct.xpath('//*[@id="wiki_part_4"]/p/text()').extract()

        yield item


    def parse_city(self,response):

        ct = Selector(response)


        gonglve_link = ct.xpath('//*[@class="navbar-btn"]/@href').extract()[0]
        city_name = response.meta.get('name')

        yield Request(self.domains_url + gonglve_link,callback=self.gong_lve,
                      meta={'name':city_name,'href':gonglve_link})















