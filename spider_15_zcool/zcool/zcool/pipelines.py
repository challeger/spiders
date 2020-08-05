# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.pipelines.images import ImagesPipeline

from .settings import IMAGES_STORE


class ZcoolPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        media_request_list = super().get_media_requests(item, info)
        # 给每一个请求附加上图片信息
        for media_request in media_request_list:
            media_request.item = item

        return media_request_list

    def file_path(self, request, response=None, info=None):
        origin_path = super().file_path(request, response=response, info=info)

        # 保存文件夹 = 图片合集标题+作者名称
        img_name = f"{request.item['img_title']}-{request.item['img_author']}"
        # 保存路径
        save_path = os.path.join(IMAGES_STORE, img_name)

        # 判断文件夹是否存在
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        # 图片名称,由url中的.jpg前的字符串组成
        save_name = origin_path.replace('full/', '')
        return os.path.join(save_path, save_name)
