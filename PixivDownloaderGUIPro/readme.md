# PixivDownloader GUI V.Test

基于Python tkinter的Pixiv下载器

作者: KoiSato

GitHub: www.github.com/SatoKoi

日期: 2018/3/2

图源: www.pixiv.net

Python版本: 3.6

p站登不进的请将下面一段代码添加到你的hosts里后面

210.129.120.41 www.pixiv.net
210.140.131.144 source.pixiv.net
210.129.120.41 accounts.pixiv.net
210.140.131.147	imgaz.pixiv.net
210.140.131.145	comic.pixiv.net
210.140.131.145 novel.pixiv.net
210.129.120.41 factory pixiv.net
210.129.120.44 oauth.secure.pixiv.net
203.210.8.44 en-dic.pixiv.net
210.129.120.40 sensei.pixiv.net
210.129.120.40 recruit.pixiv.net

这是你的hosts文件地址 -> C:\Windows\System32\drivers\etc\hosts

功能:

1、单图下载, 直接给出作品id即可。
   例: https://www.pixiv.net/member_illust.php?mode=medium&illust_id=67507815
   id 为后面几位数字

2、下载画师作品或用户收藏, 给出用户id即可。
   例: https://www.pixiv.net/member.php?id=867590
   id 同上

3、下载p站排行榜图片, 选择日期和各榜下载。

4、根据关键字TAG下载。

5、可存储默认设置

6、可选择下载漫画和r18图片 (有的漫画没法过滤)

7、ps:测试版, 功能没多少(懒)
