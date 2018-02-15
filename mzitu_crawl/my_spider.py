# coding=utf-8
import requests
import re
import sys
import os
import threading
# import multiprocessing
# import Queue
from bs4 import BeautifulSoup as bs
from sql import UrlSql
from collections import OrderedDict     # 有序字典, 按照插入顺序排列
from settings import *
from atexit import register


def init_sel():
    """初始化选择操作"""
    while True:
        select = raw_input('请输入下载方式，为0时，选择范围下载，为1时，选择页面下载，默认为0:\n')
        if select or select == '':
            while True:
                try:
                    if select == '':
                        sel = 0
                        break
                    sel_quit(select)
                    sel = int(select[0])
                    if sel == 0 or sel == 1:
                        break
                    else:
                        select = raw_input('输入错误，请输入正确的数字>>>>\n')
                        continue
                except ValueError:
                    select = raw_input('输入错误，请输入正确的数字>>>>\n')
                    continue
            max_num = get_max_page()
            if sel == 0:
                ret = raw_input('请输入初始页和末尾页，默认初始页为1，末尾页为1，(格式如下:1, 2)>>>>\n')
                while True:
                    if ret == '':
                        return True, 1, 1
                    sel_quit(ret)
                    list = get_strip('([\s,]+)', ',', ret).split(',')
                    try:
                        if len(list) > 2:
                            ret = raw_input('请重新输入, (格式如下:1, 2)>>>>\n')
                            continue
                        else:
                            start_page, last_page = int(list[0]), int(list[-1])
                            if last_page > max_num or start_page < 1 or start_page > last_page:
                                ret = raw_input('起始页或初始页输入错误, 请确认最大页后输入>>>>\n')
                                continue
                            return True, int(start_page), int(last_page)
                    except ValueError:
                        ret = raw_input('初始页和末尾页只能为数字!!!>>>>\n')

            elif sel == 1:
                while True:
                    ret = get_strip('(\s+)', '', raw_input('请输入页码进行下载>>>>\n'))
                    sel_quit(ret)
                    try:
                        ret = int(ret)
                        if 1 <= ret <= max_num:
                            return False, ret, ret
                        else:
                            print '页码输入错误'
                            continue
                    except ValueError:
                        print '格式错误, 请重新输入'
        else:
            print '格式错误, 请重新输入'


def get_page_urls(page_sel, start_num, last_num):
    """获取首页页面链接地址"""
    page_urls = []
    if page_sel:
        for i in range(start_num, last_num+1):
            page_url = Root_Url + str(i)
            page_urls.append(page_url)
    else:
        page_url = Root_Url + str(start_num)
        page_urls.append(page_url)
    return page_urls


def get_img_urls(page_urls, start_page, headers, new_folder=None, folder_num=1):
    """获取每页图片地址"""
    img_urls = OrderedDict()
    for page_url in page_urls:
        if new_folder is None:
            page_path = os.path.join(sys.path[0], 'page' + str(start_page))
            start_page += 1
        else:
            page_path = os.path.join(sys.path[0], new_folder, str(folder_num))
        while True:
            if not os.path.exists(page_path):
                os.mkdir(page_path)
            count = len(os.listdir(page_path))
            if count > 24:
                folder_num += 1
                page_path = os.path.join(sys.path[0], new_folder, str(folder_num))
            else:
                break

        resp = requests.get(page_url, headers=headers)
        resp.encoding = 'utf-8'
        soup = bs(resp.text, 'html.parser')
        lis = soup.find('ul', id='pins').find_all('li')
        for li in lis:
            a_link = li.find_all('a')[1]
            folder_name = os.path.join(page_path, get_strip('([,.?:";*~|!^@]+)', '', a_link.get_text()))
            img_url = a_link['href']
            img_urls[folder_name] = img_url
    return img_urls


def generic_downloader(sql, img_urls, headers):
    """通常下载器"""
    print u'>>>>>>>>>>开始下载<<<<<<<<<<'
    for folder_name, img_url in img_urls.items():
        if not cache_check(folder_name, sql, img_url):
            try:
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
            except WindowsError:
                print u'创建{}文件夹失败, 将跳过当前图片下载'.format(folder_name)
                print u'当前URL:', img_url
                return
            try:
                max_img_num = get_img_max_page(img_url, headers)
                print u'该图片数', max_img_num
                print u'下载到', folder_name
                multi_threading_downloader(max_img_num, folder_name, img_url, headers)
                sql.insert_url_into_database(img_url)
            except Exception as e:
                print u'连接失败', e
        else:
            index = folder_name.rindex('\\')
            print u'总图集 {} 已下载或已存在'.format(folder_name[index+1:])


def multi_threading_downloader(max_img_num, folder_name, img_url, headers):
    """多线程下载器"""
    Threads = []
    lock = threading.Lock()
    try:
        for i in range(1, max_img_num+1):
            thread = threading.Thread(target=img_downloader, args=(i, folder_name, img_url, headers, lock))
            Threads.append(thread)
            thread.start()

        for thread in Threads:
            thread.join()
    except Exception as e:
        print e


def img_downloader(i, folder_name, img_url, headers, lock):
    """图片下载器"""
    with lock:
        try:
            resp = requests.get(img_url + '/' + str(i), headers=headers)
            soup = bs(resp.text, 'html.parser')
            img = soup.find('div', class_='main-image').find('img')['src']
            headers['Referer'] = str(img_url)
            with open('/'.join([folder_name, str(i) + '.jpg']), 'wb') as f_obj:
                res = requests.get(img, headers=headers)
                f_obj.write(res.content)
                print u'图片{}下载完毕'.format(i)
        except Exception as e:
            print e


# def multi_processing_downloader(sql, img_urls, headers):
#     """多进程下载器, 因windows环境及python环境原因报错"""
#     processings = []
#     queue = Queue.Queue()
#     num_cpus = multiprocessing.cpu_count()
#     print '最大进程数', num_cpus
#     for folder_name, img_url in img_urls.items():
#         queue.put((folder_name, img_url), block=True, timeout=30)
#     while True:
#         # try:
#         for i in range(num_cpus):
#             img_info = queue.get(False)
#             process = multiprocessing.Process(target=generic_downloader, args=(sql, img_info[0], img_info[1], headers))
#             processings.append(process)
#             process.start()

#              for i in range(num_cpus):
#                  processings[i].join()
#         except Exception as e:
#             print e
#             print '进程创建失败或已完成'
#             break


def get_img_max_page(img_url, headers):
    """获取该套图最大图片数"""
    resp = requests.get(img_url, headers=headers)
    resp.encoding = 'utf-8'
    soup = bs(resp.text, 'html.parser')
    max_img_num = soup.find('div', class_='pagenavi').find_all('a')[4].find('span').get_text()
    return int(max_img_num)


def get_max_page():
    """获取首页下的最大页数"""
    resp = requests.get(Root_Url + '/' + str(1))
    resp.encoding = 'utf-8'
    soup = bs(resp.text, 'html.parser')
    max_page = soup.find('div', class_='nav-links').find_all('a')[3]['href']
    max_num = re.search(r'/(\d+)/', max_page).group(1)
    print u'当前最大页数为', max_num
    return int(max_num)


def cache_check(folder_name, sql, img_url):
    """检测当前url是否下载过"""
    sql.get_url_from_database()
    try:
        if sql.query.index(img_url) and os.path.exists(folder_name):
            return True
        else:
            for i in range(1, 32):
                i = str(i)
                index = folder_name.rindex('\\')
                new_folder = folder_name[:9] + u'page{}'.format(i) + folder_name[index:]
                auto_folder = folder_name[:9] + u'Auto_add/{}'.format(i) + folder_name[index:]
                if os.path.exists(new_folder) or os.path.exists(auto_folder):
                    return True
            return False
    except ValueError:
        return False


def _quit(my_quit):
    """退出函数"""
    if my_quit == 'quit' or my_quit == '\q':
        sys.exit(0)


def get_strip(pattern, rep, string):
    """去符函数"""
    return re.sub(r'{}'.format(pattern), r'{}'.format(rep), string)


def sel_quit(select):
    """选择项退出调用函数"""
    the_quit = get_strip('(\s+)', '', select)
    _quit(the_quit)


@register
def _final_exit():
    """退出注册函数, 程序正常退出后回调"""
    global sql
    sql.exit()


def auto_run():
    """自动运行函数, 固定爬取前两页的图片, 可在DOS控制台下(cmd)直接运行"""
    print u'>>>>>>>>>>当前为自动下载模式<<<<<<<<<<<'
    sel = 1
    start_page = 1
    last_page = 2
    new_folder = u'Auto_add'
    page_urls = get_page_urls(sel, start_page, last_page)
    img_urls = get_img_urls(page_urls, start_page, Headers, new_folder=new_folder)
    generic_downloader(sql, img_urls, Headers)


def main():
    print ur'''>>>>
            程序:  妹子图片爬虫
            网址:  http://www.mzitu.com/
            版本:  0.5
            作者:  KoiSato
            首发:  2018-1-21
            最终:  2018-2-2  
            环境:  Python 2.7
            IDE:   PyCharm
            说明:  基于Requests与MySQL数据库的爬虫程序, 可选择页面范围，或选定页面爬取图片，
                   图片一律下载到page目录的子文件夹里。   
                   输入quit或\q可退出程序。
    >>>>'''
    # multiprocessing.freeze_support()
    # 删除数据库缓存，慎用
    # sql.delete_all_data()
    while True:
        sel, start_page, last_page = init_sel()     # 返回三个参数sel(bool), start_page(int), last_page(int)
        page_urls = get_page_urls(sel, start_page, last_page)
        img_urls = get_img_urls(page_urls, start_page, headers=Headers)
        generic_downloader(sql, img_urls, headers=Headers)
        print u'>>>>>>>>>>下载结束<<<<<<<<<<'

if __name__ == '__main__':
    sql = UrlSql()
    if is_auto:
        auto_run()
    else:
        main()