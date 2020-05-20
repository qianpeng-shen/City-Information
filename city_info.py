
# -*- coding: utf-8 -*-
import re
import requests
import time
import operator
from fake_useragent import UserAgent

def check(func):
    def check_data(*args,**kwargs):
        request_data = func(*args,**kwargs)
        num = 0
        while not request_data and num < 3:
            request_data = func(*args,**kwargs)
            if request_data :
                break
            num += 1
        return request_data
    return check_data

@check
def request(param,tim):
    '''
    下载页面
    '''
    time.sleep(tim)

    try:
        url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/' + param
        # 伪装
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        res = requests.get(url,headers=headers)
        res.raise_for_status()
        #字符集编码
        res.encoding = res.apparent_encoding
        return res.text

    except :
        print('报错')
        time.sleep(3)
        return ''


def main():
    ############# 省 #############
    province_param = 'index.html'
    p_data = request(province_param,1)

    p_pattern = re.compile(r"<a href='([\s\S]*?)'>([\s\S]*?)<")
    r_province_list = re.findall(p_pattern, p_data)
    for province in r_province_list:

        province_id = province[0].split('.')[0]
        province_name = province[1]

        print(province_id,province_name)

        ############# 市 ############
        city_param = province[0]
        c_data = request(city_param,1)
        c_pattern = re.compile(r"<a[\s\S]*?>([\s\S]*?)</a></td><td>[\s\S]*?>([\s\S]*?)<")
        r_city_list = re.findall(c_pattern,c_data)
        for city in r_city_list:
            city_id = city[0]
            if city[1] == '市辖区':
                city_name = province_name
            else:
                city_name = city[1]

            print(city_id,city_name)

            ############ 区 ############
            # 获取区链接
            dirstrict_src = re.compile(r"<a href='([\s\S]*?)'>")
            dirstrict_param = re.search(dirstrict_src,c_data).groups()[0]
            #获取区数据
            d_data = request(dirstrict_param,2)
            d_pattern = re.compile(r"<a[\s\S]*?>([\s\S]*?)</a></td><td>[\s\S]*?>([\s\S]*?)<")
            r_dirstrict_list = re.findall(d_pattern,d_data)
            for dirstrict in r_dirstrict_list:

                dirstrict_id = dirstrict[0]
                dirstrict_name = dirstrict[1]

                print(dirstrict_id,dirstrict_name)

                #################### 街道 ##################
                # 获取街道链接
                street_src = re.compile(r"<a href='([\s\S]*?)'>")
                street_param = re.search(street_src,d_data).groups()[0]
                #获取街道数据
                s_data = request(province_id + '/' + street_param,2)
                s_pattern = re.compile(r"<a[\s\S]*?>([\s\S]*?)</a></td><td>[\s\S]*?>([\s\S]*?)<")
                r_street_list = re.findall(s_pattern,s_data)

                for street in r_street_list:
                    
                    street_id = street[0]
                    street_name = street[1]

                    print(street_id,street_name)
main()
