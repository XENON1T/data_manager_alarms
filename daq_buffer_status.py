import datetime
import time
import os
import pymongo

EB_SERVERS = ['eb0:27000', 'eb1:27000', 'eb2:27000']

def get_db(host, db='untriggered'):
    client = pymongo.MongoClient("mongodb://daq:%s@%s/admin" % (os.environ.get('MONGO_PASSWORD'), host))
    return client[db]

def get_daq_buffer_info():
    data = {'name' : 'daq_buffer',
            'time' : datetime.datetime.utcnow()}
    for eb in EB_SERVERS:
        data[eb] = get_db(eb).command({'dbstats': 1})
    return data

def db_size():
    db = get_db(host='gw:27017', db='run')
    collection = db['pipeline_status']
    collection.create_index("time", expireAfterSeconds=86400)
    collection.insert(get_daq_buffer_info())
    print('Inserted...')
    return

while 1:

    db_size()

    time.sleep(60)
