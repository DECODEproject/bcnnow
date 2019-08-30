from pymongo import MongoClient, GEO2D
from kafka import KafkaProducer
from config.config import Config
import json
from datetime import datetime

cfg = Config().get()

class StorageHelper:
    client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
    db = client[cfg['storage']['dbname']]
    def __init__(self):
        return
    # Store record in Kafka or MongoDB
    def store(self, record,check_old=True):
        print("store")
        json_record = json.loads(record, encoding="utf8")
        ts = datetime.timestamp(datetime.now())
        collection = StorageHelper.db[json_record['source']]
        try:
            if(check_old):
                if collection.find({"id": json_record['id']}).count() == 0:
                    collection.insert_one(json_record)
                    #print(str(datetime.datetime.now()) + ' ' + '              Saved to ' + cfg['collectors']['common']['destination'] + ' ' + record)
                else:
                    collection.update_one({"id": json_record['id']}, {"$set": json_record}, upsert=False)
                    #print(str(datetime.datetime.now()) + ' ' + '              Updated to ' + cfg['collectors']['common']['destination'] + ' ' + record)
            else:
                collection.insert_one(json_record)
        except Exception as e:
            print(str(e))
        print(datetime.timestamp(datetime.now())-ts)

