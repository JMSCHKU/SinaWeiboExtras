#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import time
import datetime
import json

if len(sys.argv) < 2:
    print "missing arguments: [file] [date start] [date end]"
    sys.exit()
if len(sys.argv) == 3:
    datestart = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d %H:%M")
    dateend = datetime.datetime.now()
elif len(sys.argv) >= 4:
    datestart = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d %H:%M")
    dateend = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d %H:%M")
else:
    datestart = datetime.datetime.now() - datetime.timedelta(hours=24)
    dateend = datetime.datetime.now()

f = open(sys.argv[1], "r")

j = json.loads(f.read())

out = dict()
out["hits"] = list()
for line in j["hits"]:
    created_at = datetime.datetime.strptime(line["created_at"], "%Y-%m-%d %H:%M:%S")
    if created_at >= datestart and created_at < dateend:
        out["hits"].append(line)

out["query_finished"] = j["query_finished"]
out["dateend"] = j["dateend"]
out["generated"] = int(time.time() * 1000)

print json.dumps(out)
