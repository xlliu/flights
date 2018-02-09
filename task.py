#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Task(object):

    def __init__(self):
        pass

    def __set_headers(self):
        '''set requests headers
        '''
        raise NotImplementedError()

    def _get_flight_list(self):
        '''get flight list

        return [{},{},...]
        '''
        raise NotImplementedError()

    def _format_params(self):
        '''format flight params
        '''
        raise NotImplementedError()

    def _domain(self):
        '''set main domain
        '''
        raise NotImplementedError()

    def __format_results(self, lists):
        '''format output result for E-mail

        lists: [{},{},...]

        return str
        '''
        raise NotImplementedError()

    def __send_email(self, results):
        '''send E-mail to me 

        results: str

        return 0 or 1
        '''
        raise NotImplementedError()

    def _set_request(self):
        raise NotImplementedError()

    def __request(self):
        _air_list = self._get_flight_list()
        results = self.__format_resutls(_air_list)
        resp = self.__send_email(results)
        print u"执行结束， 结果：{}".format(resp)
