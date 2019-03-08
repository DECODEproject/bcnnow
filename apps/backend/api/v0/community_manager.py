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
from flask import request, jsonify
from config.config import Config

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

            bcn_community = Community.create(community_name, community_id, attribute_id,
                                             credential_issuer_endpoint_address)
            print("created community locally")
            credential_key = b'''{
            "issuer_identifier": {
                 "verify": {
                  "alpha": "367ebdd5253b44465955adf396342ad08cc35ead43a6ede3363583175bf7918f98a3821379ae385a56a49074c5ce280c387616731023b7cab28837514b30a3a202f442a4a91fefbce1f7fa9bc3d61549898df123e9d12fb94c601810f5dcce9b2110f4742d99ee6fda4f2d1849678f5621aad99d535e8671baff04b0368f9d2ba5edbaa6174ff36aec427bfe94920cdf3a8c849089bbb8f275a2119479e58ffa23bbcf518972eb940d0da93b20b7eabac112f5626be99176d028c091aee642ac",
                  "beta": "3f848595e9c114d2dad9df90c1b6f404359a17fc15190ce2b1c563e021c3165b6b240dda993088419183099a2dd39f6b26ba1772f8cfd9ff93fc16d904aa21bbaf1bdfbe27c17c92b6a802eb6709f896a053c75fa517d57edc98b7fc3c54449f4c0d44f2cb0a312ce265f112359147e46f6e36c6afd73c089c23600af74c9abb6d72bd10b040e160144d39cca9cd9bfd124ecf292275ced2f5fb252c709d87d2be1eed33045700582f9ad76d7714eba6a30944654b295f5be2599f286571cd48"
                   }
                }
            }
            '''
            # to do get it from end point url
            if(cfg['iotconfig']['bypass']=='no'):
                res = requests.get(credential_issuer_endpoint_address + "authorizable_attribute/{}".format(attribute_id))
                if res.ok:
                    print("\tAll good, got this result: {}".format(res.json()))
                    credential_key = res.json()
                else:
                    print("\tCalls not getting back, got this error: {}".format(res.json()))
                    response = jsonify(message="Could not get public key data from credential_issuer_endpoint_address")
                    response.status_code = 401
                    return response

            print("got public key for validation")
            Community.update(bcn_community.id, credential_key)
            return {"id": bcn_community.id, "public_key": cfg['encryption']['public']}
        except:
            print("Unexpected error:", sys.exc_info()[0])
            response = jsonify(message="Internal Error")
            response.status_code = 401
            return response

    def create_community(self, community_name, community_id, attribute_id, credential_issuer_endpoint_address):
        try:

            bcn_community = Community.create(community_name, community_id, attribute_id,
                                             credential_issuer_endpoint_address)
            print("created community locally")
            credential_key = b'''{
            "issuer_identifier": {
                 "verify": {
                  "alpha": "367ebdd5253b44465955adf396342ad08cc35ead43a6ede3363583175bf7918f98a3821379ae385a56a49074c5ce280c387616731023b7cab28837514b30a3a202f442a4a91fefbce1f7fa9bc3d61549898df123e9d12fb94c601810f5dcce9b2110f4742d99ee6fda4f2d1849678f5621aad99d535e8671baff04b0368f9d2ba5edbaa6174ff36aec427bfe94920cdf3a8c849089bbb8f275a2119479e58ffa23bbcf518972eb940d0da93b20b7eabac112f5626be99176d028c091aee642ac",
                  "beta": "3f848595e9c114d2dad9df90c1b6f404359a17fc15190ce2b1c563e021c3165b6b240dda993088419183099a2dd39f6b26ba1772f8cfd9ff93fc16d904aa21bbaf1bdfbe27c17c92b6a802eb6709f896a053c75fa517d57edc98b7fc3c54449f4c0d44f2cb0a312ce265f112359147e46f6e36c6afd73c089c23600af74c9abb6d72bd10b040e160144d39cca9cd9bfd124ecf292275ced2f5fb252c709d87d2be1eed33045700582f9ad76d7714eba6a30944654b295f5be2599f286571cd48"
                   }
                }
            }
            '''
            # to do get it from end point url
            if (cfg['iotconfig']['bypass']=='no'):
                res = requests.get(credential_issuer_endpoint_address + "authorizable_attribute/{}".format(attribute_id))
                if res.ok:
                    print("\tAll good, got this result: {}".format(res.json()))
                    credential_key = res.json()
                else:
                    print("\tCalls not getting back, got this error: {}".format(res.json()))
                    response = jsonify(message="Could not get public key data from credential_issuer_endpoint_address")
                    response.status_code = 412
                    return response

            print("got public key for validation")
            Community.update(bcn_community.id, credential_key)
            return {"id": bcn_community.id}
        except:
            print("Unexpected error:", sys.exc_info()[0])
            response = jsonify(message="Internal Error")
            response.status_code = 401
            return response
