#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016-2017 7x24hs.com
# thomas@7x24hs.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.web
import logging
import time
import sys
import os
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

from comm import *
from global_const import *
from base_handler import *
from dao import contact_message_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger


@swagger.model()
class MessageReq:
    def __init__(self, email, content):
        self.email = email
        self.content = content


# /contact/api/message
class ApiContactMessageXHR(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    @swagger.operation(nickname='post')
    def post(self):
        """
            @description: 生成联系信息

            @param body:
            @type body: C{MessageReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.info("POST %r", self.request.uri)
        logging.debug("body %r", self.request.body)

        message = None
        try:
            # data={'email':'', 'content':''}
            message = json_decode(self.request.body)
            message["email"]
            message["content"]
        except:
            logging.warn("Bad Request[400]: add contact message=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        timestamp = current_timestamp()
        _id = generate_uuid_str()
        yield contact_dao.contact_dao().insert(_id, message["email"], message["content"], timestamp)

        logging.info("Success[200]: create contact=[%r]", message)
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
        self.finish()
        return


    @tornado.gen.coroutine
    @swagger.operation(nickname='get')
    def get(self):
        """
            @description: 分页查询app客户端

            @param page: default=1
            @type page: L{int}
            @in page: query
            @required page: False

            @param limit: default=20
            @type limit: L{int}
            @in limit: query
            @required limit: False

            @rtype: L{MessageResp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.info("GET %r", self.request.uri)

        page = self.get_argument("page", 1)
        logging.debug("get page=[%r] from argument", page)
        limit = self.get_argument("limit", 20)
        logging.debug("get limit=[%r] from argument", limit)

        idx = (int(page) - 1) * int(limit)
        total_num = 0
        total_page = 0

        messages = yield contact_dao.contact_dao().find_pagination(idx, limit)
        total_num = yield contact_dao.contact_dao().count_pagination(idx, limit)

        if total_num % int(limit) == 0:
            total_page = int(total_num / int(limit))
        else:
            total_page = int(total_num / int(limit)) + 1
        rs = {"page":page, "total_page":total_page, "data":messages}

        logging.info("OK(200): query messages: page=[%r] total_page=[%r] num=[%r]", page, total_page, len(messages))
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":rs}))
        self.finish()
        return
