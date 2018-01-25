# coding=utf-8
# MySQL设置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'scrapy'

# Request headers设置, 反防盗链
Connection = 'keep-alive'
Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
Headers = {
    'User-Agent': User_Agent,
    'Accept': Accept,
    'Connection': Connection,
}

# 根路径设置
Root_Url = 'http://www.mzitu.com/page/'
Root_Path = 'mypic'
