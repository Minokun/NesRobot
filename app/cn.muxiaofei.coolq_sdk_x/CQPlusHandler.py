#coding:utf-8
import cqplus
import os
import  configparser
import time
import requests
import pickle

class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):
        # 群聊信息
        # if event == 'on_group_msg':
        #     # user_info = self._api.get_group_member_info(params['from_group'], params['from_qq'], False)
        #     # # 此处是获取用户信息的代码
        #     # for key in user_info:
        #     #     self.logging.debug(key + "  " + str(user_info[key]))
        #     # self.logging.debug(params['msg'])
        #     send_msg = "{}".format(msg)
        #     self.logging.debug(send_msg)
        #     cqplus._api.send_group_msg(params["env"], target_group, send_msg)

        if event == 'on_timer':
            if params['name'] == 'news':
                with open('./var.pk', 'rb') as fp:
                    var_dict = pickle.load(fp)
                id_max = self.pushNews(var_dict['id_max'], params)
                with open('./var.pk', 'wb') as fp:
                    pickle.dump({'id_max': id_max}, fp)

    def pushNews(self, id_max, params):
        target_group = 489825174
        url = 'http://zhibo.sina.com.cn/api/zhibo/feed?page_size=20&zhibo_id=152&tag_id=0&dpc=1&pagesize=20'
        response = requests.get(url).json()
        new_list = response['result']['data']['feed']['list']
        id_new = new_list[0]['id']
        if id_new > id_max:
            rich_text = new_list[0]['rich_text']
            send_msg = "※插播新浪快讯：※\r\n" + rich_text
            cqplus._api.send_group_msg(params["env"], target_group, send_msg)
        return id_new
pass