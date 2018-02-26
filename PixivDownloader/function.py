# -*- coding:utf-8 -*-
import os
import sys
import re
import time
from atexit import register
from collections import Counter
import requests
from settings import *
import manager


def mk_dir(dir_name):
    """创建文件夹"""
    dir_path = os.path.join(sys.path[0], dir_name)
    if not os.path.exists(dir_path):
        wrap_it('正在创建文件夹 {}'.format(dir_path))
        os.mkdir(dir_path)
    return dir_path


def wrap_it(str):
    """获取当前时间"""
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('[Time: {}] >>>>>> {}'.format(current_time, str))


def running_time(function):
    """获取爬虫运行时间, 此函数作为装饰器包装爬虫函数"""
    def work(*args):
        """对传入函数进行包装, *arg -> args为元组参数, *args对元组拆包
        此处*args表示爬虫函数的多个参数"""
        start_time = time.time()
        function(*args)
        stop_time = time.time()

        def time_decorate(start, stop):
            """时间修饰"""
            temp = stop - start
            minute = temp // 60
            sec = temp - minute * 60
            return minute, sec
        wrap_it('Spider运行时间: {0[0]:.0f} 分 {0[1]:.0f} 秒\n'.format(time_decorate(start_time, stop_time)))
    return work


def _quit(my_quit):
    """退出函数"""
    if my_quit == 'quit' or my_quit == '\q':
        sys.exit(0)


def get_strip(pattern, rep, string):
    """去符函数"""
    return re.sub(r'{}'.format(pattern), r'{}'.format(rep), string)


def get_split(pattern, string, max_split=0):
    """分割函数"""
    return re.split(r'{}'.format(pattern), string, maxsplit=max_split)


def has_number(input_string):
    """检查字符串是否含有数字"""
    return any(char.isdigit() for char in input_string)


def is_word(input_string):
    """检查字符串是否全为字母"""
    return all(char.isalpha() for char in input_string)


def sel_quit(select):
    """选择项退出调用函数"""
    the_quit = get_strip('(\s+)', '', select)
    _quit(the_quit)


@register
def _exit():
    wrap_it('程序已终止'.format())
    time.sleep(3)


def mode_sel():
    """选择模式下载"""
    while True:
        sel = input('请选择下载方式:\n  1、输入作品id单个下载\n  2、输入用户id多个下载\n  3、下载排行榜\n  4、搜索关键字进行下载\n>>>>')
        sel_quit(sel)
        try:
            mode = int(sel)
            if mode == 1 or mode == 2 or mode == 3 or mode == 4:
                return mode
            else:
                print('请输入正确的数字')
        except ValueError:
            print('请输入正确的数字')
            continue


def r_18_confirm():
    """r_18选择器"""
    global r_18
    sel = input('请确认是否下载r-18的图片, 若不下载, 请输入n (默认下载)\n>>>>')
    sel_quit(sel)
    if sel == 'n' or sel == 'N':
        r_18 = False


def page_sel(per_page, page):
    """页数选择"""
    while True:
        sel = input('当前默认总页数为{}, 单页作品数为{}, 输入y可以更改设置 (最好保持原设置, 页数*单页作品数 过大会get不到资源)\n>>>>'.format(page, per_page))
        if sel == 'y' or sel == 'Y':
            break
        else:
            return per_page, page
    while True:
        try:
            per_page = int(input('请输入单页作品数\n>>>>'))
        except ValueError:
            print('请输入正确的数字')
        while True:
            try:
                page = int(input('请输入页数\n>>>>'))
                return per_page, page
            except ValueError:
                print('请输入正确的数字')


def manga_confirm():
    while True:
        sel = input('请确认是否下载漫画, 输入y则选择下载漫画 (默认不下载)\n>>>>')
        if sel == 'y' or sel == 'Y':
            return True
        else:
            return False


def atlas_count_sel():
    while True:
        try:
            count = input('请输入单个图集作品下载多少图片 (默认为20)\n>>>>')
            if count == '':
                return 20
            return int(count)
        except ValueError:
            print('请输入正确的数字')


def get_img_name(img_url):
    """获取图片名字"""
    index = img_url.rindex('/')
    return img_url[index + 1:]


def get_img_status(json_str, manga_block=False, single_flag=False, atlas_count=20, unwanted_tags=None):
    """获取图片状态"""
    imgs_status = []
    page_count = 0
    now = lambda: time.time()
    atlas_count = atlas_count if not single_flag else 100
    try:
        response_list = json_str['response']
    except KeyError:
        wrap_it('获取资源失败! 请核实信息是否正确输入!')
        return None

    def get_meta_url(_id, atlas_count):
        """获取meta数据"""
        img_url = []
        count = 0
        response = requests.get((api_url + '&id=%d') % (illust, int(_id))).json()['response'][0]
        metadata = response['metadata']
        pages = metadata['pages']
        for page in pages:
            count += 1
            if count > atlas_count:
                break
            img_url.append(page['image_urls']['large'])
        return img_url

    def get_work(response):
        """获取用户收藏"""
        try:
            return response['works']
        except KeyError:
            return False

    def get_page_count(start, page_count):
        """当前图片已获取数量"""
        sep = now() - start
        if sep >= 2:
            sep -= 2
            wrap_it('当前已获取{} 张图片'.format(page_count))

    def tags_confirm(iTags, targetTags):
        """检查图片是否含有剔除标签"""
        target_flag = False
        for target in targetTags:
            try:
                iTags.index(target)
                target_flag = True
            except ValueError:
                continue
        return target_flag

    start = now()
    try:
        works = get_work(response_list[0])
    except IndexError:
        wrap_it('没有获取到图片资源, 请确认该用户是否有图片资源!!!')
        return None
    if works:
        response_list = works
        wrap_it('图片资源正在获取, 请稍等...')
    for response in response_list:
        status = {}
        try:
            _id = response['id']
            page_count += response['page_count']
        except KeyError:
            response = response['work']
            _id = response['id']
            page_count += response['page_count']
        # 漫画开关通道
        if not manga_block:
            img_type = response['type']
            if img_type == 'manga':
                continue
        get_page_count(start, page_count)
        # 图集或漫画作品
        if response['page_count'] > 1:
            try:
                img_url = get_meta_url(_id, atlas_count)
            except KeyError as e:
                img_url = response['image_urls']['large']
        else:
            img_url = response['image_urls']['large']
        try:
            status['score'] = response['stats']['score']
        except TypeError:
            status['score'] = None
        status['img_url'] = img_url
        iTags = response['tags']
        if unwanted_tags:
            if(tags_confirm(iTags, unwanted_tags)):
                continue
        status['title'] = response['title']
        status['age_limit'] = response['age_limit']
        status['id'] = _id
        imgs_status.append(status)
    wrap_it('图片资源已获取, 当前资源共{}张图片'.format(page_count))
    return imgs_status


def init_other_settings():
    manga = "不获取"
    r_18_str = '获取'
    manga_block = manga_confirm()
    if manga_block:
        manga = "获取"
    atlas_count = atlas_count_sel()
    r_18_confirm()
    if not r_18:
        r_18_str = '不获取'
    return manga, r_18_str, atlas_count, manga_block


def single_downloader(headers):
    """单张图片下载"""
    while True:
        illust_id = input('请输入作品的id\n>>>>')
        try:
            illust_id = int(illust_id)
            correct_url = (api_url + '&id=%d') % (illust, illust_id)
            json_str = requests.get(correct_url).json()
            break
        except ValueError:
            print('请输入正确的id')
            continue

    @running_time
    def img_download(headers):
        """图片下载"""
        img_status = get_img_status(json_str, single_flag=True)[0]
        img_url = img_status['img_url']
        dir_path = mk_dir(u'p站单图下载')
        if not isinstance(img_url, list):
            file_path = '\\'.join([dir_path, get_img_name(img_url)])
            with open(file_path, 'wb') as f_obj:
                resp = requests.get(img_url, headers=headers)
                f_obj.write(resp.content)
        else:
            _id = img_status['id']
            dir_name = u'p站单图下载/' + u'%s' % _id
            dir_path = mk_dir(dir_name)
            for url in img_url:
                img_name = get_img_name(url)
                file_path = '/'.join([dir_path, img_name])
                if os.path.exists(file_path):
                    wrap_it('{} 图片已存在'.format(img_name[:-4]))
                else:
                    with open(file_path, 'wb') as f_obj:
                        resp = requests.get(url, headers=headers)
                        f_obj.write(resp.content)
        wrap_it('{} 图片下载结束'.format(illust_id))
    img_download(headers)


def multi_init():
    """多图下载初始化"""
    while True:
        try:
            _id = int(input('请输入用户id:\n>>>>'))
            break
        except ValueError:
            print('请确认输入数字')
    while True:
        sel = input('请选择下载用户作品或用户收藏:\n  1、选择用户作品下载\n  2、选择用户收藏进行下载\n>>>>')
        sel_quit(sel)
        try:
            mode = int(sel)
            if mode == 1 or mode == 2:
                return _id, mode
            else:
                print('请输入正确的数字')
        except ValueError:
            print('请输入数字进行下载')


def multi_downloader(per_page, page):
    """多图下载器"""
    _id, sel_mode = multi_init()
    per_page, page = page_sel(per_page, page)
    manga, r_18_str, atlas_count, manga_block = init_other_settings()
    _type = member_illust
    threading_num = 15
    folder_name = str(_id) + u'_画师作品'
    if sel_mode == 2:
        folder_name = str(_id) + u'_用户收藏'
        _type = favorite
    wrap_it('总页数: {}, 单页作品数: {}, 类型: {}, 漫画: {}, r18: {}, 单个图集最大图片数量: {}'
            .format(page, per_page, folder_name[-4:], manga, r_18_str, atlas_count))
    wrap_it('当前正在获取{}资源, 请稍等...'.format(folder_name[-4:]))
    correct_url = (api_url + '&id=%d&per_page=%d&page=%d') % (_type, _id, per_page, page)
    start_to_work(correct_url, threading_num, folder_name, manga_block, atlas_count)


@running_time
def start_to_work(url, threading_num, folder_name, manga_block, atlas_count, tags=None):
    """爬虫管理下载机制启动"""
    global r_18
    json_str = requests.get(url, headers=headers).json()
    all_illusts = get_img_status(json_str, atlas_count=atlas_count, unwanted_tags=tags)
    if all_illusts is None:
        return
    checker = manager.Checker(all_illusts, folder_name, r_18)
    checker.check()
    downloader = manager.Downloader(checker.img_queue, threading_num, folder_name)
    downloader.work()


def date_confirm(mode, date):
    """日期确认"""
    year = int(date[:4])
    month_day = date[-4:]
    if year == int(month_day):
        year = int(time.localtime()[0])
    month = int(date[-4:-2])
    day = int(date[-2:])

    def ren_day_get(year):
        if (year % 4 == 0 or year % 400 == 0) and year % 100 != 0:
            return 29
        return 28

    if 1 <= month <= 12 and 1 <= day <= 31:
        if mode == 2:
            date = str(year) + date[-4:-2] + '31'
        if month == 2 and day > ren_day_get(year):
            return False
        elif month == 2 and day < ren_day_get(year) and mode == 2:
            date = str(year) + date[-4:-2] + str(ren_day_get(year))
        if (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
            return False
        elif (month == 4 or month == 6 or month == 9 or month == 11) and day < 30 and mode == 2:
            date = str(year) + date[-4:-2] + '31'
        if mode == 1:
            if month > 6:
                date = str(year) + '1231'
            else:
                date = str(year) + '0630'
        return date
    else:
        return False


def rank_init():
    """排行榜下载初始化"""
    while True:
        sel = input('请选择排行榜下载类型:\n  1、年榜\t2、月榜\n  3、周榜\t4、日榜\n>>>>')
        sel_quit(sel)
        try:
            mode = int(sel)
            if mode == 1 or mode == 2 or mode == 3 or mode == 4:
                break
            else:
                print('请输入正确的数字')
        except ValueError:
            print('请输入数字进行下载')

    while True:
        try:
            date = get_strip('[\D]+', '', input('请输入日期进行下载: (格式为 yyyymmdd | mmdd, 后一种默认为当前年, ~且程序只保留输入数字)\n注意: 获取年榜数据'
                                                '数据时, 将分成6月与12月; 获取月榜数据时, 默认为当前月最后一日\n>>>>'))
            if len(date) == 4:
                date = date_confirm(mode, date)
                if date:
                    date = '-'.join(['2018', date[:2], date[-2:]])
                    return mode, date
            elif len(date) == 8:
                date = date_confirm(mode, date)
                if date:
                    date = '-'.join([date[:4], date[4:6], date[-2:]])
                    return mode, date
            print('日期输入有误, 请输入正确的日期')
        except Exception as e:
            print(e)


def rank_downloader(per_page, page, block):
    """排行榜下载器"""
    sel_mode, date = rank_init()
    _type = rank
    _mode = mode_year
    threading_num = 15
    folder_name = date[:4] + u'年' + date[5:7] + u'月年榜'
    if sel_mode == 2:
        if not block:
            per_page = 250
        _mode = mode_month
        folder_name = date[:4] + u'年' + date[5:7] + u'月月榜'
    elif sel_mode == 3:
        if not block:
            per_page = 50
        _mode = mode_week
        folder_name = date[:4] + u'年' + date[5:7] + u'月' + date[-2:] + u'日周榜'
    elif sel_mode == 4:
        if not block:
            per_page = 20
        _mode = mode_day
        folder_name = date[:4] + u'年' + date[5:7] + u'月' + date[-2:] + u'日日榜'
    per_page, page = page_sel(per_page, page)
    manga, r_18_str, atlas_count, manga_block = init_other_settings()
    wrap_it('总页数: {}, 单页作品数: {}, 类型: {}, 漫画: {}, r18: {}, 日期: {}, 单个图集最大图片数量: {}'
            .format(page, per_page, folder_name[-2:], manga, r_18_str, date, atlas_count))
    correct_url = (api_url + '&mode=%s&per_page=%d&page=%d&date=%s') % (_type, _mode, per_page, page, date)
    start_to_work(correct_url, threading_num, folder_name, manga_block, atlas_count)


def set_search_key():
    """关键字设置"""
    def get_key(key_list):
        """获取默认设置或添加自定义设置"""
        real_key = set()
        key_set_dict = {
            1: '10000users', 2: '5000users', 3: '3000users', 4: '1000users', 5: '500users',
            6: '100users', 7: 'VOCALOID', 8: '東方', 9: '艦これ', 10: 'Fate',
            11: 'FGO', 12: 'アズールレーン', 13: '初音', 14: '少女', 15: '女の子',
            16: '背景', 17: '百合', 18: '风景',
            19: 'ロリ', 20: 'R-18', 21: '尻神様'
        }
        for key in key_list:
            try:
                key = int(key)
                value = key_set_dict.get(key, str(key))
                real_key.add(value)
            except ValueError:
                if key is '':
                    pass
                else:
                    real_key.add(key)
        new_list = []
        for key in real_key:
            new_list.append(key)
        return new_list[-4:]

    def remove_repeat(key_list):
        """移除重复的tag"""
        new_list = []
        counter = Counter(key_list)
        for key in counter.keys():
            new_list.append(key)
        return new_list[-4:]
    primary_input = '请输入当前想要获取的关键字, 直接回车表示将设置默认关键字[东方 10000users] (输入以下数字获取设置的默认关键字, 输入其他可自定义你想设置的关键字)\n'\
                    '关键字最多设置四个, 格式为 (每个关键字用逗号或空格隔开)\n'
    primary_tags = '----------以下是用户收藏数关键字-----------\n  '\
                   '1、10000users  2、5000users\n  3、3000users   4、1000users\n  5、500users    6、100users\n'\
                   '---------以下是常见IP热门作品关键字---------\n  '\
                   '7、VOCALOID  8、東方  9、艦これ(舰C)  10、Fate\n  '\
                   '11、FGO  12、アズールレーン(碧蓝航线)  13、初音\n'\
                   '----------------其它关键字-----------------\n  '\
                   '14、少女  15、女の子  16、背景\n  '\
                   '17、百合  18、风景  19、ロリ(萝莉)\n'\
                   '---------------奇怪的关键字----------------\n  '\
                   '20、R-18  21、尻神様\n' \
                   '注意: 设置多个关键字时, 只会获取同时含有这几个关键字的图片, 而不会每个关键字独立下载\n' \
                   '每类关键字请小心选择, 比如10000users选了, 就不要继续选其他users关键字\n>>>>'
    cur_settings = primary_input + primary_tags
    key_list = []
    default_key_list = ['10000users', '東方']
    while True:
        search_key = input(cur_settings)
        if search_key == 'get' or search_key == '\G':
            cur_settings = primary_tags
            continue
        if search_key == '':
            key_list = key_list if len(key_list) >= 1 else default_key_list
            # 排序方式 (1、全为数字，排在最后 2、含有数字, 排在1后 3、全为字母, 排在2后 4、字母大写, 排在3后 5、其余按正常排序排在前面)
            key_list = sorted(key_list, key=lambda x: (x.isdigit(), has_number(x), is_word(x), x.isupper(), x))
            print('已设置关键字: {}'.format(', '.join(key_list)))
            return key_list
        try:
            key_list += get_key(get_split('[,\s]+', search_key))
            key_list = remove_repeat(key_list)
            print('当前已有关键字: {}'.format(', '.join(key_list)))
            cur_settings = '请确认是否继续设置关键字, 多于四种关键字则覆盖 (直接回车表示将确认设置, ' \
                           '输入数字获取默认关键字, 输入其他自定义设置关键字, 输入get或\G则获取初始设置)\n>>>>'
        except Exception as e:
            print(e)


def set_sort_method():
    """设置排序方法"""
    while True:
        try:
            period = input('请设置搜索默认排序周期 (默认为所有):\n  1、所有  2、一天之内\n  3、一周之内  4、一月之内\n>>>>')
            if period == '':
                period = 'all'
                break
            else:
                period = int(period)
                if period == 1:
                    period = 'all'
                    break
                elif period == 2:
                    period = 'day'
                    break
                elif period == 3:
                    period = 'week'
                    break
                elif period == 4:
                    period = 'month'
                    break
                else:
                    print('请输入正确的数字')
        except ValueError:
            print('请输入正确的数字')
    while True:
        try:
            order = input('请设置搜索后默认排序方式 (默认为倒序):\n  1、按日期倒序\n  2、按日期正序\n>>>>')
            if order == '':
                order = 'desc'
                return period, order
            else:
                order = int(order)
                if order == 1:
                    order = 'desc'
                    return period, order
                elif order == 2:
                    order = 'asc'
                    return period, order
                else:
                    print('请输入正确的数字')
        except ValueError:
            print('请输入正确的数字')


def tags_unwanted():
    """剔除不想要的标签"""
    while True:
        tag = input('以下标签将被剔除, 请输入你想保留的标签, 输入数字选择以下标签 (默认为全选)\n  1、BL  2、漫画  3、腐向け\n>>>>')
        tags = ['漫画', 'BL', '腐向け']
        if tag == '':
            return tags
        try:
            tag = int(tag)
            if tag == 1:
                tags.remove('BL')
            elif tag == 2:
                tags.remove('漫画')
            elif tag == 3:
                tags.remove('腐向け')
            else:
                print('请输入正确的数字')
        except ValueError:
            print('请输入正确的数字, 当前剔除标签 {}'.format(tags))


def search_tag_downloader(per_page, page):
    """搜索下载器"""
    threading_num = 15
    key_list = set_search_key()
    tags = tags_unwanted()
    period, order = set_sort_method()
    folder_name = key_word = ' '.join(key_list)
    per_page, page = page_sel(per_page, page)
    _type = 'search'
    _mode = 'tag'
    manga, r_18_str, atlas_count, manga_block = init_other_settings()
    wrap_it('总页数: {}, 单页作品数: {}, 关键字: {}, 剔除标签: {}, 漫画: {}, r18: {}, 单个图集最大图片数量: {}'
            .format(page, per_page, key_word, ' '.join(tags), manga, r_18_str, atlas_count))
    correct_url = (api_url + '&mode=%s&per_page=%d&page=%d&word=%s&period=%s&order=%s') %\
                  (_type, _mode, per_page, page, key_word, period, order)
    start_to_work(correct_url, threading_num, folder_name, manga_block, atlas_count, tags)
