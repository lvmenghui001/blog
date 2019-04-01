import sys
import json
import copy
import time
import random
import logging
from hashlib import sha1
from copy import deepcopy
from datetime import datetime
from flask import request
from flask import jsonify
from flask import Blueprint
from flask import redirect
from flask import session
from flask import url_for
from flask import render_template
from .send_message import *
from src.models.models import db
from src.models.models import *



# mongo1 = PyMongo(app, uri = CONFIG.DATABASE["tag"])
# memcache = SimpleCache(default_timeout=CONFIG.TAG_CACHE_EXPIRE)
# tagger = utils.Tagger(mongo1, memcache)
# mongo2 = PyMongo(app, uri = CONFIG.DATABASE["offer"])
# toaddrs = ["yangqiao.wu@mobvista.com"]
