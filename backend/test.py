import pymongo

myclient = pymongo.MongoClient("mongodb+srv://jamesMongo:0Az82U28n2WyxNl5@clusterj.z7twq.mongodb.net/?retryWrites=true&w=majority")
# print(myclient.list_database_names())

mydb = myclient["sample_analytics"]

# print(mydb.list_collection_names())

mycol = mydb['accounts']

print(mycol.find_one())