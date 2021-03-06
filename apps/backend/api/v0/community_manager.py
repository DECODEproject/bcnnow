# -*- coding: utf-8 -*-
"""Example of Flask and qrcode.

NOTE: by requirements image in memory!
"""

from flask_restful import Resource

from apps.backend.api.v0.models import Community

__author__ = 'Rohit Kumar'
__version__ = (0, 0, 1)

import sys

import requests
from flask import request, jsonify, current_app
from config.config import Config

cfg = Config().get()


class CommunityManager(Resource):
    def __init__(self, ):
        return

    def post(self, source):
        if source == 'create_encrypted' or source == 'create':
            try:
                current_app.logger.info(" Called POST create community")
                current_app.logger.info("json: " + str(request.json))
                basic_parameters = request.json
                community_id = basic_parameters['community_id']
                current_app.logger.debug("Created community: " + community_id)
                community_name = basic_parameters['community_name']
                authorizable_attribute_id = basic_parameters['authorizable_attribute_id']
                credential_issuer_endpoint_address = basic_parameters['credential_issuer_endpoint_address']
                if source == 'create_encrypted':
                    return self.create_secure_community(community_name, community_id, authorizable_attribute_id,
                                                        credential_issuer_endpoint_address)
                else:
                    return self.create_community(community_name, community_id, authorizable_attribute_id,
                                                 credential_issuer_endpoint_address)

            except Exception as e:
                current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
                current_app.logger.error("Error description: " + e)
                response = jsonify(message="Internal Error: " + str(e))
                response.status_code = 501
                return response
        else:
            current_app.logger.error("Unknown request: " + source)
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            response = jsonify(message="Invalid source path")
            response.status_code = 501
            return response

    def create_secure_community(self, community_name, community_id, attribute_id, credential_issuer_endpoint_address):
        try:

            bcn_community = Community.create(community_name, community_id, attribute_id,
                                             credential_issuer_endpoint_address)
            return {"id": bcn_community.id, "public_key": cfg['encryption']['public']}
        except Exception as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            response = jsonify(message="community_id or attribute_id already exist")
            response.status_code = 501
            return response

    def create_community(self, community_name, community_id, attribute_id, credential_issuer_endpoint_address):
        try:
            current_app.logger.debug("updating db")
            bcn_community = Community.create(community_name, community_id, attribute_id,
                                             credential_issuer_endpoint_address)
            current_app.logger.info("created community locally: " + community_name)
            return {"id": bcn_community.id}
        except Exception as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            response = jsonify(message="community_id or attribute_id already exist")
            response.status_code = 501
            return response
