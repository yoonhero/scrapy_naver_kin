#!/usr/local/bin/zsh

echo "building start!"

docker build . --tag naver
docker tag naver:latest ghcr.io/yoonhero/naver-kin-crawl-crawler:latest
docker push ghcr.io/yoonhero/naver-kin-crawl-crawler:latest