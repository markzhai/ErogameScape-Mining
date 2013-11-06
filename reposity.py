# reposity-redis.py
"""Defines reposity functions."""

import redis
import itertools

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def save_game(id, title):
	#set(self, name, value, ex=None, px=None, nx=False, xx=False)
	r.set(id, title, None, None, True, False)

def map_reduce(i,mapper,reducer):
  intermediate = []
  for (key,value) in i.items():
    intermediate.extend(mapper(key,value))
  groups = {}
  for key, group in itertools.groupby(sorted(intermediate),
                                      lambda x: x[0]):
    groups[key] = list([y for x, y in group])
  return [reducer(intermediate_key,groups[intermediate_key])
          for intermediate_key in groups]
