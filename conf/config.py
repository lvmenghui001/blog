#!/usr/bin/env python3

HOST = '0.0.0.0'
PORT = 8500

TAG_CACHE_EXPIRE = 3600 * 24
LOGGING = './conf/log.conf'

DATABASE = {
    "blog": "mysql://root:654321@localhost:3306/blog"
}
