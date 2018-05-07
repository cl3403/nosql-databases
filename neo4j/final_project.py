# Put the use case you chose here. Then justify your database choice:
#
# I chose to do the Instagram-like app where users can share photos & videos, leave comments under photos & videos,
# send messages to other users, get system notifications, add stories, and make collections of photos & videos. 
# I chose neo4j because there are so many entities and relationship in this app and using a graph database allows
# me to query subgraphs very easily (easy retrieval). For example, if I wanna know all the followers of a user, 
# that can be easily done by matching a FOLLOW relationship to that user. Because there are many such subgraphs 
# that will be useful, such as a user's followers, a user's photos, a user's messages, etc. it makes sense to 
# use a graph database. In addition, because data are connected in graph database, it also represents the high
# connectivity of this app very well.
#


# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# 
# Neo4j is a highly available database so we can take full advantage of that. We can set up the cluster so that
# there is a single master instance and several slave instances and all instances in the cluster have full copies
# of the data in their local database files. When one server goes down, the other instances will detect that and 
# mark it as failed and this failed server will catch up with the cluster once it becomes available again. If this
# failed server is the master, another member in the cluster will be elected and its role will be switched from 
# a slave to the new master.


# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# 
# In my app, the most important data are user accounts, photos and videos users post, and their collections of 
# photos and videos. Those are most important because the main purpose of this app is for users to share their
# photos and videos. Comments and messages are important too because they represent communications between users
# which is also promised by this app. It might be okay to lose a small portion of stories especially after 24
# hours because the stories can only be viewed by other users within 24 hours. It is okay to lose some notifications
# because users do not care that much about those notifications compared to other components of this app. To mitigate
# the risk of lost data, first of all I can always try to do atomic operations and transactions to minimize the chances
# of operations and transactions being interrupted. In addition, I would also configure the database setup so that 
# the updates to slaves are consistent immediately, in other words, a transaction will be forced to be unsuccessful
# if the update push from the master to slaves fails. In this way, I can ensure that master is always consistent with
# all the slaves and when master goes down, every slave has the same data. 
#

from neo4j.v1 import GraphDatabase
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

with driver.session() as session:
	with session.begin_transaction() as tx:



# Action 1: A user signs up for an account 
		tx.run("CREATE (vivian:User "
			   "{ username: 'Vivian', password: 'vv2562', bio: 'I am new to this app and I am excited!'})")

# Action 2: A user follows another user 
		tx.run("MATCH (a:User), (b:User) "
			   "WHERE a.username = 'Vivian' AND b.username = 'Chang' "
			   "CREATE (a)-[r:FOLLOW]->(b) "
			   "RETURN type(r)")

# Action 3: A user likes another user's photo
		tx.run("MATCH (a:User), (b:Photo) "
			   "WHERE a.username = 'Vivian' AND b.photo_id = 1 "
			   "CREATE (a)-[r:LIKE]->(b) "
			   "RETURN type(r)")
		tx.run("MATCH (n:Photo { photo_id: 1 })"
			   "SET n.likes = n.likes + 1")

# Action 4: A user comments on another user's video
		tx.run("CREATE (comment3:Comment "
			   "{ comment_id: 3, date: 20180505, likes: 0, content: 'I love this video!!'})")

		tx.run("MATCH (a:User), (b:Comment) "
			   "WHERE a.username = 'Vivian' AND b.comment_id = 3 "
			   "CREATE (a)-[r:WRITE]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (a:Comment), (b:Video) "
			   "WHERE a.comment_id = 3 AND b.video_id = 1 "
			   "CREATE (a)-[r:BELONG_TO]->(b) "
			   "RETURN type(r)")


# Action 5: A user posts a new photo 
		tx.run("CREATE (photo3:Photo { photo_id: 4, date: 20170505, likes: 0})")

		tx.run("MATCH (a:User), (b:Photo) "
			   "WHERE a.username = 'Vivian' AND b.photo_id = 4 "
			   "CREATE (a)-[r:POST]->(b) "
			   "RETURN type(r)")


# Action 6: Another user likes a user's photo and a notification is sent to this user 
		tx.run("MATCH (a:User), (b:Photo) "
			   "WHERE a.username = 'Lillian' AND b.photo_id = 4 "
			   "CREATE (a)-[r:LIKE]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (n:Photo { photo_id: 4 })"
			   "SET n.likes = n.likes + 1")

		tx.run("CREATE (notification3:Notification { n_id: 3, date: 20180505, notice: 'Lillian liked your post!'})")

		tx.run("MATCH (a:User), (b:Notification) "
			   "WHERE a.username = 'Vivian' AND b.n_id = 3 "
			   "CREATE (a)-[r:GET]->(b) "
			   "RETURN type(r)")


# Action 7: A user sends a message to another user and receives a reply 
		tx.run("CREATE (message3:Message { message_id: 3, date: 20180505, content: 'I love your photos!!'})")
		tx.run("CREATE (message4:Message { message_id: 4, date: 20180505, content: 'Glad you like them!'})")

		tx.run("MATCH (a:User), (b:Message) "
			   "WHERE a.username = 'Vivian' AND b.message_id = 3 "
			   "CREATE (a)-[r:SEND]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (a:User), (b:Message) "
			   "WHERE a.username = 'Chang' AND b.message_id = 3 "
			   "CREATE (a)-[r:RECEIVE]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (a:User), (b:Message) "
			   "WHERE a.username = 'Chang' AND b.message_id = 4 "
			   "CREATE (a)-[r:SEND]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (a:User), (b:Message) "
			   "WHERE a.username = 'Vivian' AND b.message_id = 4 "
			   "CREATE (a)-[r:RECEIVE]->(b) "
			   "RETURN type(r)")


# Action 8: A user adds a new story of their day 
		tx.run("CREATE (story3:Story { story_id: 3, date: 20180505, watches: 0})")

		tx.run("MATCH (a:User), (b:Story)"
			   "WHERE a.username = 'Vivian' AND b.story_id = 3 "
			   "CREATE (a)-[r:ADD]->(b) "
			   "RETURN type(r)")

# Action 9: A user makes a new collection of photos they like 
		tx.run("CREATE (collection3:Collection { c_id: 3, date: 20180505})")

		tx.run("MATCH (a:User), (b:Collection)"
			   "WHERE a.username = 'Vivian' AND b.c_id = 3 "
			   "CREATE (a)-[r:SAVE]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (a:Photo), (b:Collection)"
			   "WHERE a.photo_id = 1 AND b.c_id = 3 "
			   "CREATE (a)-[r:IN]->(b) "
			   "RETURN type(r)")

		tx.run("MATCH (a:Video), (b:Collection)"
			   "WHERE a.video_id = 1 AND b.c_id = 3 "
			   "CREATE (a)-[r:IN]->(b) "
			   "RETURN type(r)")










