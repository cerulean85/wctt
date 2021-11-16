# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session
#
# engine = sqlalchemy.create_engine("mariadb+mariadbconnector://tester:123456@localhost:3306/whateverdot")
# Base = declarative_base()
#
#
# class Test(Base):
#     __tablename__ = "test"
#     d1 = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     d2 = sqlalchemy.Column(sqlalchemy.Float)
#     d3 = sqlalchemy.Column(sqlalchemy.String(length=100))
#     d4 = sqlalchemy.Column(sqlalchemy.DateTime)
#
# Session = sqlalchemy.orm.sessionmaker()
# Session.configure(bind=engine)
# session = Session()
#
# test_list = session.query(Test).all()
# for test in test_list:
#     print("{} {} {}".format(test.d1, test.d2, test.d3, test.d4))
#
#
# # https://mariadb.com/ko/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/

## object {"work.channel": "jna"} 이런 식으로.

# from pymongo import MongoClient
# from pymongo.cursor import CursorType
import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db_conn_info = {
    "user": "root",
    "password": "123456",
    "host": "localhost",
    "port": 3306,
    "database": "whateverdot"
}

db_url = f"mysql+pymysql://{db_conn_info['user']}:{db_conn_info['password']}@" \
         f"{db_conn_info['host']}:{db_conn_info['port']}/{db_conn_info['database']}?charset=utf8"

db_url = 'sqlite:///../jcoty.db'


Base = declarative_base()
class WorkGroups(Base):
    __tablename__ = "work_groups"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text, nullable=False)
    channels = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Text, nullable=True)
    # start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.Text, nullable=True)
    # end_date = db.Column(db.DateTime, nullable=True)
    work_state = db.Column(db.Text, nullable=True)
    update_time = db.Column(db.Text, nullable=True)
    # update_time = db.Column(db.DateTime, nullable=True)
    report = db.Column(db.Text, nullable=True)
    data_directory = db.Column(db.Text, nullable=True)
    proj_directory = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Integer, nullable=True, default=0)


engine = db.create_engine(db_url)
session = Session(engine, future=True)
conn = engine.connect()
metadata = db.MetaData()
table = db.Table('work_groups', metadata, autoload=True, autoload_with=engine)

# session.query(WorkGroups) \
#     .filter(WorkGroups.id == 19) \
#     .update({WorkGroups.work_state: "working"})
# session.commit()
# SELECT!!
# work_group_list = session.query(WorkGroups).filter(WorkGroups.work_state == 'waiting').all()






# query = db.select([table]).where(table.columns.work_state == 'waiting')
# print(query)
# work_groups = WorkGroups.query.filter_by(work_state='waiting')
# print(work_groups)
# db
# work_group_list = session.query(WorkGroups).filter(WorkGroups.work_state == 'attached').all()
# work_group_list = session.query(WorkGroups).filter(WorkGroups.work_state == 'waiting').all()
# print(work_group_list[0].id)
# result_proxy = conn.execute(query)
# result_set = result_proxy.fetchall()
# print(result_set)
# session.query(WorkGroups).filter(WorkGroups.work_state == 'waiting').update({WorkGroups.report: "QWFQWF"})
# work_group = work_group_list[0]
# # work_group.report = "good!!"
# session.commit()
# print(work_group.id)

# session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# base = declarative_base()
# base.query = session.query_property()
# base.metadata.create_all(engine)


# class DBHandler:
#     def __init__(self):
#         host = "localhost"
#         port = "27017"
#         self.client = MongoClient(host, int(port))
#
#     def map_reduce(self, channel, reduce_value, db_name=None, collection_name=None):
#         map = "function() { emit(this." + reduce_value + ", 1); }"
#         reduce = "function(key, values) { return Array.sum(values) }"
#         out = "frequency_" + reduce_value + '_' + channel
#         query = {"channel": channel}
#         self.client[db_name][collection_name].map_reduce(map, reduce, out, query=query)
#
#     def insert_item_one(self, data, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].insert_one(data).inserted_id
#         return result
#
#     def insert_item_many(self, datas, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].insert_many(datas).inserted_ids
#         return result
#
#     def insert_urls(self, urls, work):
#         data_list = []
#         for url in urls:
#             data_list.append({
#                 "url": url,
#                 "work": work,
#                 "save_path": ''
#             })
#         self.insert_item_many(data_list, db_name="whateverdot", collection_name="urls")
#
#
#     def find_item_one(self, condition=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].find_one(condition, {"_id": False})
#         return result
#
#     def find_item(self, condition=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].find(condition, {"_id": False}, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
#         return result
#
#     def delete_item_one(self, condition=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].delete_one(condition)
#         return result
#
#     def delete_item_many(self, condition=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].delete_many(condition)
#         return result
#
#     def update_item_one(self, condition=None, update_value=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].update_one(filter=condition, update=update_value)
#         return result
#
#     def update_item_many(self, condition=None, update_value=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].update_many(filter=condition, update=update_value)
#         return result
#
#     def text_search(self, text=None, db_name=None, collection_name=None):
#         result = self.client[db_name][collection_name].find({"text": text})
#         return result



# dbh = DBHandler()
# dbh.map_reduce("nav", "text", db_name="whateverdot", collection_name="docs")
# dbh.update_item_many({"work.work_group_no": "12", "work.work_no": "100"}, { "$set": {"save_path": ""}}, "whateverdot", "urls")
# result = dbh.find_item({"work.work_group_no": "12", "work.work_no": "100"},
#                       db_name="whateverdot", collection_name="urls")
#
# for item in result:
#     print(item["url"])
# dbh.delete_item_many({"work.channel": "jna"}, db_name="whateverdot", collection_name="docs")
# dbh.delete_item_many({}, db_name="whateverdot", collection_name="docs")
# dbh.delete_item_many({}, db_name="whateverdot", collection_name="urls")
# # dbh.insert_item_many([{"text": "Hello Python1"}, {"text": "Hello Python2"}], "test", "xx")
# result = dbh.text_search("Hello Python1", "test", "xx")
# for x in result:
#     print(x)

# result = dbh.find_item(None, "test", "xx")
# print(result)
# for list in result:
# 	print(list)

# insert_item_one(mongo, {"text": "Hello Python"}, "test", "test")
# cursor = find_item(mongo, None, "test", "test")
# for list in cursor:
#     print(list["text"])
#
# delete_item_one(mongo, {"text": "Hello Python"}, "test", "test")
# cursor = find_item(mongo, None, "test", "test")
# for list in cursor:
#     print(list["text"])