# 네이버 지식인 크롤러

본 프로젝트는 NLP 파인튜닝 데이터셋을 구축하기 위해서 제작되었습니다. 

네이버의 IP 차단을 피하기 위해서 Tor-Proxy를 사용하였으며, 우회 접속을 통해서 데이터셋을 구축할 수 있었습니다. 

### Installation

```bash
pip install -r requirements.txt
```

Install the dependencies.

```bash
docker-compose up -d
```

Starting the Tor-Proxy for preventing ip ban.

### Start!!

```bash
scrapy crawl kin
```

### Caution

본 프로젝트의 코드를 활용한 모든 일의 책임은 당신에게 있습니다. 