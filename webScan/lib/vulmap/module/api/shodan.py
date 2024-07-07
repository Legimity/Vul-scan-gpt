#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import shodan
from lib.vulmap.thirdparty import shodan
import json
import base64
from lib.vulmap.module.color import color
from lib.vulmap.module.time import now
from lib.vulmap.module import globals


def shodan_api(shodan_keyword):
    try:
        shodan_key = globals.get_value("shodan_key")
        api = shodan.Shodan(shodan_key)
        res = api.search(shodan_keyword)
        shodan_target = []
        for result in res['matches']:
            shodan_target.append("%s:%s" % (result['ip_str'], result['port']))
        return shodan_target
    except shodan_key.APIError as e:
        print(now.timed(de=0) + color.red_warn() + color.red(" Shodan api: " + str(e)))
        exit(0)