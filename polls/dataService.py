# -*- coding:utf8 -*-
import json
import requests
import logging
import hashlib
logger = logging.getLogger('mfly')

urls = {
    'beta':'http://10.255.72.154:18090/fengjr-p2passet-data-collection/rmdata/api/info/current/dic-data-set',
    'on':'http://10.10.51.180:17066/rmdata/api/info/current/dic-data-set'
}
TRUE = 'true'
FALSE = 'false'

POST = 'POST'
GET = 'GET'
# 返回值格式化
def output(status, data, extra= {}):
    return {'status': status, 'data': data, 'extra': extra}


class DataService(object):

    def __init__(self, supplier, interface, passport, phone = None, **kwargs):
        '''
        数据服务Python SDK
        :param supplier: 厂商名
        :param interface: 接口名称
        :param passport: 身份证
        :param columns: 默认[] 返回接口所有列
        :param env: 环境 ，默认为测试环境地址
        :param phone: 手机号 查询爬虫接口时必须传递
        :param source: 预留字段，查询来源方   dm：数据挖掘
        '''
        self.supplier = supplier
        self.interface = interface
        self.passport = passport
        self.phone = phone
        self.productChannel = kwargs.get('productChannel')
        self.productNo = kwargs.get('productNo')
        self.card = kwargs.get('bankCard')
        if self.supplier == 'fjr' and self.interface == 'contact':
            if self.productChannel == 'mz':
                self.supplier = 'mz'
            elif self.productChannel == 'rzj':
                self.supplier = 'rzj'
            elif self.productChannel == 'wygjj':
                self.supplier = 'wygjj'
            else:
                pass

    def getMd5(self,string):
        method_md5 = hashlib.md5()
        method_md5.update("http://edw.fengjr.com")
        method_md5.update(string)
        res = method_md5.hexdigest().lower()
        return res

    def get_data(self):
        rate = {'test':'test_housefund_rate_id_89757',
                'beta':'beta_housefund_rate_id_89757',
                'on':'online_housefund_rate_id_89757'}
        if not self.supplier or not self.interface or not self.passport:
            logger.error('dataservice get_data :%s', 'param error')
            return output(FALSE, {'msg': 'param error'})

        if self.interface == 'user_ydd':
            self.passport = self.getMd5(self.passport)
        if self.interface == 'housefund_rate':
            self.passport = rate['beta']
        query_key = {
            'id': self.passport,
        }
        if self.phone:
            query_key['phone'] = self.phone
        if self.productNo:
            query_key['product_no'] = self.productNo
        if self.productChannel:
            query_key['channel'] = self.productChannel
        if self.card:
            query_key['card'] = self.card
        params = {}
        params["query_key"] = query_key
        params[self.interface] = {"dic":[],"expire_time":9999999999}
        params["org_id"] = self.supplier
        params["query_user_name"] = "test"
        print(params)
        try:
            url = urls['beta']
            r = requests.post(url, json.dumps(params))
            print(r.content)
            return json.loads(r.content)[self.interface]
        except Exception as e:
            logger.info('dataservice get_data Exception :%s', e)
            return {}



if __name__ == '__main__':
    a = DataService('model','fw_app_credit_brlargecash_V1','440301196512057177',productChannel='wygjj')
    print(a.get_data())
