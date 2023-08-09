import scrapy
import random
import glob
from pathlib import Path

class NaverKinSpider(scrapy.Spider):
    name = "kin"
    def __init__(self):
        super().__init__()

        our_dir = Path("./raw")
        our_dir.mkdir(exist_ok=True)
        self.items = glob.glob(str(our_dir / "*"))

        self.count = 0

    def start_requests(self):
        base_url = "https://kin.naver.com/tag/tagDetail.naver?tag={tag}&listType=answer&page={pagination}"
        # base_url = "https://search.naver.com/search.naver?where=kin&sm=tab_jum&ie=utf8&query={key_word}&kin_display=10&kin_start={num}&answer=2"
        keywords = ["과학", "컴퓨터", "생활", "예술", "건강", "여행", "인공지능", "우주", "역사", "글로벌", "음악", "미술", "언어", "철학", "기술", "자동차", "딥러닝", "문화", "세계", "상담", "이야기", "요리", "기후", "날씨"]

        while self.count < 20:
            keyword = random.sample(keywords, 1)[0]
            page = random.randint(0, 150)
            url = base_url.format(tag=keyword, pagination=page)
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse(self, response):
        for item in response.xpath('//*[@id="main_pack"]/section/div/ul/li'):
            atag = item.css("div.question_group a")[0]
            yield response.follow(atag, self.parse_doc)

    def parse2(self, response):
        for li in response.xpath('//*[@id="content"]/div/div[3]/div[3]/ul/li'):
            atag = li.css("a.cont")[0]
            yield response.follow(atag, self.parse_doc)

    def parse_doc(self, response):
        docId = response.request.url.split("docId=")[-1].split("&")[0]

        filename = './raw/%s.txt' % docId
        if filename in self.items:
            self.count += 1
            return 
    
        self.count = 0
        self.items.append(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)