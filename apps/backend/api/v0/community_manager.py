# -*- coding: utf-8 -*-
"""Example of Flask and qrcode.

NOTE: by requirements image in memory!
"""
from apps.backend.api.v0.db_manager import TokenManager
from flask_restful import Resource

from apps.backend.api.v0.models import Community

__author__ = 'Rohit Kumar'
__version__ = (0, 0, 1)

import sys
from urllib.request import urlopen
import flask
import qrcode
import io
import uuid
from os import urandom
import json
from flask import request,Response, jsonify, make_response

from config.Config import Config

cfg = Config().get()


class CommunityManager(Resource):
    def __init__(self, ):
        return

    def post(self, source):
        if (source == 'create_encypted' or source == 'create'):
            try:
                if (request.is_json):
                    basic_parameters = request.json
                    community_id = basic_parameters['community_id']
                    community_name = basic_parameters['community_name']
                    authorizable_attribute_id = basic_parameters['authorizable_attribute_id']
                    credential_issuer_endpoint_address = basic_parameters['credential_issuer_endpoint_address']
                    if (source == 'create_encypted'):
                        return self.create_secure_community(community_name, community_id, authorizable_attribute_id,
                                                            credential_issuer_endpoint_address)
                    else:
                        return self.create_community(community_name, community_id, authorizable_attribute_id,
                                                     credential_issuer_endpoint_address)

                else:
                    return ("Content Type not Json!! That was the deal please !!")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return "Value Error 1 "
        else:
            return "Invalid!!"

    def create_secure_community(self, community_name, community_id, attribute_id, credential_issuer_endpoint_address):
        try:

            bcn_community_id=1
            f = urlopen(credential_issuer_endpoint_address)
            myfile = f.read()


            bcn_community = Community.create(community_name, community_id, attribute_id,
                                             credential_issuer_endpoint_address)
            return {"id": bcn_community.id,"public_key":cfg['encryption']['public']}



        except:
            print("Unexpected error:", sys.exc_info()[0])
            response = jsonify(message="Internal Error")
            response.status_code = 401
            return response

    def create_community(self, community_name, community_id, attribute_id, credential_issuer_endpoint_address):
        try:
           bcn_community= Community.create(community_name, community_id, attribute_id, credential_issuer_endpoint_address)
           return {"id" :bcn_community.id}



        except:
            print("Unexpected error:", sys.exc_info()[0])
            response = jsonify(message="Internal Error")
            response.status_code = 401
            return response