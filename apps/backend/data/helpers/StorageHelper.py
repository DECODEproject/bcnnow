'''
    BarcelonaNow (c) Copyright 2018 by the Eurecat - Technology Centre of Catalonia

    This source code is free software; you can redistribute it and/or
    modify it under the terms of the GNU Public License as published
    by the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This source code is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Please refer to the GNU Public License for more details.

    You should have received a copy of the GNU Public License along with
    this source code; if not, write to:
    Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
'''

from pymongo import MongoClient
from kafka import KafkaProducer
from config.Config import Config
import json

cfg = Config().get()

# This class defines a set of utilities methods to storage BaseRecord instances.
class StorageHelper:
    def __init__(self):
        return

    # This method saves the BaseRecord record. The global configuration variable storage/mode specifies the destination.
    def store(self, record):
        record = json.loads(record, encoding="utf8")
        if cfg['collectors']['common']['destination'] == 'kafka':
            producer = KafkaProducer(value_serializer=lambda v: v.encode('utf-8'))
            future = producer.send(record['source'], json.dumps(record))
            future.get(timeout=60)
        elif cfg['collectors']['common']['destination'] == 'mongodb':
            client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
            db = client[cfg['storage']['dbname']]
            collection = db[record['source']]
            print(record)
            collection.replace_one({"id": record['id']}, record, upsert=True)