# -*- coding:utf-8 -*-
"""初始参数设置
"""

# 请求头设置
headers = {
            'referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
# api地址
api_url = 'https://api.imjad.cn/pixiv/v1/?type=%s'
# 作品详情
illust = 'illust'
# 用户作品详情
member_illust = 'member_illust'
# 用户收藏
favorite = 'favorite'
# 排行榜
rank = 'rank'
# 排行榜参数, mode类型, page指定返回页数, per_page指定每页数量
mode_year = 'yearly'
mode_month = 'monthly'
mode_week = 'weekly'
mode_day = 'daily'
# r_18选择
r_18 = True

