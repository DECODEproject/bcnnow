# -*- coding: utf-8 -*-
"""Example of Flask and qrcode.

NOTE: by requirements image in memory!
"""
import base64

__author__ = 'Rohit Kumar'
__version__ = (0, 0, 1)
from apps.backend.api.v0.token_manager import TokenManager
from flask_restful import Resource
import sys
import flask
import qrcode
import io
import uuid
from apps.backend.api.v0.models import Community
from zenroom import zenroom
from flask import request, jsonify, current_app
from config.config import Config

cfg = Config().get()

class IoTWalletLoginManager(Resource):
    def __init__(self, ):
        return

    def get(self, source):
        if source == 'qrcode':
            current_app.logger.info("Called GET qrcode")
            return self.get_qrimg()
        elif source == 'link':
            current_app.logger.info("Called GET link")
            return self.get_link()
        else:
            current_app.logger.error("Called GET unknown method: " + source)
            return "Invalid!!"

    def post(self, source):
        if source == 'qrcode':
            current_app.logger.info("Called POST qrcode")
            return self.get_qrimg()
        elif source == 'link':
            current_app.logger.info("Called POST link")
            return self.get_link()
        elif source == 'validate':
            current_app.logger.info("Called POST validate")
            try:
                if request.is_json:
                    basic_parameters = request.json
                    token = basic_parameters['sessionId']
                    return self.validateLogin(token,basic_parameters['credential'])
                else:
                    response = jsonify(message="Content Type not Json!! That was the deal please !!")
                    response.status_code = 401
                    return response

            except Exception as e:
                current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
                current_app.logger.error("Error description: " + e)
                response = jsonify(message="System Error")
                response.status_code = 401
                return response
        else:
            current_app.logger.error("Called POST unknown method: " + source)
            return "Invalid!!"


    def validateLogin(self,token,basic_parameters):
        try:

            authorizable_attribute_id = basic_parameters['authorizable_attribute_id']
            credential_issuer_endpoint_address=basic_parameters['credential_issuer_endpoint_address']

            # read the public key DB
            bcn_community_obj = Community.get_from_authorizable_attribute_id(authorizable_attribute_id)
            issuer_public = bcn_community_obj.community_validation_key
            value = basic_parameters['value']
            current_app.logger.debug(value)

            # check with zenroom if login is valid
            with open('verifyer.zencode') as file:
                verify_credential_script = file.read()
            verify_response, errs = zenroom.execute(verify_credential_script.encode(), data=issuer_public, keys=value)
            if verify_response.decode() == "OK":
                tkn_manager = TokenManager()
                tkn_status = tkn_manager.validate_token(token)
                if tkn_status == '1':
                    return {"status": False, "message": "Login Success"}
                else:
                    response = jsonify(message="Invalid Tokken")
                    response.status_code = 401
                    return response
            else:
                response = jsonify(message="Invalid Credentials")
                response.status_code = 401
                return response

        except Exception as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            response = jsonify(message="Unexpected Error in Validation")
            response.status_code = 412
            return response



    @staticmethod
    def random_qr(url='www.google.com'):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4)

        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        return img

    @staticmethod
    def get_new_token():
        # generate new token
        tkn = uuid.uuid1().hex  # or uuid.uuid4()
        tkn_manager = TokenManager()
        if tkn_manager.insert_token(tkn):
            return tkn
        else:
            return None


    @staticmethod
    def get_qrimg():
        token = IoTWalletLoginManager.get_new_token()
        iot_login_url = cfg['iotconfig']['login_url']
        callback = cfg['iotconfig']['callbackurl']
        data = 'decodeapp://login?&sessionId=%s&callback=%s' % (token, callback)
        img_buf = io.BytesIO()
        img = IoTWalletLoginManager.random_qr(url=data)
        img.save(img_buf)
        img_buf.seek(0)
        dddc_img_str = base64.b64encode(img_buf.getvalue()).decode()
        url_webapp = '%slogin?sessionId=%s&callback=%s' % (iot_login_url, token, callback)
        iot_img_buf = io.BytesIO()
        iot_img = IoTWalletLoginManager.random_qr(url=url_webapp)
        iot_img.save(iot_img_buf)
        iot_img_buf.seek(0)
        iot_img_str = base64.b64encode(iot_img_buf.getvalue()).decode()

        return {"session": token, "dddc_qr": dddc_img_str, "dddc_url": data, "iot_qr": iot_img_str, "iot_url": url_webapp}

    @staticmethod
    def get_link():
        token=IoTWalletLoginManager.get_new_token()
        header=cfg['iotconfig']['header']
        callback=cfg['iotconfig']['callbackurl']
        data = 'decodeapp://login?&sessionId=%s&callback=%s' % (token, callback)
        return data

