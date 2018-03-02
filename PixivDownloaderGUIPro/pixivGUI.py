# -*- coding:utf-8 -*-
"""
桌面级应用 PixivDownloader V.test
"""
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from settings import *
import threading
import manager
import fnmatch
import os
import requests
import time
import json
import sys


class Application(object):
    def __init__(self, Top, img_num=20, manga_block=0, r18_block=0, dir_path=''):
        """初始化控件
        :param Top: 主界面
        control: Label: 用于包含文本或图像
        control: Entry: 单行文本框, 用于收集键盘输入
        control: Button: 按钮, 响应鼠标按下、松开等事件
        control: Listbox: 显示一个选项列表
        function: grid: 网格布局方法
        function: bind: 给控件绑定事件
        """
        self.tk = Top
        try:
            self.tk.iconbitmap(pixiv_icon)
        except TclError:
            pass
        self.tag_flag = False
        self.img_num = img_num
        self.manga_block = IntVar()
        self.r18_block = IntVar()
        if manga_block: self.manga_block.set(1)
        if r18_block: self.r18_block.set(1)
        self.dir_path = dir_path
        Label(self.tk, text='下载模式: ').grid(sticky='E')
        self.modeChosen = ttk.Combobox(self.tk, width=18)
        self.modeChosen['values'] = ('单个作品ID', '画师ID', '排行榜', 'TAG')
        self.modeChosen.grid(row=0, column=1, sticky='E')
        self.modeChosen.set(self.modeChosen['values'][0])
        self.button = Button(self.tk, text='确认', fg='blue', bg='white', command=self.mode_choose)
        self.button.grid(row=0, column=2, sticky='W', padx='5')
        Label(self.tk, text='*图片存储路径: ', fg='red').grid(row=3, column=0)
        self.entry_1 = Entry(self.tk)
        self.entry_1.grid(row=3, column=1)
        self.entry_1.insert(END, self.dir_path)
        self.button1 = Button(self.tk, text='选择文件夹', command=self.select_dir, cursor='')
        self.button1.grid(row=3, column=2, sticky='W', padx='5')
        self.init_first()
        self.work_button_name = StringVar()
        self.work_button_name.set('开始爬取')
        self.work_button = Button(self.tk, textvariable=self.work_button_name, fg='red', bg='white', command=check_message)
        self.work_button.grid(row=4, column=1, sticky='EW')
        # 创建顶级菜单栏
        self.menubar = Menu(self.tk)
        # 创建次级菜单框
        self.menu = Menu(self.menubar, tearoff=0)
        self.instruct_menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label='默认值', command=set_default_settings)
        self.instruct_menu.add_command(label='ReadMe', command=open_readme)
        # self.menu.add_command(label='下载路径', command=save_path_settings)
        self.menubar.add_cascade(label='设置', menu=self.menu)
        self.menubar.add_cascade(label='说明', menu=self.instruct_menu)
        # 将次级菜单框添加到窗口上
        self.tk.config(menu=self.menubar)

    def init_first(self):
        """初始化第一个下载方式"""
        self.select_status = 0
        self.illust_id_label = Label(self.tk, text='*请输入作品id: ', fg='red')
        self.illust_id_label.grid(row=1, column=0)
        self.entry_illust_id = Entry(self.tk)
        self.entry_illust_id.grid(row=1, column=1)

    def mode_choose(self):
        """下载模式选择, 动态显示控件"""
        idx = check_mode(self.modeChosen)
        if idx == 0:
            self.clear_current_status(idx)
            self.init_first()
            center_window(self.tk, 400, 135)
        elif idx == 1:
            center_window(self.tk, 700, 160)
            self.clear_current_status(idx)
            self.member_id_label = Label(self.tk, text='*请输入画师id: ', fg='red')
            self.member_id_label.grid(row=1, column=0)
            self.entry_member_id = Entry(self.tk)
            self.entry_member_id.grid(row=1, column=1)
            self.work_or_collection = ttk.Combobox(self.tk, width='12')
            self.work_or_collection['values'] = ('下载作品', '下载收藏')
            self.work_or_collection.grid(row=1, column=2, sticky='E')
            self.work_or_collection.set(self.work_or_collection['values'][0])
            self.work_or_collection.bind('<FocusIn>', func=self.findFocus)
            self.sel_idx = 0
            self.set_common_settings()
        elif idx == 2:
            center_window(self.tk, 650, 185)
            self.clear_current_status(idx)
            self.rank_label = Label(self.tk, text='*请选择排行榜: ', fg='red')
            self.rank_label.grid(row=1, column=0)
            self.rank_control = ttk.Combobox(self.tk, width='8')
            self.rank_control['values'] = ('年榜', '月榜', '周榜', '日榜')
            self.rank_control.grid(row=1, column=1, sticky='E')
            self.rank_control.set(self.rank_control['values'][2])
            self.rank_control.bind('<FocusIn>', func=self.findFocus)
            self.set_common_settings()
            self.date_label = Label(self.tk, text='*日期: ', fg='blue')
            self.date_label.grid(row=2, column=0, sticky='E')
            self.year_control = ttk.Combobox(self.tk, width='8')
            self.year_control['values'] = [year for year in range(2008, int(time.strftime('%Y', time.localtime())) + 1)]
            self.year_control.grid(row=2, column=1, sticky='E')
            self.year_control.bind('<FocusIn>', func=self.findFocus)
            self.month_control = ttk.Combobox(self.tk, width='6')
            self.month_control['values'] = [month for month in range(1, 13)]
            self.month_control.grid(row=2, column=2, sticky='E')
            self.month_control.bind('<FocusIn>', func=self.findFocus)
            self.day_control = ttk.Combobox(self.tk, width='6')
            self.day_control['values'] = [day for day in range(1, 32)]
            self.day_control.grid(row=2, column=3, sticky='E')
            self.day_control.bind('<FocusIn>', func=self.findFocus)
        elif idx == 3:
            center_window(self.tk, 670, 165)
            self.clear_current_status(idx)
            self.tag_label = Label(self.tk, text='*Tag: ', fg='red')
            self.tag_label.grid(row=1, column=0, sticky='E')
            self.tag1 = ttk.Combobox(self.tk, width='12')
            self.tag1['values'] = ('VOCALOID', '東方', '艦これ', 'Fate', 'FGO', 'アズールレーン', '初音')
            self.tag1.grid(row=1, column=1, sticky='E')
            self.tag2 = ttk.Combobox(self.tk, width='12')
            self.tag2['values'] = ('10000users', '5000users', '3000users', '1000users', '500users')
            self.tag2.grid(row=1, column=2, sticky='E')
            self.tag2.bind('<FocusOut>', func=self.check_tag)
            self.set_common_settings()

    def bind_focus_out(self, event):
        """绑定聚焦失去事件
        :param event: 事件反馈"""
        messagebox.showinfo('Error', '请使用下拉框选择')
        if self.select_status == 1:
            self.current_select = self.work_or_collection.get()
            self.work_or_collection.bind('<FocusOut>', func=self.clear)
        elif self.select_status == 2:
            self.rank_select = self.rank_control.get()
            self.rank_control.bind('<FocusOut>', func=self.clear)
            self.year_select = self.year_control.get()
            self.year_control.bind('<FocusOut>', func=self.clear)
            self.month_select = self.month_control.get()
            self.month_control.bind('<FocusOut>', func=self.clear)
            self.day_select = self.month_control.get()
            self.day_control.bind('<FocusOut>', func=self.clear)

    def clear(self, event):
        """清除绑定"""
        if self.select_status == 1:
            self.work_or_collection.set(self.current_select)
            self.work_or_collection.unbind('<FocusOut>')
        elif self.select_status == 2:
            self.rank_control.set(self.rank_select)
            self.rank_control.unbind('<FocusOut>')
            self.year_control.set(self.year_select)
            self.year_control.unbind('<FocusOut>')
            self.month_control.set(self.month_select)
            self.month_control.unbind('<FocusOut>')
            self.day_control.set(self.day_select)
            self.day_control.unbind('<FocusOut>')

    def findFocus(self, event):
        """回调函数, 绑定响应按键事件"""
        if hasattr(self, 'work_or_collection'):
            self.work_or_collection.bind('<Key>', func=self.bind_focus_out)
        if hasattr(self, 'rank_control'):
            self.rank_control.bind('<Key>', func=self.bind_focus_out)
        if hasattr(self, 'year_control'):
            self.year_control.bind('<Key>', func=self.bind_focus_out)
        if hasattr(self, 'month_control'):
            self.month_control.bind('<Key>', func=self.bind_focus_out)
        if hasattr(self, 'day_control'):
            self.day_control.bind('<Key>', func=self.bind_focus_out)

    def set_common_settings(self, img_label_column=3, img_control_column=3, manga_column=4, r18_column=5):
        """设置共有设定"""
        self.img_num_label = Label(self.tk, text='图集最大\n获取图片数', font='consola -17 normal', fg='#3e83e1')
        self.img_num_label.grid(row=0, column=3, sticky='S')
        self.img_num_control = Scale(self.tk, from_=1, to=50, orient=HORIZONTAL, fg='blue')
        self.img_num_control.grid(row=1, column=3, sticky='NE')
        self.img_num_control.set(self.img_num)
        self.manga_block_control = Checkbutton(self.tk, text='漫画', fg='gray', variable=self.manga_block)
        self.manga_block_control.grid(row=1, column=4, sticky='E')
        self.r18_block_control = Checkbutton(self.tk, text='r18', fg='red', variable=self.r18_block)
        self.r18_block_control.grid(row=1, column=5, sticky='E')

    def clear_current_status(self, idx):
        """切换模式时, 清除当前页面控件"""
        if self.select_status == 0:
            if hasattr(self, 'illust_id_label'):
                self.illust_id_label.grid_forget()
                self.entry_illust_id.grid_forget()
        elif self.select_status == 1:
            self.member_id_label.grid_forget()
            self.entry_member_id.grid_forget()
            self.work_or_collection.grid_forget()
            self.clear_both()
        elif self.select_status == 2:
            self.rank_label.grid_forget()
            self.rank_control.grid_forget()
            self.date_label.grid_forget()
            self.year_control.grid_forget()
            self.day_control.grid_forget()
            self.month_control.grid_forget()
            self.clear_both()
        elif self.select_status == 3:
            self.tag_label.grid_forget()
            self.tag1.grid_forget()
            self.tag2.grid_forget()
            if hasattr(self, 'tag3'):
                self.tag3.grid_forget()
            self.clear_both()
        self.select_status = idx

    def clear_both(self):
        """清除共有控件"""
        self.img_num_label.grid_forget()
        self.img_num_control.grid_forget()
        self.manga_block_control.grid_forget()
        self.r18_block_control.grid_forget()

    def select_dir(self):
        """选择文件夹, 设置路径
        :function askdiretory: 获取文件夹路径
                      :return: 选择路径名称
        """
        fn = filedialog.askdirectory()
        if not fn:
            return
        self.entry_1.delete(0, len(self.entry_1.get()))
        self.entry_1.insert(END, fn)

    def check_tag(self, event):
        """检查tag是否含有字符"""
        text = self.tag2.get()
        if text and not self.tag_flag:
            self.tk.geometry('670x188')
            self.tag3 = ttk.Combobox(self.tk, width='12')
            self.tag3['values'] = ('少女', '女の子', '背景', '百合', '风景', 'ロリ')
            self.tag3.grid(row=2, column=2, sticky='E')
            self.tag_flag = True
        elif not text and self.tag_flag:
            self.tk.geometry('670x165')
            self.tag3.grid_forget()
            self.tag_flag = False

    def _listen_window_close(self):
        """监听关闭窗口事件"""
        self.tk.protocol('WM_DELETE_WINDOW', func=close_all)


class PixivSpiderTK(Tk):
    def __init__(self, title):
        """初始化控件"""
        super(PixivSpiderTK, self).__init__()
        self.wm_title(title)
        self.read_flag = False
        try:
            self.iconbitmap(pixiv_icon)
        except TclError:
            pass
        self.resizable(False, False)
        self._create_control()
        center_window(self, 800, 500)

    def _create_control(self):
        """创建控件"""
        self.title_label = Label(self, text='Pixiv下载器 V1.5', fg='#49c', font='MicrosoftYahei -20 bold')
        self.title_label.pack(side='top')
        self.message = Message(self, text='  作者: KoiSato\n  日期: 2018-02-28\n  '
                                           '图源: www.pixiv.net\n   Api: https://api.imjad.cn/pixiv.md\n'
                                           'Github: https://github.com/SatoKoi', fg='purple', font='consola -16 bold',
                                  width=400)
        self.message.pack(after=self.title_label, side='top', anchor='w')
        self.split_label = Label(self, text='{:-^125}'.format(''), fg='#999')
        self.split_label.pack(after=self.message, anchor='center')
        # 建立Text与Scrollbar联立的框架
        self.text_frame = Frame(self)
        self.text_control = Text(self.text_frame, font='Yaheiconsola -16 normal', width='100', selectbackground='#64a6e3', selectforeground='white',
                                 spacing1='2')
        self.text_control.pack(side='left', fill='both', anchor='center')
        self.text_scroll_bar = Scrollbar(self.text_frame)
        self.text_scroll_bar.pack(side='right', fill='y')
        # 纵向滑动条绑定Text Y方向显示
        self.text_scroll_bar.config(command=self.text_control.yview)
        # Text绑定纵向滑动滚动条
        self.text_control.config(yscrollcommand=self.text_scroll_bar.set)
        self.text_frame.pack(after=self.split_label)

    def _listen_window_close(self):
        """监听窗口关闭事件"""
        self.protocol(name='WM_DELETE_WINDOW', func=open_pixiv_gui)

    def test_work(self):
        """多线程测试用"""
        self.threading_flag = True
        for i in range(100):
            self.text_control.insert(END, str(i))
            self.text_control.update()
            self.text_control.see(END)
            time.sleep(0.05)

    def get_settings(self, mode, **kwargs):
        """获取设置"""
        def get_common(kwargs):
            """获取相同设置"""
            atlas_count = kwargs.get('atlas_count')
            manga_block = kwargs.get('manga_block')
            r_18_block = kwargs.get('r_18_block')
            dir_path = kwargs.get('dir_path')
            return atlas_count, manga_block, r_18_block, dir_path
        self.update()
        if mode == 0:
            illust_id = kwargs.get('illust_id')
            dir_path = os.path.join(kwargs.get('dir_path'), 'p站单图下载')
            self.threading_start(self.single_work, illust_id, dir_path)
        elif mode == 1:
            member_id = kwargs.get('member_id')
            sel_mode = kwargs.get('sel_mode')
            atlas_count, manga_block, r_18_block, dir_path = get_common(kwargs)
            self.threading_start(self.multi_work, member_id, sel_mode, atlas_count, manga_block, r_18_block, dir_path)
        elif mode == 2:
            rank = kwargs.get('rank')
            date = kwargs.get('date')
            atlas_count, manga_block, r_18_block, dir_path = get_common(kwargs)
            self.threading_start(self.rank_work, rank, date, atlas_count, manga_block, r_18_block, dir_path)
        elif mode == 3:
            tags = kwargs.get('tags')
            atlas_count, manga_block, r_18_block, dir_path = get_common(kwargs)
            self.threading_start(self.search_work, tags, atlas_count, manga_block, r_18_block, dir_path)

    def threading_start(self, target, *args, **kwargs):
        """开启一个线程完成爬取功能"""
        self.task_threading = threading.Thread(target=target, args=args, kwargs=kwargs)
        self.task_threading.setName('task_threading')
        self.task_threading.daemon = True
        self.task_threading.start()

    def single_work(self, illust_id, dir_path):
        """单图下载"""
        single_downloader(headers, illust_id=illust_id, dir_path=dir_path, cls=self)

    def multi_work(self, member_id, sel_mode, atlas_count, manga_block, r_18_block, dir_path):
        """多图下载"""
        multi_downloader(800, 1, member_id, sel_mode, manga_block, r_18_block, atlas_count, dir_path, cls=self)

    def rank_work(self, rank, date, atlas_count, manga_block, r_18_block, dir_path):
        """排行榜下载"""
        rank_downloader(rank, date, manga_block, r_18_block, atlas_count, dir_path, cls=self)

    def search_work(self, tags, atlas_count, manga_block, r_18_block, dir_path):
        """Tag下载"""
        search_tag_downloader(tags, dir_path, manga_block, r_18_block, atlas_count, cls=self)

    def wrap_it(self, string):
        """包装信息"""
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.text_control.insert(END, '[Time: {}] >>>>>> {}\n'.format(current_time, string))
        # 实时查看底部数据, 使scrollbar自动下滑
        self.text_control.see(END)
        # 实时更新数据
        self.text_control.update()


class SettingTk(Tk):
    def __init__(self, title='PixivDownloader V.Test', img_num=20, manga_block=0, r18_block=0, dir_path=''):
        super(SettingTk, self).__init__()
        try:
            self.iconbitmap(settings_icon)
        except TclError:
            pass
        self.wm_title(title)
        self.resizable(False, False)
        self.img_num = img_num
        self.manga_block = manga_block
        self.dir_path = dir_path
        self.r18_block = r18_block
        self.create_flag = False
        self.select_flag = False
        center_window(self, 400, 135)

    def create_control(self):
        if not self.create_flag:
            self.text_label = Label(self, text='默认值设置', font='YaheiConsola -16 bold', fg='#f1441b')
            self.text_label.pack(side='top', anchor='center')
            self.img_frame = Frame(self)
            self.img_num_label = Label(self.img_frame, text='图集最大获取图片数', font='consola -17 normal', fg='#3e83e1',
                                       anchor='w', padx='15', pady='20')
            self.img_num_label.pack(side='left')
            self.img_num_control = Scale(self.img_frame, from_=1, to=50, orient=HORIZONTAL, fg='blue')
            self.img_num_control.pack(side='right')
            self.img_num_control.set(self.img_num)
            self.img_frame.pack(after=self.text_label)
            self.control_frame = Frame(self)
            self.manga_label = Label(self.control_frame, text='漫画', padx='12')
            self.manga_label.pack(side='left')
            self.manga_control = ttk.Combobox(self.control_frame, width='6')
            self.manga_control['values'] = ('不下载', '下载')
            self.manga_control.pack(side='left')
            self.manga_control.set(self.manga_control['values'][self.manga_block])
            self.r18_label = Label(self.control_frame, text='r18', padx='12')
            self.r18_label.pack(side='left')
            self.r18_control = ttk.Combobox(self.control_frame, width='6')
            self.r18_control['values'] = ('不下载', '下载')
            self.r18_control.pack(side='left')
            self.r18_control.set(self.r18_control['value'][self.r18_block])
            self.control_frame.pack(after=self.img_frame)
            self.dir_frame = Frame(self)
            self.dir_label = Label(self.dir_frame, text='默认存储路径: ', fg='#333', padx='10')
            self.dir_label.pack(side='left')
            self.dir_entry = Entry(self.dir_frame, width='25')
            self.dir_entry.pack(side='left')
            self.dir_entry.insert(END, self.dir_path)
            self.dir_button = Button(self.dir_frame, text='打开文件夹', padx='20', bg='#e5e5e5', command=self.select_dir)
            self.dir_button.pack(side='right', expand=0)
            self.dir_frame.pack(after=self.control_frame)
            self.confirm_button = Button(self, text='确认', command=self.confirm)
            self.confirm_button.pack(side='bottom', after=self.dir_frame, ipadx='20')
            self.create_flag = True

    def _listen_window_close(self):
        self.protocol(name='WM_DELETE_WINDOW', func=self.change_status)

    def change_status(self):
        global setting_tk_active
        setting_tk_active = False
        self.withdraw()
        center_window(app.tk, 400, 135)

    def confirm(self):
        img_num = self.img_num_control.get()
        fn = self.dir_entry.get()
        manga = self.manga_control.get()
        r18 = self.r18_control.get()
        try:
            manga_block = self.manga_control['values'].index(manga)
        except ValueError:
            messagebox.showinfo('Error', '漫画栏选择错误, 请用下拉框选择')
            return
        try:
            r18_block = self.r18_control['values'].index(r18)
        except Error:
            messagebox.showinfo('Error', 'r18栏选择错误, 请用下拉框选择')
            return
        if not check_dir_path(fn):
            self.dir_entry.delete(0, len(fn))
            return
        data = {'img_num': img_num,
                'manga_block': manga_block,
                'r18_block': r18_block,
                'dir_path': fn}
        try:
            fp = open(json_file_path, 'w', encoding='utf-8')
        except FileNotFoundError:
            os.mkdir(json_file_path[:-9])
            fp = open(json_file_path, 'w', encoding='utf-8')
        json.dump(data, fp, sort_keys=True, indent=4, ensure_ascii=False)
        fp.close()
        threading.Thread(target=messagebox.showinfo, args=('PixivDownloader V.Test', '设置成功, 重新启动将载入配置')).start()
        app.tk.deiconify()
        app.tk.geometry('+10000+10000')

    def select_dir(self):
        if not self.select_flag:
            self.select_flag = True
            fn = filedialog.askdirectory()
            self.select_flag = False
            if not fn:
                return
            self.dir_entry.delete(0, len(self.dir_entry.get()))
            self.dir_entry.insert(END, fn)
        else:
            return


def set_default_settings():
    """开始设置默认值, 打开设置默认值窗口"""
    global setting_tk_active
    if not setting_tk_active:
        app.tk.geometry('+10000+10000')
        setting_tk.create_control()
        setting_tk.deiconify()
        setting_tk_active = True
        setting_tk._listen_window_close()
        setting_tk.mainloop()
    else:
        return


def open_pixiv_gui():
    """显示设置面板, 隐藏爬取页面"""
    ptk.text_control.delete(0.0, END)
    if ptk.read_flag:
        center_window(tk, 400, 135)
        tk.deiconify()
        ptk.withdraw()
        return
    if ptk.task_threading.is_alive() and messagebox.askyesno('PixivDownloader V.Test', '当前正在爬取图片, 确认在后台运行程序?'):
        center_window(tk, 400, 135)
        tk.deiconify()
        ptk.withdraw()
        check_threading = threading.Thread(target=threading_is_alive, args=(ptk.task_threading,))
        check_threading.daemon = True
        check_threading.start()
    elif not ptk.task_threading.is_alive():
        center_window(tk, 400, 135)
        tk.deiconify()
        ptk.withdraw()


def threading_is_alive(threading):
    """检测爬取线程是否仍在工作"""
    set_flag = False
    while True:
        if threading.is_alive():
            if not set_flag:
                app.work_button_name.set('正在爬取')
                app.work_button.config(command=show_detail)
                set_flag = True
        else:
            messagebox.showinfo('PixivDownloader V.Test', '下载图片完成')
            app.work_button_name.set('开始爬取')
            app.work_button.config(command=show_spider)
            break


def center_window(root, width, height):
    """水平居中, 垂直中间靠上"""
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    currentWidth = (screenwidth - width)/2
    currentHeight = (screenheight - height)/2.5
    size = '+%d+%d' % (currentWidth, currentHeight)
    root.geometry(size)
    return currentWidth, currentHeight


def init_tk():
    """窗口初始化"""
    tk = Tk()
    tk.title('PixivDownloader设置面版')
    center_window(tk, 400, 135)
    tk.resizable(False, False)
    return tk


def check_mode(modeChosen):
    """检查模式选择"""
    mode_str = modeChosen.get()
    try:
        idx = modeChosen['values'].index(mode_str)
        return idx
    except ValueError:
        messagebox.showinfo('Error', '请选择正确的下载模式')
        return -1


def check_id(_id, select_status):
    """检查作品id输入"""
    _type = '作品' if select_status == 0 else '画师'
    if not _id:
        messagebox.showinfo('Error', '请输入{}id!'.format(_type))
        if hasattr(app, 'entry_illust_id'):
            app.entry_illust_id.focus()
        else:
            app.entry_member_id.focus()
        return False
    elif select_status == 0:
        try:
            int(_id)
        except ValueError:
            messagebox.showerror('Error', '作品id只能为数字!')
            app.entry_illust_id.delete(0, len(_id))
            return False
    return True


def check_dir_path(dir_path):
    """获取文件夹路径名称"""
    if setting_tk_active:
        app.tk.withdraw()
        setting_tk.wm_attributes('-topmost', 0)
        if not dir_path:
            messagebox.showinfo('Error', '请设置图片存放路径')
            app.tk.deiconify()
            setting_tk.wm_attributes('-topmost', 1)
            return False
        if not re.search(r'(\w+):/.*', dir_path):
            messagebox.showerror('Error', '图片存放路径格式错误 ')
            app.tk.deiconify()
            setting_tk.wm_attributes('-topmost', 1)
            return False
    else:
        if not dir_path:
            messagebox.showinfo('Error', '请设置图片存放路径')
            return False
        if not re.search(r'(\w+):/.*', dir_path):
            messagebox.showerror('Error', '图片存放路径格式错误 ')
            return False
    return True


def check_date(year, month, day):
    """检测是否有错误格式的日期"""
    if not year:
        messagebox.showinfo('Error', '请选择年份!')
        return False
    if not month:
        messagebox.showinfo('Error', '请选择月份')
        return False
    if not day:
        messagebox.showinfo('Error', '请选择日期')
        return False
    try:
        int(year)
    except ValueError:
        messagebox.showinfo('Error', '请选择年份!')
        return False
    try:
        int(month)
    except ValueError:
        messagebox.showinfo('Error', '请选择月份!')
        return False
    try:
        int(year)
    except ValueError:
        messagebox.showinfo('Error', '请选择日期!')
        return False
    return True


def check_message():
    """检查信息输入"""
    dir_path = app.entry_1.get()
    if app.select_status == 0:
        illust_id = app.entry_illust_id.get()
        if not check_id(illust_id, app.select_status):
            return
        if not check_dir_path(dir_path):
            app.entry_1.delete(0, len(dir_path))
            return
        app.entry_illust_id.delete(0, len(illust_id))
        show_spider(app.select_status, illust_id=illust_id, dir_path=dir_path)
    elif app.select_status == 1:
        member_id = app.entry_member_id.get()
        if not check_id(member_id, app.select_status):
            return
        if not check_dir_path(dir_path):
            app.entry_1.delete(0, len(dir_path))
            return
        sel_str = re.search(r'([\u4e00-\u9fa5])+', app.work_or_collection.get()).group()
        sel_mode = app.work_or_collection['values'].index(sel_str)
        atlas_count, manga_block, r_18_block = get_common_settings()
        app.entry_member_id.delete(0, len(member_id))
        app.entry_1.delete(0, len(dir_path))
        show_spider(app.select_status, member_id=member_id, sel_mode=sel_mode, atlas_count=atlas_count,
                    manga_block=manga_block, r_18_block=r_18_block, dir_path=dir_path)

    elif app.select_status == 2:
        # 中文unicode字符集
        rank_str = re.search(r'([\u4e00-\u9fa5])+', app.rank_control.get()).group()
        rank = app.rank_control['values'].index(rank_str)
        year, month, day = app.year_control.get(), app.month_control.get(), app.day_control.get()
        if not check_date(year, month, day):
            return
        if len(month) < 2:
            month = '0' + month
        if len(day) < 2:
            day = '0' + day
        date = date_confirm(rank, ''.join([year, month, day]))
        if not date:
            messagebox.showinfo('Error', '请选择正确的日期')
            app.day_control.delete(0, len(app.day_control.get()))
            return
        if not check_dir_path(dir_path):
            app.entry_1.delete(0, len(dir_path))
            return
        atlas_count, manga_block, r_18_block = get_common_settings()
        app.year_control.delete(0, len(app.year_control.get()))
        app.month_control.delete(0, len(app.month_control.get()))
        app.day_control.delete(0, len(app.day_control.get()))
        show_spider(app.select_status, rank=rank, date='-'.join([date[:4], date[4:6], date[-2:]]), atlas_count=atlas_count,
                    manga_block=manga_block, r_18_block=r_18_block, dir_path=dir_path)

    elif app.select_status == 3:
        tags = []
        tags.append(app.tag1.get())
        tags.append(app.tag2.get())
        if hasattr(app, 'tag3'):
            tags.append(app.tag3.get())
        if len(tags) < 1:
            messagebox.showinfo('Error', '必须填写一个tag栏')
            return
        if not check_dir_path(dir_path):
            app.entry_1.delete(0, len(dir_path))
            return
        atlas_count, manga_block, r_18_block = get_common_settings()
        show_spider(app.select_status, tags=tags, atlas_count=atlas_count, manga_block=manga_block, r_18_block=r_18_block,
                    dir_path=dir_path)


def show_spider(mode, **kwargs):
    """开始爬取页面显示"""
    tk.withdraw()
    ptk.deiconify()
    # ptk.test_work()
    ptk.get_settings(mode, **kwargs)
    ptk.mainloop()


def show_detail():
    """显示爬取页面"""
    tk.withdraw()
    ptk.deiconify()


def close_all():
    """退出程序"""
    import sys
    if hasattr(ptk, 'task_threading'):
        if ptk.task_threading.is_alive():
            if messagebox.askyesno('PixivDownloader V.Test', '爬虫正在后台运行, 是否退出程序?'):
                sys.exit()
    sys.exit()


def mk_dir(dir_path, cls=None):
    """创建文件夹"""
    if not os.path.exists(dir_path):
        if cls:
            cls.wrap_it('正在创建文件夹 {}'.format(dir_path))
            os.mkdir(dir_path)
    return dir_path


def running_time(function):
    """获取爬虫运行时间, 此函数作为装饰器包装爬虫函数"""
    def work(*args):
        """对传入函数进行包装, *arg -> args为元组参数, *args对元组拆包
        此处*args表示爬虫函数的多个参数"""
        cls = args[-1]
        start_time = time.time()
        function(*args)
        stop_time = time.time()

        def time_decorate(start, stop):
            """时间修饰"""
            temp = stop - start
            minute = temp // 60
            sec = temp - minute * 60
            return minute, sec
        cls.wrap_it('爬虫运行时间: {0[0]:.0f} 分 {0[1]:.0f} 秒\n'.format(time_decorate(start_time, stop_time)))
    return work


def get_common_settings():
    """获取公共设置"""
    return app.img_num_control.get(), app.manga_block.get(), app.r18_block.get()


def has_number(input_string):
    """检查字符串是否含有数字"""
    return any(char.isdigit() for char in input_string)


def is_word(input_string):
    """检查字符串是否全为字母"""
    return all(char.isalpha() for char in input_string)


def date_confirm(mode, date):
    """日期确认"""
    local_date = time.strftime('%Y%m%d', time.localtime())
    if date > local_date:
        app.year_control.delete(0, len(app.year_control.get()))
        app.month_control.delete(0, len(app.month_control.get()))
        app.day_control.delete(0, len(app.day_control.get()))
        return False
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
        if mode == 1:
            date = str(year) + date[-4:-2] + '31'
        if month == 2 and day > ren_day_get(year):
            return False
        elif month == 2 and day < ren_day_get(year) and mode == 1:
            date = str(year) + date[-4:-2] + str(ren_day_get(year))
        if (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
            return False
        elif (month == 4 or month == 6 or month == 9 or month == 11) and day < 30 and mode == 1:
            date = str(year) + date[-4:-2] + '31'
        if mode == 0:
            if month > 6:
                date = str(year) + '1231'
            else:
                date = str(year) + '0630'
        return date
    else:
        return False


def get_img_name(img_url):
    """获取图片名字"""
    index = img_url.rindex('/')
    return img_url[index + 1:]


def get_img_status(json_str, manga_block=False, single_flag=False, atlas_count=20, unwanted_tags=None, cls=None):
    """获取图片状态"""
    imgs_status = []
    page_count = 0
    now = lambda: time.time()
    atlas_count = atlas_count if not single_flag else 100
    try:
        response_list = json_str['response']
    except KeyError:
        cls.wrap_it('获取资源失败! 请核实信息是否正确输入!')
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
            cls.wrap_it('当前已获取{} 张图片'.format(page_count))

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
        cls.wrap_it('没有获取到图片资源, 请确认该用户是否有图片资源!!!')
        return None
    if works:
        response_list = works
        cls.wrap_it('图片资源正在获取, 请稍等...')
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
    cls.wrap_it('图片资源已获取, 当前资源共{}张图片'.format(page_count))
    return imgs_status


def single_downloader(headers, illust_id=None, dir_path=None, cls=None):
    """单张图片下载"""
    correct_url = (api_url + '&id=%d') % (illust, int(illust_id))
    json_str = requests.get(correct_url).json()

    @running_time
    def img_download(headers, dir_path=None, cls=None):
        """图片下载"""
        img_status = get_img_status(json_str, single_flag=True, cls=cls)[0]
        img_url = img_status['img_url']
        mk_dir(dir_path, cls)
        if not isinstance(img_url, list):
            file_path = '/'.join([dir_path, get_img_name(img_url)])
            with open(file_path, 'wb') as f_obj:
                resp = requests.get(img_url, headers=headers)
                f_obj.write(resp.content)
        else:
            _id = img_status['id']
            dir_path += '/{}'.format(_id)
            mk_dir(dir_path, cls)
            for url in img_url:
                img_name = get_img_name(url)
                file_path = '/'.join([dir_path, img_name])
                if os.path.exists(file_path):
                    cls.wrap_it('{} 图片已存在'.format(img_name[:-4]))
                else:
                    with open(file_path, 'wb') as f_obj:
                        resp = requests.get(url, headers=headers)
                        f_obj.write(resp.content)
        cls.wrap_it('{} 图片下载成功'.format(illust_id))
    img_download(headers, dir_path, cls)


def multi_downloader(per_page, page, _id, sel_mode, manga_block, r_18_block, atlas_count, dir_path, cls=None):
    """多图下载器"""
    manga = '不获取'
    r_18_str = '不获取'
    if manga_block:
        manga = '获取'
    if r_18_block:
        r_18_str = '获取'
    _type = member_illust
    threading_num = 15
    folder_name = str(_id) + u'_画师作品'
    if sel_mode == 1:
        folder_name = str(_id) + u'_用户收藏'
        _type = favorite
    dir_path = os.path.join(dir_path, folder_name)
    cls.wrap_it('总页数: {}, 单页作品数: {}, 类型: {}, 漫画: {}, r18: {}, 单个图集最大图片数量: {}'
            .format(page, per_page, folder_name[-4:], manga, r_18_str, atlas_count))
    cls.wrap_it('当前正在获取{}资源, 请稍等...'.format(folder_name[-4:]))
    correct_url = (api_url + '&id=%d&per_page=%d&page=%d') % (_type, int(_id), per_page, page)
    start_to_work(correct_url, threading_num, dir_path, manga_block, r_18_block, atlas_count, cls)


@running_time
def start_to_work(url, threading_num, folder_name, manga_block, r_18_block, atlas_count, cls, tags=None):
    """爬虫管理下载机制启动"""
    json_str = requests.get(url, headers=headers).json()
    all_illusts = get_img_status(json_str, atlas_count=atlas_count, unwanted_tags=tags, cls=cls)
    if all_illusts is None:
        return
    checker = manager.Checker(all_illusts, folder_name, r_18_block)
    checker.check(cls=cls)
    downloader = manager.Downloader(checker.img_queue, threading_num, folder_name)
    downloader.work(cls=cls)


def rank_downloader(sel_mode, date, manga_block, r_18_block, atlas_count, dir_path, cls=None, per_page=800, page=1, block=False):
    """排行榜下载器"""
    manga = '不获取'
    r_18_str = '不获取'
    _type = rank
    _mode = mode_year
    threading_num = 15
    if manga_block:
        manga = '获取'
    if r_18_block:
        r_18_str = '获取'
    folder_name = dir_path + '/' + date[:4] + u'年' + date[5:7] + u'月年榜'
    if sel_mode == 1:
        if not block:
            per_page = 300
        _mode = mode_month
        folder_name = dir_path + '/' + date[:4] + u'年' + date[5:7] + u'月月榜'
    elif sel_mode == 2:
        if not block:
            per_page = 150
        _mode = mode_week
        folder_name = dir_path + '/' + date[:4] + u'年' + date[5:7] + u'月' + date[-2:] + u'日周榜'
    elif sel_mode == 3:
        if not block:
            per_page = 100
        _mode = mode_day
        folder_name = dir_path + '/' + date[:4] + u'年' + date[5:7] + u'月' + date[-2:] + u'日日榜'
    cls.wrap_it('总页数: {}, 单页作品数: {}, 类型: {}, 漫画: {}, r18: {}, 日期: {}, 单个图集最大图片数量: {}'
            .format(page, per_page, folder_name[-2:], manga, r_18_str, date, atlas_count))
    correct_url = (api_url + '&mode=%s&per_page=%d&page=%d&date=%s') % (_type, _mode, per_page, page, date)
    start_to_work(correct_url, threading_num, folder_name, manga_block, r_18_block, atlas_count, cls)


def search_tag_downloader(key_list, dir_path, manga_block, r_18_block, atlas_count, cls=None, per_page=800, page=1):
    """搜索下载器"""
    global tags, manga, r_18_str
    threading_num = 15
    key_list = sorted(key_list, key=lambda x: (x.isdigit(), has_number(x), is_word(x), x.isupper(), x))
    key_word = ' '.join(key_list)
    folder_name = dir_path + '/' + key_word
    _type = 'search'
    _mode = 'tag'
    if manga_block:
        manga = '获取'
    if r_18_block:
        r_18_str = '获取'
    cls.wrap_it('总页数: {}, 单页作品数: {}, 关键字: {}, 剔除标签: {}, 漫画: {}, r18: {}, 单个图集最大图片数量: {}'
            .format(page, per_page, key_word, ' '.join(tags), manga, r_18_str, atlas_count))
    correct_url = (api_url + '&mode=%s&per_page=%d&page=%d&word=%s&period=%s&order=%s') %\
                  (_type, _mode, per_page, page, key_word, period, order)
    start_to_work(correct_url, threading_num, folder_name, manga_block, r_18_block, atlas_count, cls, tags)


def get_json_data(json_file_path):
    """获取json数据"""
    try:
        fp = open(json_file_path, 'r', encoding='utf-8')
        data = json.load(fp)
    except FileNotFoundError:
        data = None
    except json.JSONDecodeError:
        data = None
    return data


def open_readme():
    ptk.read_flag = True
    app.tk.geometry('+2000+2000')
    ptk.deiconify()
    try:
        with open('./readme.md', 'r', encoding='utf-8') as f:
            ptk.text_control.insert(END, f.read())
            ptk.text_control.update()
    except Exception:
        messagebox.showerror('Error', '找不到readme文件')


if __name__ == '__main__':
    data = get_json_data(json_file_path)
    tk = init_tk()
    ptk = PixivSpiderTK('PixivDownloader V.Test')
    ptk.withdraw()
    if data:
        app = Application(tk, **data)
        setting_tk = SettingTk(title='PixivDownloader V.Test', **data)
    else:
        app = Application(tk)
        setting_tk = SettingTk()
    app._listen_window_close()
    ptk._listen_window_close()
    setting_tk.withdraw()
    setting_tk_active = False
    tk.mainloop()
