# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-10-16
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

import pymongo

'''
http://www.runoob.com/python3/python-mongodb.html   MONGDB操作方法网址
'''

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["sites"]

mylist = [
    {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
    {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
    {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
    {"name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
    {"name": "Github", "alexa": "109", "url": "https://www.github.com"}
]

action_items = ['add', 'print', 'delete', 'delete_all', 'modify', 'sort']
action = action_items[1]

if action == 'add':
    # mycol.drop()
    x = mycol.insert_many(mylist)

    # 输出插入的所有文档对应的 _id 值
    # print(x.inserted_ids)

elif action =='print':
    #########################################################################
    for y in mycol.find():
        print y
    #########################################################################
    myquery = {"name": "Taobao"}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)
    #######################0 will not display, 1 will showing up#############
    for x in mycol.find({},{ "_id": 0, "name": 1, "alexa": 1, "url": 1 }):
        for key, value in x.items():
            print "key is: %s, value is: %s"%(key, value)
    #########################################################################
    myresult = mycol.find().limit(3)
    # 输出结果
    for x in myresult:
        print(x)
    #########################################################################
    myquery = {"name": {"$regex": "^R"}}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)
    #########################################################################
    myquery = {"name": {"$gt": "H"}}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)

elif action == 'delete':
    myquery = {"name": "Taobao"}
    mycol.delete_one(myquery)
    # 删除后输出
    for x in mycol.find():
        print(x)

    myquery = {"name": {"$regex": "^F"}}
    x = mycol.delete_many(myquery)
    print(x.deleted_count, "个文档已删除")

elif action == 'delete_all':
    mycol.drop()

elif action == 'modify':
    myquery = {"alexa": "10000"}
    newvalues = {"$set": {"alexa": "12345"}}
    mycol.update_one(myquery, newvalues)
    # 输出修改后的  "sites"  集合
    for x in mycol.find():
        print(x)

    myquery = {"name": {"$regex": "^F"}}
    newvalues = {"$set": {"alexa": "123"}}
    x = mycol.update_many(myquery, newvalues)
    print(x.modified_count, "文档已修改")

elif action == 'sort':
    mydoc = mycol.find().sort("alexa", -1)
    for x in mydoc:
        print(x)