# BiqugeSpider

基于scrapy 与 mysql的小说网站全站爬虫

需自行创建对应的数据库表

CREATE TABLE `笔趣阁` (
  `name` varchar(50) NOT NULL,
  `author` varchar(50) NOT NULL,
  `category` varchar(30) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `id` varchar(200) NOT NULL DEFAULT '''',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `笔趣阁章节内容` (
  `book_name` varchar(50) NOT NULL,
  `book_id` varchar(200) NOT NULL,
  `chapter_name` varchar(50) NOT NULL,
  `chapter_id` varchar(200) NOT NULL,
  `chapter_url` varchar(100) NOT NULL,
  `chapter_content` text,
  KEY `chapter_id` (`chapter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

运行debugger.py即可