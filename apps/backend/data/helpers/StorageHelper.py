from pymongo import MongoClient, GEO2D
from kafka import KafkaProducer
from config.Config import Config
import json
import datetime

cfg = Config().get()

class StorageHelper:

    def __init__(self):
        return

    # Store record in Kafka or MongoDB
    def store(self, record):
        json_record = json.loads(record, encoding="utf8")
        if cfg['collectors']['common']['destination'] == 'kafka':
            producer = KafkaProducer(value_serializer=lambda v: v.encode('utf-8'))
            future = producer.send(cfg['storage']['topic'], json.dumps(json_record))
            result = future.get(timeout=60)
            print(str(datetime.datetime.now()) + ' ' + '              Saved to ' + cfg['collectors']['common']['destination'] + ' ' + record)
        elif cfg['collectors']['common']['destination'] == 'mongodb':
            client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
            db = client[cfg['storage']['dbname']]
            collection = db[json_record['source']]
            try:
                if collection.find({"id": json_record['id']}).count() == 0:
                    collection.insert_one(json_record)
                    print(str(datetime.datetime.now()) + ' ' + '              Saved to ' + cfg['collectors']['common']['destination'] + ' ' + record)
                else:
                    collection.update_one({"id": json_record['id']}, {"$set": json_record}, upsert=False)
                    print(str(datetime.datetime.now()) + ' ' + '              Updated to ' + cfg['collectors']['common']['destination'] + ' ' + record)
            except:
                print(str(datetime.datetime.now()) + ' ' + '              Error with ' + cfg['collectors']['common']['destination'] + ' ' + record)

