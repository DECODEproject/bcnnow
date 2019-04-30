import sys
from logging.config import dictConfig

from bson import ObjectId
from flask import Flask, logging, current_app, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
from flask import request
from datetime import datetime
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from config.config import Config
import json
import re
import ast
from flask_compress import Compress
from apps.backend.api.v0.oauth2_routes import OAuthManager
from apps.backend.api.v0.iot_login import IoTWalletLoginManager
from apps.backend.api.v0.models import db, DataSetCommunity, DataSet, Dashboard, DashboardCommunity
from apps.backend.api.v0.oauth2 import config_oauth, require_oauth
from apps.backend.api.v0.community_manager import CommunityManager

cfg = Config().get()

app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }, 'detailed': {
        'format': '%(asctime)s %(module)-17s line:%(lineno)-4d '
        '%(levelname)-8s %(message)s',
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'bcnnow_api.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})

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

    def post(self, source):
        if source == 'post_new_dashboard':
            current_app.logger.info("Called POST post_new_dashboard")
            return self.post_new_dashboard()

    # @require_oauth('profile')
    def get(self, source):

        if source == 'get_available_datasets':
            current_app.logger.info("Called GET get_available_datasets")
            return self.get_available_datasets()

        if source == 'get_public_dashboards':
            current_app.logger.info("Called GET get_public_dashboards")
            return self.get_public_dashboards()

        if source == 'get_private_dashboards':
            current_app.logger.info("Called GET get_private_dashboards")
            return self.get_private_dashboards()

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
                    query.append({"$group": {"_id": {field.split('@')[0]: '$' + field.split('@')[1] for field in group.split(',')}, "count":{"$sum":1}, "doc": {"$last": "$$ROOT"}}})
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

        try:
            # connect to Mongo
            client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
            m_db = client[cfg['storage']['dbname']]
            collection = m_db["datasets"]

            # get dataset json contents from MongoDB
            return_dict = {}

            # build an array of private dataset ids:
            user = OAuthManager.get_current_user()
            data_sets_community = DataSetCommunity.query.filter_by(community_id=user.community_id).all()
            for data_set in data_sets_community:
                entry = collection.find_one({"id": str(data_set.dataset_id)})
                # add type to entry
                entry["availability"] = 'private'
                return_dict[entry["id"]] = entry

            # get public datasets
            data_sets = DataSet.query.filter_by(typeof='public').all()
            for data_set in data_sets:
                entry = collection.find_one({"id": str(data_set.id)})
                # add type to cursor
                entry["availability"] = 'public'
                return_dict[entry["id"]] = entry

            ret = JSONEncoder().encode(return_dict)
            return json.loads(ret)
        except Exception as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            response = jsonify(message="System Error")
            response.status_code = 401
            return response

    @require_oauth('profile')
    def get_public_dashboards(self):

        try:
            # get public dashboards
            dashboards = Dashboard.query.filter_by(typeof='public').all()

            # get dashboards json contents from MongoDB
            client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
            m_db = client[cfg['storage']['dbname']]
            collection = m_db["dashboards"]

            return_dict = {}

            for dashboard in dashboards:

                query_cursor = collection.find({"id": dashboard.id})

                for cursor in query_cursor:
                    # build dict of format "page-2": {...}
                    head = "page-" + str(cursor["id"]-1)
                    return_dict[head] = cursor
                    # body = cursor[head]
                    # return_dict[head] = body

            ret = JSONEncoder().encode(return_dict)
            return json.loads(ret)
        except Exception as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            response = jsonify(message="System Error")
            response.status_code = 401
            return response


    @require_oauth('profile')
    def get_private_dashboards(self):
        user = OAuthManager.get_current_user()
        dashboard_community = DashboardCommunity.query.filter_by(community_id=user.community_id).all()

        # build an array of dashboard ids:
        dashboard_ids = []
        for dashboard in dashboard_community:
            dashboard_ids.append(dashboard.dashboard_id)

        # get dashboard json contents from MongoDB
        client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
        m_db = client[cfg['storage']['dbname']]
        collection = m_db["dashboards"]

        return_dict = {}
        for dashboard_id in dashboard_ids:

            query_cursor = collection.find({"id": dashboard_id})

            for cursor in query_cursor:
                # build dict of format "page-2": {...}
                head = "page-" + str(cursor["id"] - 1)
                return_dict[head] = cursor
                # body = cursor[head]
                # return_dict[head] = body

        ret = JSONEncoder().encode(return_dict)
        return json.loads(ret)

    @require_oauth('profile')
    def post_new_dashboard(self):
        user = OAuthManager.get_current_user()
        dashboard = json.loads(request.data.decode("utf-8"))

        # search if the dashboard already exists in MongoDB
        # db.getCollection('dashboards').find({"name": "Housing"}).sort({ "id": -1 }).limit(1)
        client = MongoClient(cfg['storage']['ipaddress'], cfg['storage']['port'])
        m_db = client[cfg['storage']['dbname']]
        collection = m_db["dashboards"]

        # calc the type of the dasboard
        dashboard_type = 'public'
        # if len(dashboard['widgets']) == 0:
        #     dashboard_type = 'public'
        for widget in dashboard['widgets']:
            #     if len(widget['sources']) == 0:
            #     dashboard_type = 'public'
            for source in widget['sources']:
                dataset = DataSet.query.filter_by(id=source['id']).first()
                if dataset.typeof == 'private':
                    dashboard_type = 'private'
                    break
                # remove data
                source['dataset'] = None

        if 'id' in dashboard.keys():
            # get the id from the query
            entry = collection.find_one({"id": dashboard['id']})
            dashboard_id = entry["id"]
            # put the contents of the existing Mongo entry in dashboard_configuration_history table
            existent_dashboard = collection.find_one({"id": dashboard_id})
            existent_dashboard['timestamp'] = datetime.now()
            collection_history = m_db["dashboard_configuration_history"]
            del existent_dashboard['_id']
            collection_history.insert_one(existent_dashboard)
            # update the existing entry in dashboards
            collection.update_one({"id": dashboard_id}, {"$set": dashboard}, upsert=False)

            # update the mysql to public or private if it changes
            # get current dashboard type
            current_dashboard_mysql = Dashboard.query.filter_by(id=existent_dashboard['id']).first()
            current_dashboard_type = current_dashboard_mysql.typeof

            if current_dashboard_type != dashboard_type:
                Dashboard.update(existent_dashboard['id'], dashboard_type)
                # if private to public
                if dashboard_type == 'public':
                    # remove entries for dataset in dataset_community
                    DashboardCommunity.remove_dashboard_from_community(existent_dashboard['id'], user.community_id)
                # if public to private
                if dashboard_type == 'private':
                    # add entries for dataset in dataset_community
                    DashboardCommunity.add_dashboard_to_community(existent_dashboard['id'], user.community_id)

        else:
            # insert new
            # get max id
            max_id = collection.find({}).sort("id", pymongo.DESCENDING).limit(1)[0]["id"]
            # save new in mongo with +1 id
            new_id = max_id+1
            dashboard['id'] = new_id
            collection.insert_one(dashboard)
            # insert dashboard in mysql
            Dashboard.create(new_id, dashboard_type)
            # relate to the current user if it's private
            if dashboard_type == 'private':
                DashboardCommunity.add_dashboard_to_community(new_id, user.community_id)

        return True

    @app.errorhandler(500)
    def internal_error(exception):
        current_app.logger.error(exception)
        response = jsonify(message="Unexpected error")
        response.status_code = 500
        return response

if __name__ == '__main__':
    Compress(app)
    CORS(app)
    api = Api(app)
    db.init_app(app)
    config_oauth(app)

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel('INFO')

    api.add_resource(BasicDataAccess, '/api/v0/<source>')
    api.add_resource(IoTWalletLoginManager, '/iotlogin/<string:source>')
    api.add_resource(OAuthManager, '/oauth/<string:source>')
    api.add_resource(CommunityManager, '/community/<string:source>')
    app.run(host='0.0.0.0', port=cfg['api']['v0']['port'], threaded=True, debug=False)
