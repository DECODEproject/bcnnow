# -*- coding: utf-8 -*-
"""Example of Flask and qrcode.

NOTE: by requirements image in memory!
"""
from apps.backend.api.v0.token_manager import TokenManager
from flask_restful import Resource
__author__ = 'Rohit Kumar'
__version__ = (0, 0, 1)

import sys
import flask
import qrcode
import io
from os import urandom
import json
from flask import request
from config.Config import Config
cfg = Config().get()

class IoTWalletLoginManager(Resource):
    def __init__(self, ):
        return

    def get(self, source):
        if(source=='qrcode'):
            return self.get_qrimg()
        elif(source=='link'):
            return self.get_link()
        else:
            return "Invalid!!"

    def post(self, source):
        if(source=='qrcode'):
            return self.get_qrimg()
        elif(source=='link'):
            return self.get_link()
        elif (source == 'validate'):
            try:
                if(request.is_json):
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


    def validateLogin(self,token,basic_parameters):
        try:
            tkn_manager = TokenManager()
            tkn_status=tkn_manager.validate_token(token)

            if(tkn_status=='1'):
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


    def random_qr(self,url='www.google.com'):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4)

        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        return img

    def get_new_token(self):
        #generate new token
        tkn=urandom(12).hex()
        tkn_manager=TokenManager()
        if(tkn_manager.insert_token(tkn)):
            return  tkn
        else:
            return None


    def get_qrimg(self):
        token=self.get_new_token()
        header=cfg['iotconfig']['header']
        callback=cfg['iotconfig']['callbackurl']
        data = 'decodewallet://?action=login&header =%s&sessionId=%s&callback=%s' % (header, token, callback)
        img_buf = io.BytesIO()
        img = self.random_qr(url=data)
        img.save(img_buf)
        img_buf.seek(0)

        return flask.send_file(img_buf, mimetype='image/png')


    def get_link(self):
        token=self.get_new_token()
        header=cfg['iotconfig']['header']
        callback=cfg['iotconfig']['callbackurl']
        data= 'decodewallet://?action=login&header =%s&sessionId=%s&callback=%s'%(header,token,callback)
        return data

