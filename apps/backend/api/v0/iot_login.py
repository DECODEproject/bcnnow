# -*- coding: utf-8 -*-
"""Example of Flask and qrcode.

NOTE: by requirements image in memory!
"""
from apps.backend.api.v0.token_manager import TokenManager
from flask_restful import Resource
__author__ = 'Rohit Kumar'
__version__ = (0, 0, 1)


import flask
import qrcode
import io
import secrets
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
        tkn=secrets.token_urlsafe(20)
        tkn_manager=TokenManager()
        if(tkn_manager.insert_token(tkn)):
            return  tkn
        else:
            return None


    def get_qrimg(self):
        token=self.get_new_token()
        header=cfg['iotconfig']['header']
        callback=cfg['iotconfig']['callbackurl']
        data= 'decodewallet://login?header =%s&sessionId=%s&callback=%s'%(header,token,callback)

        img_buf = io.BytesIO()
        img = self.random_qr(url=data)
        img.save(img_buf)
        img_buf.seek(0)

        return flask.send_file(img_buf, mimetype='image/png')


    def get_link(self):
        token=self.get_new_token()
        header=cfg['iotconfig']['header']
        callback=cfg['iotconfig']['callbackurl']
        data= 'decodewallet://login?header =%s&sessionId=%s&callback=%s'%(header,token,callback)
        return data

