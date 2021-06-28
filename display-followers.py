#!/usr/bin/env python3

import json
import pprint
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
pp = pprint.PrettyPrinter(indent=4)

for key in r.scan_iter():
    values = json.loads(r.get(key))
    if values['verified']:
        print(key.decode("utf-8"), end=' '),
        print(values['followers_count'], end=' ')
        print(values['friends_count'])
