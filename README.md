# Tianya_Spider

**Prepare**
```
pip3 install scrapy scrapy-inline-requests
```

**run**
```
scrapy crawl tianya -o tianya.json -s LOG_FILE=all.log
```

**Improvement**
1. Try scrapy+redis to boost speed <br>
2. Get second-level comments