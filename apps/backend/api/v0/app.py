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

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
from flask import request
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from config.Config import Config
import json
import re
import ast
from flask_compress import Compress

cfg = Config().get()

app = Flask(__name__)

# This method validates the received parameters and return them into a dictionary
def getParams(request):
    default_page_size = 2147483647
    default_limit = 2147483647

    params = dict(request.args)
    params['page'] = int(request.args['page']) if "page" in params else 1
    params['page_size'] = int(request.args['page_size']) if "page_size" in params else default_page_size
    params['page_limit'] = int(request.args['limit']) if "limit" in params else default_limit
    params['location'] = ast.literal_eval(request.args['near']) if "near" in params else [0.0, 0.0]
    params['sort'] = [[field.split('@')[1] if '@' in field else field, (pymongo.ASCENDING if field.split('@')[0].lower() == 'a' else pymongo.DESCENDING) if '@' in field else pymongo.ASCENDING] for field in request.args['sort'].split(',')] if "sort" in params else ''
    params['group'] = request.args['group'] if "group" in params else ''
    params['isobservation'] = True if "isobservation" in params else False
    params['norecords'] = True if "norecords" in params else False
    params['fields']= request.args['fields'] if "fields" in params else ''
    params['aggregator'] = request.args['aggregators'] if "aggregator" in params else ''
    params['page_step']= int(request.args['step']) if "step" in params else 1

    return params

# This method translates the parameters from the API format to MongoDB query syntax
def getMongoSyntax(params):
    try:
        for key, field in params.items():
            value = field[0]
            if ',' in value:
                set = {}
                for criteria in value.split(','):
                    set['$' + criteria.split('@')[0]] = criteria.split('@')[1]
                params[key] = set
            elif '@' in value:
                params[key] = {'$' + value.split('@')[0]: value.split('@')[1]}
            else:
                parsed = value if not '[' in value else re.compile('.*' + value.replace('[', '').replace(']', '') + '.*', re.IGNORECASE)
                params[key] = parsed
    except:
        params[key] = value

    location = {}
    if params['location'][0] != 0 and params['location'][1] != 0:
        location['$near'] = {}
        location['$near']['$geometry'] = {'type': 'Point', 'coordinates': [params['location'][1], params['location'][0]]}
    if len(location) > 0:
        params['location.point'] = location

    if 'group' in params:
        if not 'sort' in params:
            params['sort'] = []
        params['sort'].append(['distance', pymongo.ASCENDING])
        for key, value in params.copy().items():
            if not '$' in key:
                params['doc.' + key] = value
            else:
                params[key[1:]] = value

    return params

# This method traslates the MongoDB query results into standard API results
def getResults(params, results, base= '', path='/api/v0/'):
    records = [] if params['norecords'] else [dumps(element) for index, element in enumerate(results[(params['page'] - 1) * params['page_size']:params['page'] * params['page_size']]) if index < params['page_limit'] and index % params['page_step'] == 0]
    count = (results.count() / params['page_step'] if not 'group' in params else len(results) / params['page_step'])
    next = (base + path + '?page=' + str(params['page'] + 1) + '&page_size=' + str(params['page_size']) + (''.join(['&' + key + '=' + value[0] for key, value in params.items()]))) if params['page'] * params['page_size'] < count else ""
    current = base + path + '?page=' + str(params['page']) + '&page_size=' + str(params['page_size']) + (''.join(['&' + key + '=' + value[0] for key, value in params.items()]))
    success = "true"
    return json.loads('{"success": ' + json.dumps(success) + ', ' + '"count": ' + json.dumps(count) + ', ' + '"records": [' + ','.join(records) + '], ' + '"links": {"current": ' + json.dumps(current) + ', "next": ' + json.dumps(next) + '}}')

# This method executes the corresponding query on MongoDB
def performQuery(source, params):
    client = MongoClient(cfg['storage']['mongodb']['ip'], cfg['storage']['mongodb']['port'])
    db = client[cfg['storage']['mongodb']['dbname']]
    collection = db[source]

    query = []
    if not 'group' in params:
        if params['sort'] != '':
            results = collection.find(params).sort(params['sort'])
        else:
            results = collection.find(params)
    else:
        if params['location'][0] != 0 and params['location'][1] != 0:
            query.append({'$geoNear': {'near': {'type': 'Point', 'coordinates': [params['location'][1], params['location'][0]]}, 'spherical': True, 'distanceField': 'distance'}})
            query.append({"$sort": {"timestamp": 1}})
            query.append({"$unwind": "$" + params['group']})
            query.append({"$group": {"_id": "$" + params['group'], "doc": {"$last": "$$ROOT"}}})
            query.append({"$match": params})
            query.append({"$sort": {"doc.distance": 1}})
            results = list(collection.aggregate((query)))
        else:
            if 'isobservation' in params:
                query.append({"$match": params})
                grouped = {
                    "$group": {"_id": {field.split('@')[0]: '$' + field.split('@')[1] for field in params['group'].split(',')},
                               "doc": {"$push": {field.split('@')[0]: '$' + field.split('@')[1] for field in
                                                 params['fields'].split(',')}}}}
                grouped["$group"]["count"] = {"$sum": 1}
                if params['aggregator'] != '':
                    for aggregator in params['aggregator'].split(','):
                        grouped["$group"][aggregator.split('@')[0]] = {
                            "$" + aggregator.split('@')[0]: "$" + aggregator.split('@')[1]}
                query.append(grouped)
                for field in params['group'].split(',')[1:]:
                    query.append({"$group": {"_id": "$_id." + field.split('@')[0], "doc": {"$push": "$$ROOT"}}})
                query.append({"$sort": {"_id": 1}})
                results = list(collection.aggregate((query), allowDiskUse=True))
            else:
                query.append({"$match": params})
                query.append({"$group": {
                    "_id": {field.split('@')[0]: '$' + field.split('@')[1] for field in params['group'].split(',')},
                    "doc": {"$last": "$$ROOT"}}})
                query.append({"$sort": {"_id": 1}})
                results = list(collection.aggregate((query), allowDiskUse=True))
    return results

# This class represents the base root to access API
class BasicDataAccess(Resource):

    def get(self, source):
        params = getMongoSyntax(getParams(request))
        results = performQuery(source, params)
        return getResults(params, results)

if __name__ == '__main__':
    Compress(app)
    CORS(app)
    api = Api(app)
    api.add_resource(BasicDataAccess, '/api/v0/<source>')
    app.run(host='0.0.0.0', port=cfg['api']['v0']['port'], threaded=True, debug=False)