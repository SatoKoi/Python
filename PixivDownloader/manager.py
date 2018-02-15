# -*- coding:utf-8 -*-
import threading
from queue import Queue
from function import *


class DownloaderThreading(threading.Thread):
    """下载器线程"""
    def __init__(self, tid, queue, folder_name):
        threading.Thread.__init__(self)
        self.queue = queue
        self.headers = headers
        self.folder_name = folder_name
        self.tid = tid

    def run(self):
        """线程运行"""
        while True:
            if not self.queue.empty():
                img_url = self.queue.get()
                img_name = get_img_name(img_url)
                wrap_it('[Threading {}]: 正在下载图片 {}, 剩余 {} 张图片'.format(self.tid, img_name[:-4], self.queue.qsize()))
                file_path = os.path.join(sys.path[0], self.folder_name, img_name)
                if os.path.exists(file_path):
                    wrap_it('Report: 该图片 {} 已存在, 将跳过下载'.format(img_name[:-4]))
                    time.sleep(0.05)
                    continue
                while True:
                    try:
                        with open(file_path, 'wb') as f_obj:
                            resp = requests.get(img_url, headers=self.headers, timeout=40)
                            f_obj.write(resp.content)
                        break
                    except ConnectionError as e:
                        wrap_it('网络连接错误{}'.format(e))
                    except Exception as e:
                        print(e, '{} 图片未能成功下载'.format(img_name[:-4]))
            else:
                break


class Downloader:
    """下载器"""
    def __init__(self, queue, threading_num, folder_name):
        self.queue = queue
        self.threading_num = threading_num
        self.folder_name = folder_name

    def work(self):
        """创建线程"""
        threading_list = []
        wrap_it('下载器开始创建线程')
        new_threading_num = self.queue.qsize() + 1 if self.queue.qsize() < self.threading_num else self.threading_num + 1
        for t in range(1, new_threading_num):
            wrap_it('[Threading {}]: Created'.format(t))
            new_threading = DownloaderThreading(t, self.queue, self.folder_name)
            new_threading.start()
            threading_list.append(new_threading)
        for t in range(1, new_threading_num):
            threading_list[t-1].join()
            wrap_it('[Threading {}]: Destroyed'.format(t))


class Checker(object):
    """筛选器"""
    def __init__(self, illusts, folder_name):
        self.illusts = illusts
        self.folder_name = folder_name
        self.img_queue = Queue()

    def check(self):
        wrap_it('管理器将对资源进行审查')
        count = 0
        for _illust in self.illusts:
            tid = _illust['id']
            if r_18 is False and _illust['age_limit'] == 'r18':
                continue
            if isinstance(_illust['img_url'], list):
                for url in _illust['img_url']:
                    self.img_queue.put(url)
                    count += 1
            else:
                self.img_queue.put(_illust['img_url'])
                count += 1
        wrap_it('审查后待下载图片数为 {}, 将在2s后开始下载'.format(count))
        mk_dir(self.folder_name)
        time.sleep(2)

    @property
    def queue(self):
        return self.img_queue

    def get_status(self, **kwargs):
        return kwargs


class Getter:
    """获取器"""
    def __init__(self, per_page, page):
        self.per_page = per_page
        self.page = page
        self.mode = mode_sel()

    def work(self):
        if self.mode == 1:
            single_downloader(headers)
        elif self.mode == 2:
            multi_downloader(self.per_page, self.page)
        elif self.mode == 3:
            rank_downloader(self.per_page, self.page, self.page_block)
        elif self.mode == 4:
            search_tag_downloader(self.per_page, self.page)

    @property
    def page_block(self):
        if self.per_page == 800 and self.page == 1:
            return False
        return True

