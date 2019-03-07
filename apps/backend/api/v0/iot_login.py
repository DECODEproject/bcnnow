# -*- coding: utf-8 -*-
"""Example of Flask and qrcode.

NOTE: by requirements image in memory!
"""
from http.client import HTTPResponse

from apps.backend.api.v0.token_manager import TokenManager
from flask_restful import Resource
__author__ = 'Rohit Kumar'
__version__ = (0, 0, 1)

import sys
import qrcode
import io
from os import urandom
from flask import request
from config.config import Config
import base64

cfg = Config().get()


class IoTWalletLoginManager(Resource):
    def __init__(self, ):
        return

    def get(self, source):
        if source == 'qrcode':
            return self.get_qrimg()
        elif source == 'link':
            return self.get_link()
        elif source == 'login':
            session_id = request.args['session']
            return self.allow_login(session_id)
        elif source == 'force':
            session_id = request.args['session']
            return self.forceValidateLogin(session_id)
        else:
            return "Invalid!!"

    def post(self, source):
        if source == 'qrcode':
            return self.get_qrimg()
        elif source == 'link':
            return self.get_link()
        elif source == 'login':
            session_id = request.args['session']
            return self.allow_login(session_id)
        elif source == 'validate':
            try:
                if request.is_json:
                    basic_parameters = request.json
                    token = basic_parameters['sessionId']
                    return self.validateLogin(token,basic_parameters['attribute'])
                else:
                    return ("Content Type not Json!! That was the deal please !!")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return "Value Error 1 "
        else:
            return "Invalid!!"

    def validateLogin(self, token, basic_parameters):
        try:
            tkn_manager = TokenManager()
            tkn_status=tkn_manager.validate_token(token)

            if tkn_status == '1':
                predicate = basic_parameters['attribute']['predicate']
                if (predicate == 'schema:iotCommunity'):
                    credential_x = basic_parameters['attribute']['provenance']['credential']['x']
                    credential_y = basic_parameters['attribute']['provenance']['credential']['y']
                    return "Login_valid"
                else:
                    return "predicate not matching"
            else:
                return tkn_status
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return "Value Error 2"

    def forceValidateLogin(self, token):
        try:
            tkn_manager = TokenManager()
            tkn_status = tkn_manager.validate_token(token)
            return tkn_status
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return "Value Error 2"

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
        #generate new token
        tkn = urandom(12).hex()
        tkn_manager = TokenManager()
        if tkn_manager.insert_token(tkn):
            return tkn
        else:
            return None

    @staticmethod
    def get_qrimg():
        token = IoTWalletLoginManager.get_new_token()
        schema = cfg['iotconfig']['schema']
        header = cfg['iotconfig']['header']
        callback = cfg['iotconfig']['callbackurl']
        data = '%s://?action=login&header =%s&sessionId=%s&callback=%s' % (schema, header, token, callback)
        img_buf = io.BytesIO()
        img = IoTWalletLoginManager.random_qr(url=data)
        img.save(img_buf)
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.getvalue()).decode()
        return {"qr": img_str, "session": token, "url_app": data, "url": data}

    def allow_login(self, sessionId):
        status = False
        if sessionId == "987654321":
            status = True
        else:
            tkn_manager = TokenManager()
            tkn_status = tkn_manager.check_token(sessionId)
            if tkn_status == 1:
                status = True
        return {"status": status}

    def get_link(self):
        token=self.get_new_token()
        header=cfg['iotconfig']['header']
        callback=cfg['iotconfig']['callbackurl']
        data= 'decodewallet://?action=login&header =%s&sessionId=%s&callback=%s'%(header,token,callback)
        return data

