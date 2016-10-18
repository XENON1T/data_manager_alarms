from pagerduty_api import Alert
import subprocess
import os
import sys
import time
import pymongo

EB_SERVERS = ['eb0', 'eb1', 'eb2']

def get_db(host, db='untriggered'):
    client = pymongo.MongoClient("mongodb://daq:%s@%s:27000/admin" % (os.environ.get('MONGO_PASSWORD'), host))
    return client[db]

def get_daq_buffer_info():
    data = {'name' : 'daq_buffer',
            'time' : datetime.datetime.utcnow()}
    for eb in EB_SERVERS:
        data[eb] = get_db(eb).command({'dbstats': 1})
        if data[eb]['dataSize'] > max_size:
            max_size = data[eb]['dataSize']
    return data, max_size

def db_size(resolve = False):
    db = get_db(host='gw', db='run')
    collection = db['pipeline_status']
    collection.create_index("time", expireAfterSeconds=86400)
    collection.insert(data)



    my_key = 'PAGERDUTY_API_KEY_DAQ_BUFFER_SIZE'
    if os.environ.get(my_key) is None:
        print("Set environmental variable", my_key)
        sys.exit()

    data, max_size = get_max_size()

    
        
    if max_size > 1e11:
        alert = Alert(service_key=os.environ.get(my_key))
        alert.trigger(
            description='DAQ buffer is overflowing (more than 100 gigabyte)',
            client='pipeline_alarms',
            client_url='https://github.com/XENON1T/pipeline_alarms',
            details=data
        )
        
            
            

    1e11


    return
#    my_key = 'PAGERDUTY_API_KEY_DAQ'
#    if os.environ.get(my_key) is None:
#        print("Set environmental variable", my_key)
#        sys.exit()

#        alert = Alert(service_key=os.environ.get(my_key))

 #       alert.trigger(
 #           description='Midway is not running massive cax',
 #           client='data_manager_alarms',
 #           client_url='https://github.com/XENON1T/data_manager_alarms',
 #           details={'ps output': output},
 #       )


while 1:

    db_size()

    time.sleep(60*60)
