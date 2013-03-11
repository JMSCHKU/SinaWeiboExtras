#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import json

if len(sys.argv) < 2:
    print "missing arguments: [file master] [file with updated data]"
    sys.exit()

f_orig = open(sys.argv[1], "r")
f_new = open(sys.argv[2], "r")

orig = json.loads(f_orig.read())
new = json.loads(f_new.read())

for newhit in new["hits"]:
    found = False
    for orighit in orig["hits"]:
        if orighit["status_id"] == newhit["status_id"]:
            orighit = newhit
            found = True
            break
    if not found:
        orig["hits"].append(newhit)

out = dict()
out["hits"] = sorted(orig["hits"], key=lambda x: x["created_at"], reverse=True)
out["query_finished"] = new["query_finished"]
out["dateend"] = new["dateend"]
if out["dateend"] < 10000000000:
    out["dateend"] *= 1000
out["datestart"] = int(time.mktime(time.strptime(out["hits"][len(out["hits"])-1]["created_at"], "%Y-%m-%d %H:%M:%S")) * 1000)
out["generated"] = int(time.time() * 1000)

print json.dumps(out)
