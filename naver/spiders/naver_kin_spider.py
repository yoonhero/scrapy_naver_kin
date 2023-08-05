import scrapy
import random

class NaverKinSpider(scrapy.Spider):
    name = "kin"

    def start_requests(self):
        base_url = "https://search.naver.com/search.naver?where=kin&sm=tab_jum&ie=utf8&query={key_word}&kin_display=10&kin_start={num}&answer=2"
        keywords = ["과학", "컴퓨터", "생활", "예술", "건강", "여행", "인공지능", "우주", "역사", "글로벌", "음악", "미술", "언어", "철학", "기술", "자동차", "딥러닝", "문화", "세계", "상담", "이야기"]

        for _ in range(1000):
            keyword = random.sample(keywords, 1)[0]
            num = random.randint(0, 100)
            url = base_url.format(key_word=keyword, num=num*10)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath('//*[@id="main_pack"]/section/div/ul/li'):
            atag = item.css("div.question_group a")[0]
            yield response.follow(atag, self.parse_doc)
                        
    def parse_doc(self, response):
        docId = response.request.url.split("docId=")[-1].split("&")[0]

        filename = './raw/%s.txt' % docId
        with open(filename, 'wb') as f:
            f.write(response.body)