# BiqugeSpider

����scrapy �� mysql��С˵��վȫվ����

�����д�����Ӧ�����ݿ��

CREATE TABLE `��Ȥ��` (
  `name` varchar(50) NOT NULL,
  `author` varchar(50) NOT NULL,
  `category` varchar(30) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `id` varchar(200) NOT NULL DEFAULT '''',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `��Ȥ���½�����` (
  `book_name` varchar(50) NOT NULL,
  `book_id` varchar(200) NOT NULL,
  `chapter_name` varchar(50) NOT NULL,
  `chapter_id` varchar(200) NOT NULL,
  `chapter_url` varchar(100) NOT NULL,
  `chapter_content` text,
  KEY `chapter_id` (`chapter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

����debugger.py����