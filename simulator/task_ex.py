#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import random
import time
import json

from config import TT, RANDOM_START, RANDOM_END, OUT_RANDOM_START, OUT_RANDOM_END

class FlightTask(object):

    def __init__(self):
        super(FlightTask, self).__init__()
        self.s = requests.Session()
        pass

    def _set_headers(self):
        '''set requests headers
        '''
        headers = {
           "Referer": "https://m.flight.qunar.com/ncs/page/flightlist?depCity=%E5%8C%97%E4%BA%AC&arrCity=%E9%B8%A1%E8%A5%BF&goDate=2018-02-09&from=touch_index_search",
           "Accept": "application/json, text/javascript",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "Cache-Control": "no-cache",
           "DNT": "1",
           "9bfe7a": "09ae65eba94109d2d271264bd9cb1f45",
           "Content-Type": "application/json",
           "Cookie": "QN99=7450; QN1=O5cv5VpqqYsz3+DmtfSxAg==; QunarGlobal=10.86.213.122_-eeec6ac_16130a46afa_-6995|1516939661665; QN205=auto_4e0d874a; QN277=auto_4e0d874a; csrfToken=kNeEHPNIn3nyiEpMSMZVJl3NmZZkVo1e; _i=RBTjeTIL-ybQujrR6qRnvZ5A18Mx; _vi=LWDjfPALIm1R4WVvH_GBGGJIkkKF0sbeOvCFD0vLTwO1OxZgfRjPjJMfcc4hqFFhpdvKgyEfSvHTKO_pB5U3v0NYTSrk55iq8J24OggvfhJY0g9zlWPw7puqI_1-0N5ereSlER9JTgcWov33N-ojZYAJaKxnBgwbx8UtXnXcsSRk; QN601=16b95bb32b57b8dd5858a7de38f01859; QN269=6AB43ED000DD11E8A409FA163E9DCB6D; QN163=0; QN6=auto_4e0d874a; Hm_lvt_75154a8409c0f82ecd97d538ff0ab3f3=1516939664; Hm_lpvt_75154a8409c0f82ecd97d538ff0ab3f3=1516939664; QN48=tc_cc1f1459ed14ac2b_16130a65ac3_dfd7; QN66=3w; QN300=3w; _RF1=1.119.145.46; _RSG=AZq_ey7.GY4oAiV7hUt5VB; _RDG=2827d04daadc3a22ef27b93d5dde990c95; _RGUID=4890f87f-28ff-48ca-b7c5-ddeac77ec2b2; QN667=C; QN668=51%2C55%2C51%2C56%2C59%2C53%2C59%2C57%2C57%2C57%2C51%2C56%2C56; QN621=fr%3Dtouch_index; F235=1516939834554",
        }
        return headers

    def _set_request(self):
        self.s.headers = self._set_headers()

    def _get_flight_list(self):
        '''get flight list

        return [{},{},...]
        '''
        __url_domain = self._domain()
        __data = self._format_params()
        __url = __url_domain + u"/touch/api/domestic/flightlist"
        resp = self.s.post(__url, __data)
        result = json.loads(resp.text)
        if result != 0:
            terminate(result)
        return result

    def terminate(self, reuslt):
        print json.dumps(result, ensure_ascii=False, indent=4)
        raise Excetption()

    def _format_params(self):
        '''format flight params
        '''
        timestamp = int(round(time.time() * 1000))
        _data = {
            "arrCity": self.params['GO_CITY'].encode('utf8'),
            "depCity": self.params['FROM_CITY'].encode('utf8'),
            "from": u"touch_index_search",
            "goDate": self.params['GO_DATE'],
            "firstRequest": "true",
            "startNum": 0,
            "sort": 5,
            "r": timestamp,
        }
        return _data

    def _domain(self):
        '''set main domain
        '''
        __url_domain = u'https://m.flight.qunar.com'
        return __url_domain

    def __format_results(self, lists):
        '''format output result for E-mail

        lists: [{},{},...]

        return str
        '''
        self._flights = self.__format_flights(lists)
        self._trends = self.__format_goFTrend(lists)

    def __deal_flights(self):
        flights = self._flights
        trends = self._trends
        min_price = 0
        _msg = []
        for f in flights:
            _min_price = f['minBarePrice']
            if min_price == 0 or _min_price < min_price:
                min_price = _min_price
                if min_price <= self.params['APPOINT_PRICE']:
                    _msg.append(_msg)

        flights_info = self._extract_flights_info(_msg)
        trends_info = self._extract_trends_info(_msg)
        return flights_info, trends_info

    def _extract_trends_info(self, trends):
        go_date = self.params['GO_DATE']
        flag = ''

        for i,t in enumerate(trends):
            if t['date'] == go_date:
                flag = i

        trends_slice = trends[flag-2: flag+2]
        res = _is_quality(trends_slice)
        return res

    def _is_quality(self, trends):
        res = []
        for i in trends:
            if i['price'] <= self.params['APPOINT_PRICE']:
                res.append(i)
        return res
        
    def _extract_flights_info(self, msg):
        _res = []
        for m in msg:
            _res.append({
                u'最低票价': m['minBarePrice'],
                u'航班号': m['code'],
            })
        return _res

    def __format_flights(self, lists):
        flights = lists['data']['flights']
        return flights 

    def __format_goFTrend(self, lists):
        trends = lists['data']['trendPrice']['goFTrend']
        return trends

    def __send_email(self, results):
        '''send E-mail to me 

        results: str

        return 0 or 1
        '''
        raise NotImplementedError()

    def __request(self, params):
        self.params = params
        _flight_list = self._get_flight_list()
        self.__format_resutls(_flight_list)
        results = __deal_flights()
        if results[1]:
            resp = self.__send_email(results)
        print u"执行结束， 结果：{}".format(resp)

    def _in_sl_tim(self):
        sl_tim = random.randrange(RANDOM_START, RANDOM_END, _int=float)
        print u"内间隔时间为: {}".format(sl_tim)
        time.sleep(sl_tim)

    def out_sl_tim(self):
        sl_tim = random.randrange(OUT_RANDOM_START, OUT_RANDOM_END, _int=float)
        print u"外间隔时间为: {}".format(sl_tim)
        time.sleep(sl_tim)

    def entry(self):
        for i in TT:
            self._in_sl_tim()
            self.__request(i)
            

if __name__ == '__main__':
    try:
        while 1:
            ft = FlightTask()
            ft.entry()
            ft.out_sl_tim()
    except:
        pass

