#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import datetime
import json
import urllib
import httplib
import socket

translate_api_url = "/language/translate/v2"
host = "www.googleapis.com"

data = { "key": "AIzaSyA5J1NTl9WlG3R5UbnIzxebCKUM8Jnk0mU", "target": "en" }

if len(sys.argv) < 2:
    print "missing arguments: [json file to add translations]"
    sys.exit()

cutoff = datetime.datetime.now() - datetime.timedelta(hours=24) # only translate 6 hours or newer

f = open(sys.argv[1], "r")

# ugly hack to force IPV4 from http://stackoverflow.com/questions/2014534/force-python-mechanize-urllib2-to-only-use-a-requests/6319043#6319043
#sock = socket.socket(socket.AF_INET)
origGetAddrInfo = socket.getaddrinfo
def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)
socket.getaddrinfo = getAddrInfoWrapper

js = json.loads(f.read())
for hit in js["hits"]:
    data["q"] = ""
    try:
        created_at = datetime.datetime.strptime(hit["created_at"], "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        continue
    if created_at < cutoff:
        break
    if "text_en" not in hit and hit["retweeted_status"] is None:
        #continue # testing
        try:
            data["q"] = hit["text"].encode("utf8")
            url = (translate_api_url + "?%s") % urllib.urlencode(data)
            #resp, content = http.request(url, "GET")
            h = httplib.HTTPSConnection(host)
            h.request("GET", url)
            resp = h.getresponse()
            jsResp = json.loads(resp.read())
            translatedText = jsResp["data"]["translations"][0]["translatedText"]
            if len(translatedText) > 0:
                hit["text_en"] = translatedText
        except Exception as e:
            #print e.message
            continue

print json.dumps(js)
