ErogameScape-Mining
===================

A spider and data-mining project on ErogameScape

Redis
-----
How data stores in redis:

1. Hash - game:id -> game_title, brand_id

		HMSET game:16506 title この大空に、翼をひろげて brand_id 689
		HGETALL game:16506
		HEXISTS game:16506 title

3. String - brand:id -> brand_name

		SET brand:689 PULLTOP
		
4. Hash - uid:game_id

		HMSET comment:yamadayo:7062 score 65 playtime 30h date 2013年11月04日02時13分14秒 comment "個別が鈴√と来ヶ谷以外全く面白くない" netabare 1

5. Set - games, users

		SADD games "16506"
		SMEMBERS games
		
		SADD users "yamadayo" "christia"
		SMEMBERS users
		
		SADD brands 689
		
		SADD yamadayo:games 16506

6. List - user:games

		LPUSH new_commented:games 16506

Spider
------
erogame.py

To set up other 

Versioning
----------
At version 0.0.1.
