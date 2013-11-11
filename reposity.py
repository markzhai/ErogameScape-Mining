#!/usr/bin/python
"""
Defines reposity functions.
"""

import redis
import itertools

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def save_game_info(game_id, title, brand_id):
  r.hmset('game:%s' % game_id, {'title':title, 'brand_id':brand_id})

def save_game_pov(game_id, *args):
  pipe = r.pipeline() 
  for i in range(0, len(args), 2):
    pipe.sadd('%s:pov' % game_id, args[i])
    pipe.hset('game:%s' % game_id, 'pov%s' % args[i], args[i+1])
  pipe.execute()

def save_brand(id, name):
  r.setnx('brand:%s' % id, name)

def get_game_pov(game_id):
  return r.smembers('%s:pov' % game_id)

def get_game_pov_cnt(game_id, pov_id):
  return r.hget('game:%s' % game_id, 'pov%s' % pov_id)

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

save_game_info(0, 'true tears', 0)
save_game_pov(0, '52', 1, '36', 222)
save_brand(0, 'key')
print(get_game_pov(0))
print(get_game_pov_cnt(0, 36))