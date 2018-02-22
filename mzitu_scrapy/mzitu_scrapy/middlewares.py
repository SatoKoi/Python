# coding=utf-8


class MeiZiTu(object):

    def process_request(self, request, spider):
        """设置headers和切换请求头
        当每个request通过下载中间件时, 该方法被调用
        :param request: 请求体
        :param spider: spider对象
        :return: None
        """
        referer = request.meta.get('referer', None)
        if referer:
            request.headers['referer'] = referer