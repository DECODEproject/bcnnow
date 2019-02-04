from bson import ObjectId
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
from apps.backend.api.v0.oauth2_routes import OAuthManager
from apps.backend.api.v0.iot_login import IoTWalletLoginManager
from apps.backend.api.v0.models import db, DataSetCommunity, DataSet
from apps.backend.api.v0.oauth2 import config_oauth, require_oauth

cfg = Config().get()

app = Flask(__name__)

app.config.update({
    'SECRET_KEY': 'NyJH84Nh5iTSoYime40ctGPkwN6sPSL8kVpg92YpA2SUhPzU',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': cfg['db']['url'],
})


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# Basic Root API
class BasicDataAccess(Resource):

    # @require_oauth('profile')
    def get(self, source):

        if source == 'get_available_datasets':
            return self.get_available_datasets()

        # Default values
        default_page_size = 2147483647
        default_limit = 2147483647

        # Parse parameters
        base = cfg['api']['v0']['ipaddress'] + "/api/v0/"
        basic_parameters = dict(request.args)
        parameters = dict(request.args)
        page = int(request.args['page']) if "page" in parameters else 1
        parameters.pop('page', None)
        basic_parameters.pop('page', None)
        page_size = int(request.args['page_size']) if "page_size" in parameters else default_page_size
        parameters.pop('page_size', None)
        basic_parameters.pop('page_size', None)
        limit = int(request.args['limit']) if "limit" in parameters else default_limit
        parameters.pop('limit', None)
        near = ast.literal_eval(request.args['near']) if "near" in parameters else []
        latitude = near[0] if "near" in parameters else 0
        longitude = near[1] if "near" in parameters else 0
        parameters.pop('near', None)
        sort = [[field.split('@')[1] if '@' in field else field, (pymongo.ASCENDING if field.split('@')[0].lower() == 'a' else pymongo.DESCENDING) if '@' in field else pymongo.ASCENDING] for field in request.args['sort'].split(',')] if "sort" in parameters else ''
        parameters.pop('sort', None)
        group = request.args['group'] if "group" in parameters else ''
        parameters.pop('group', None)
        isObservation = True if "isObservation" in parameters else False
        parameters.pop('isObservation', None)
        noRecords = True if "noRecords" in parameters else False
        parameters.pop('noRecords', None)
        fields = request.args['fields'] if "fields" in parameters else ''
        parameters.pop('fields', None)
        aggregators = request.args['aggregators'] if "aggregators" in parameters else ''
        parameters.pop('aggregators', None)
        step = int(request.args['step']) if "step" in parameters else 1
        parameters.pop('step', None)

        # Translate non-primitive conditions in MongoDB syntax
        try:
            for key, field in parameters.items():
                value = field[0]
                if ',' in value:
                    set = {}
                    for criteria in value.split(','):
                        set['$'+criteria.split('@')[0]] = criteria.split('@')[1]
                    parameters[key] = set
                elif '@' in value:
                    parameters[key] = {'$'+value.split('@')[0]: value.split('@')[1] }
                else:
                    parsed = value if not '[' in value else re.compile('.*' + value.replace('[','').replace(']','') + '.*', re.IGNORECASE)
                    parameters[key] = parsed
        except:
            parameters[key] = value

        # Translate location condition in MongoDB syntax
        location = {}
        if latitude != 0 and longitude != 0:
            location['$near'] = {}
            location['$near']['$geometry'] = { 'type': 'Point', 'coordinates': [longitude, latitude] }
        if len(location) > 0:
            parameters['location.point'] = location

        # Translate group conditions in MongoDB syntax
        isGroup = False
        if group != '':
            isGroup = True
            if sort == '':
                sort = []
            sort.append(['distance', pymongo.ASCENDING])
            parameters.pop('location.point', None)
            novel = {}
            for key, value in parameters.items():
                if not '$' in key:
                    novel['doc.'+key] = value
                else:
                    novel[key[1:]] = value
            parameters = novel

        # Perform query
        client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
        db = client[cfg['storage']['dbname']]
        collection = db[source]

        query = []
        if not isGroup:
            if sort != '':
                results = collection.find(parameters).sort(sort)
            else:
                results = collection.find(parameters)
        else:
            if len(location) > 0:
                query.append({'$geoNear': {'near': { 'type': 'Point', 'coordinates': [longitude,latitude]}, 'spherical': True, 'num': default_limit, 'distanceField': 'distance'} })
                query.append({"$sort": { "timestamp": 1 }})
                query.append({"$unwind": "$"+group})
                query.append({"$group": {"_id": "$"+group, "doc": {"$last": "$$ROOT"}}})
                query.append({"$match": parameters})
                query.append({"$sort": { "doc.distance": 1}})
                results = list(collection.aggregate((query)))
            else:
                if isObservation:
                    query.append({"$match": parameters})
                    grouped = {"$group": {"_id": {field.split('@')[0]: '$' + field.split('@')[1] for field in group.split(',')}, "doc": {"$push": {field.split('@')[0]:'$'+field.split('@')[1] for field in fields.split(',')}}}}
                    grouped["$group"]["count"] = {"$sum": 1}
                    if aggregators != '':
                       for aggregator in aggregators.split(','):
                            grouped["$group"][aggregator.split('@')[0]] = {"$"+aggregator.split('@')[0]: "$"+aggregator.split('@')[1]}
                    query.append(grouped)
                    for field in group.split(',')[1:]:
                        query.append({"$group": {"_id": "$_id." + field.split('@')[0], "doc": {"$push": "$$ROOT"}}})
                    query.append({"$sort": { "_id": 1 }})
                    results = list(collection.aggregate((query), allowDiskUse=True))
                else:
                    query.append({"$match": parameters})
                    query.append({"$group": {"_id": {field.split('@')[0]: '$' + field.split('@')[1] for field in group.split(',')}, "doc": {"$last": "$$ROOT"}}})
                    query.append({"$sort": { "_id": 1 }})
                    results = list(collection.aggregate((query), allowDiskUse=True))

        # Build query results
        records = [] if noRecords else [dumps(element) for index, element in enumerate(results[(page-1)*page_size:page*page_size]) if index < limit and index % step == 0]
        count = (results.count() / step if not isGroup else len(results) / step) #if limit == 2147483647 else limit
        next = (base + source + '?page=' + str(page+1) + '&page_size=' + str(page_size) + (''.join(['&'+key+'='+value[0] for key, value in basic_parameters.items()]))) if page * page_size < count else ""
        current = base + source + '?page=' + str(page) + '&page_size=' + str(page_size) + (''.join(['&'+key+'='+value[0] for key, value in basic_parameters.items()]))
        success = "true"
        return json.loads('{"success": ' + json.dumps(success) + ', ' \
                            '"count": ' + json.dumps(count) + ', ' \
                            '"records": [' + ','.join(records) + '], ' \
                            '"links": {"current": ' + json.dumps(current) + ', "next": ' + json.dumps(next) + '}}')

    @require_oauth('profile')
    def get_available_datasets(self):
        user = OAuthManager.get_current_user()
        data_sets_community = DataSetCommunity.query.filter_by(community_id=user.community_id).all()

        # get dataset json contents from MongoDB
        client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
        db = client[cfg['storage']['dbname']]
        collection = db["datasets"]

        return_dict = {}
        i = 1

        for data_set in data_sets_community:

            query_cursor = collection.find({"id": str(data_set.dataset_id)})
            # if query_cursor.count() == 1:
            #     return_json_obj = query_cursor[0]

            for cursor in query_cursor:
                return_dict[str(i)] = cursor
                i = i + 1

        # return_dict = {'1': return_json_obj}
        ret = JSONEncoder().encode(return_dict)
        # ret = '{ "1": ' + ret + '}'
        return json.loads(ret)


if __name__ == '__main__':
    Compress(app)
    CORS(app)
    api = Api(app)
    db.init_app(app)
    config_oauth(app)
    api.add_resource(BasicDataAccess, '/api/v0/<source>')
    api.add_resource(IoTWalletLoginManager, '/iotlogin/<string:source>')
    api.add_resource(OAuthManager, '/oauth/<string:source>')
    app.run(host='0.0.0.0', port=cfg['api']['v0']['port'], threaded=True, debug=False)
