import datetime
import time
import os
import pymongo

EB_SERVERS = ['eb0:27000', 'eb1:27000', 'eb2:27000']

def get_db(host, db='untriggered'):
    # Handle MongoDB connections
    client = pymongo.MongoClient("mongodb://daq:%s@%s/admin" % (os.environ.get('MONGO_PASSWORD'), host))
    return client[db]

def get_daq_buffer_info():
    # This is needed for everything in the pipeline
    data = {'name' : 'daq_buffer',
            'time' : datetime.datetime.utcnow()}
    
    # Add whatever data you want here to this document, where these
    # values can be used by the frontend or alarms
    for eb in EB_SERVERS:
        data[eb] = get_db(eb).command({'dbstats': 1})
        
    # Give back
    return data

def db_size():
    # Establish connection to run database and pipeline collection.
    db = get_db(host='gw:27017', db='run')
    collection = db['pipeline_status']
    
    # Make it so documents expire after a certain amount of time
    collection.create_index("time", expireAfterSeconds=86400)
    
    # Add a latest value
    collection.insert(get_daq_buffer_info())
    print('Inserted...')
    
    return

while 1:

    db_size()

    time.sleep(60)
