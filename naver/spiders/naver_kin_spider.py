import scrapy
import random
import glob
from pathlib import Path
import os
import hashlib
from shutil import which
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS=['-headless']

class NaverKinSpider(scrapy.Spider):
    name = "naver"
    KIN = "kin"
    BLOG = "blog"

    def __init__(self):
        super().__init__()
        base_mode = NaverKinSpider.KIN

        our_dir = Path("./raw")
        our_dir.mkdir(exist_ok=True)
        self.items = glob.glob(str(our_dir / "*"))

        self.count = 0
        self.max_surf_depth = 10

        try: 
            self.mode = os.getenv("CRAWL_MODE")
        except: self.mode = base_mode

    def start_requests(self):
        if self.mode == NaverKinSpider.KIN:
            base_url = "https://kin.naver.com/tag/tagDetail.naver?tag={tag}&listType=answer&page={pagination}"
            # base_url = "https://search.naver.com/search.naver?where=kin&sm=tab_jum&ie=utf8&query={key_word}&kin_display=10&kin_start={num}&answer=2"
            keywords = ["과학", "컴퓨터", "생활", "예술", "건강", "여행", "인공지능", "우주", "역사", "글로벌", "음악", "미술", "언어", "철학", "기술", "자동차", "딥러닝", "문화", "세계", "상담", "이야기", "요리", "기후", "날씨"]

            while self.count < 20:
                keyword = random.sample(keywords, 1)[0]
                page = random.randint(0, 150)
                url = base_url.format(tag=keyword, pagination=page)
                yield scrapy.Request(url=url, callback=self.parse2)

        elif self.mode == NaverKinSpider.BLOG:
            base_url = "https://section.blog.naver.com/Search/Post.naver?pageNo={pageNo}&rangeType=ALL&orderBy=sim&keyword=%EC%9D%BC%EC%83%81"
            max_index = 570

            for i in range(max_index):
                pageNo = i + 1               
                url = base_url.format(pageNo=pageNo)
                # yield scrapy.Request(url=url, callback=self.parse_blog_items)
                yield SeleniumRequest(url=url, callback=self.parse_blog_items, wait_time=10, wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.se-section'))) 

    def parse(self, response):
        for item in response.xpath('//*[@id="main_pack"]/section/div/ul/li'):
            atag = item.css("div.question_group a")[0]
            yield response.follow(atag, self.parse_doc)

    def parse2(self, response):
        for li in response.xpath('//*[@id="content"]/div/div[3]/div[3]/ul/li'):
            atag = li.css("a.cont")[0]
            yield response.follow(atag, self.parse_doc)

    def parse_blog_items(self, response):
        print(response.body)
        for li in response.selector.xpath('//*[@id="content"]/section/div[2]/div'):
            print(li, "asdfja;lsdkjfal;ksdjf;laksjdfl;akjsdl;fkj")
            target_url = 'https://blog.naver.com/PostView.naver?blogId={blogId}&logNo={logNo}&postListTopCurrentPage=1&from=postView&userTopListCount=30'
            href = li.css("a.desc_inner").xpath('href').extract()
            blogId = href.split("/")[-2]
            logNo = href.split("/")[-1]
            url = target_url.format(blogId=blogId, logNo=logNo)
            print(url, logNo)
            yield scrapy.Request(url=url, callback=self.parse_blog_items)

    def parse_doc(self, response):
        docId = response.request.url.split("docId=")[-1].split("&")[0]
        self.save(response=response, file=docId)

    def surf(self, response, depth=0):
        # file = "-".join(response.request.url.split("/")[-2:])
        # self.save(resopnse=response, file=file)
        for tr in response.xpath('//*[@id="listTopForm"]/table/tbody/tr'):
            # class="pcol2 _setTop _setTopListUrl"
            atag = tr.css("a.pcol2")
            yield response.follow(atag, self.parse_blog_doc)
    
    def hashing(self, t):
        return str(hashlib.sha256(t.encode()).hexdigest())

    def parse_blog_doc(self, response):
        file = self.hashing(response.request.url)
        self.save(resopnse=response, file=file)
        return 

    def save(self, response, file):
        filename = './raw/%s.txt' % file
        if filename in self.items:
            self.count += 1
            return 
    
        self.count = 0
        self.items.append(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)