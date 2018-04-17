# require the driver package
from pymongo import MongoClient
from pprint import pprint

# Create a client
# client = ...


# I imported movies.bson into database named hw3 and collection named movies
client = MongoClient()
db = client.hw3
movies = db.movies

# A. Update all movies with "NOT RATED" at the "rated" key to be "Pending rating". The operation must be in-place and atomic.
movies.update_many({"rated":"NOT RATED"}, {"$set":{"rated":"Pending rating"}})

# B. Find a movie with your genre in imdb and insert it into your database with the fields listed in the hw description.
movies.insert(
   {"title" : "Game Night",
    "year" : 2018,
    "countries" : [
             "USA"
    ],
    "genres" : [
             "Comedy",
             "Crime",
             "Mystery",
             "Thriller"
    ],
    "directors" : [
             "Roar Uthaug"
    ],
    "imdb" : {
             "rating" : 7.4,
             "votes" : 27459,
             "id" : 2704998
    },
    })

# C. Use the aggregation framework to find the total number of movies in your genre.

# Example result:
#  => [{"_id"=>"Comedy", "count"=>14046}]
pipeline_c = [
	{"$unwind" : "$genres"},
	{"$match" : {"genres" : "Comedy"}},
	{"$count" : "count"},
	{"$project" : {"_id" : "Comedy", "count": 1} }
]

res_c = movies.aggregate(pipeline_c)
print("Result for part C: ")
pprint(list(res_c))
print("")

# D. Use the aggregation framework to find the number of movies made in the country you were born in with a rating of "Pending rating".

# Example result when country is Hungary:
#  => [{"_id"=>{"country"=>"Hungary", "rating"=>"Pending rating"}, "count"=>9}]

pipeline_d = [
	{"$unwind" : "$countries"},
	{"$match" : {"countries" : "China", "rated" : "Pending rating"}},
	{"$count" : "count"},
	{"$project" : {"_id" : {"country" : "China", "rating" : "Pending rating"}, "count": 1} }
]
res_d = movies.aggregate(pipeline_d)
print("Result for part D: ")
pprint(list(res_d))
print("")
#413 24

# E. Create an example using the $lookup pipeline operator. See hw description for more info.

db.students.insert_many([
   { "sname" : "Chang Liu", "age" : 21, "school" : "SEAS", "country" : "China" },
   { "sname" : "Biqing Qiu", "age" : 22, "school" : "SEAS", "country" : "Singapore" },
   { "sname" : "Vivian Han", "age" : 21, "school" : "Barnard", "country" : "South Korea" },
   { "sname" : "Lillian Wang", "age" : 21, "school" : "CC", "country" : "USA" }
])

db.products.insert_many([
   { "name" : "Chang Liu", "phone" : "iPhone 6", "laptop" : "Mac Pro"},
   { "name" : "Biqing Qiu", "phone" : "SAMSUNG Galaxy", "laptop" : "Mac Basic"},
   { "name" : "Vivian Han", "phone" : "iPhone X", "laptop" : "Lenovo"},
   { "name" : "Lillian Wang", "phone" : "iPhone 8", "laptop" : "Dell"}
])

pipeline_e = [
	{'$lookup': 
                {'from' : 'products',
                 'localField' : 'sname',
                 'foreignField' : 'name',
                 'as' : 'electronics'}},
    {"$project" : {"_id" : 0} }
]
res_e = db.students.aggregate(pipeline_e)
print("Result for part E - students and their electronics: ")
pprint(list(res_e))






















