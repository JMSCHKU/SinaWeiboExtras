#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import time
import json

if len(sys.argv) < 2:
    print "missing arguments: [file] "
    sys.exit()

f = open(sys.argv[1], "r")

j = json.loads(f.read())

ids = set()
for line in j["hits"]:
    l = line["text"].encode("utf8")
    if "//" in l:
        foo = l.split("//")[0]
        index = 1
        while foo.endswith("http:"):
            index += 1
            foo = "//".join(l.split("//")[0:index])
        l = foo
    if "[" in l:
        l = re.sub(r'\[[^\[\]]+\]', '', l)
    if len(l.strip()) > 0:
        print l
    ids.add(line["status_id"])

for line in j["hits"]:
    if line["retweeted_status"] is not None and line["rt_text"] is not None and line["retweeted_status"] not in ids:
        l = line["rt_text"].encode("utf8")
        if "//" in l:
            foo = l.split("//")[0]
            index = 1
            while foo.endswith("http:"):
                index += 1
                foo = "//".join(l.split("//")[0:index])
            l = foo
        if "[" in l:
            l = re.sub(r'\[[^\[\]]+\]', '', l)
        if len(l.strip()) > 0:
            print l
        ids.add(line["retweeted_status"])
