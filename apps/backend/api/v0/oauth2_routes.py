#!/usr/bin/env python
# -*- coding: utf-8 -*

from random import randint

from flask import request, session
from flask import render_template, redirect, jsonify, json, abort
from flask_restful import Resource
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from authlib.specs.rfc6749 import OAuth2Error
from apps.backend.api.v0.models import db, User, OAuth2Client, OAuth2Token
from apps.backend.api.v0.oauth2 import authorization, require_oauth
from apps.backend.api.v0.iot_login import IoTWalletLoginManager
from werkzeug.datastructures import ImmutableMultiDict
from config.config import Config
from base64 import b64encode

__author__ = 'Jordi Allué'
__version__ = (0, 0, 1)

cfg = Config().get()


class OAuthManager(Resource):

    def get(self, source):
        if source == 'user_info':
            return self.current_user()
        elif source == 'iot_login':
            return self.login_with_iot()
        elif source == 'check_login':
            return self.check_login()
        else:
            return "Invalid!!"

    def post(self, source):
        if source == 'login':
            return self.issue_token()
        elif source == 'iot_login_callback':
            return self.login_with_iot_callback()
        else:
            return "Invalid!!"

    @require_oauth('profile')
    def current_user(self):
        user = self.api_me()
        return user

    @staticmethod
    def home():
        if request.method == 'POST':
            data = request.json
            username = data['username']
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username)
                db.session.add(user)
                db.session.commit()
            session['id'] = user.id
            return redirect('/')
        user = OAuthManager.current_user()
        if user:
            clients = OAuth2Client.query.filter_by(user_id=user.id).all()
        else:
            clients = []
        # response = authorization.create_token_response()  #render_template('home.html', user=user, clients=clients)
        return "Success"

    @staticmethod
    def logout():
        del session['id']
        return redirect('/')

    @staticmethod
    def create_client():
        # user = OAuthManager.current_user()
        # if not user:
        #     return redirect('/')
        # if request.method == 'GET':
        #    return render_template('create_client.html')
        client = OAuth2Client()
        client.user_id = 1
        client.client_id = gen_salt(24)
        if client.token_endpoint_auth_method == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)
        db.session.add(client)
        db.session.commit()
        return redirect('/')

    @staticmethod
    def authorize():
        user = OAuthManager.current_user()
        if request.method == 'GET':
            try:
                grant = authorization.validate_consent_request(end_user=user)
            except OAuth2Error as error:
                return error.error
            return render_template('authorize.html', user=user, grant=grant)

        data = request.json
        username = data['username']
        user = User.query.filter_by(username=username).first()

        grant_user = user
        response = authorization.create_authorization_response(grant_user=grant_user)
        return response

    @staticmethod
    def issue_token():
        return authorization.create_token_response(request)

    @staticmethod
    def revoke_token():
        return authorization.create_endpoint_response('revocation')

    @staticmethod
    def login_with_iot():

        # get the info of the user and the link from iotlogin library
        iot_login_info = IoTWalletLoginManager.get_qrimg()

        # create user for oit session
        User.crate_user(iot_login_info['session'], 'iot')

        return {"qr": iot_login_info['qr'], "session": iot_login_info['session'], "url": iot_login_info['url']}

    @staticmethod
    def login_with_iot_callback():

        # username: AzrWLH8xw1xGYoPBBt1lP4xl
        # password: V2CQt67jOXTpeV4BrDMumQOcka1HEpQmDWp72l1mnutz52j8

        data = request.json
        # TODO: process data
        session_token = data['sessionId']

        # TODO: do magic auth algorithm

        # if 3rd party magic algorithm success create oauth2 token else return error
        number = randint(0, 9)
        if number > 0:
            # login
            request.headers.environ['HTTP_AUTHORIZATION'] = \
                'Basic ' + b64encode(bytes(cfg['oauth']['client_username'] + ':'
                                           + cfg['oauth']['client_password'], 'utf-8')).decode('utf-8')

            data2 = ImmutableMultiDict([('grant_type', 'password'), ('username', session_token),
                                        ('scope', 'profile'), ('password', 'dummy')])
            request.form = data2

            token = authorization.create_token_response(request)
            return token
        else:
            response = jsonify(message="IoT returned invalid authentication")
            response.status_code = 401
            return response

    @staticmethod
    def check_login():
        data = request.args
        username = data['session']
        user = User.query.filter_by(username=username).one()

        # given a username check if it has a token created for him
        try:
            token = OAuth2Token.query.filter_by(user_id=user.id).one()

            return {"status": True,
                    "access_token": token.access_token,
                    "expires_in": token.expires_in,
                    "refresh_token": token.refresh_token,
                    "scope": token.scope,
                    "token_type": token.token_type}
        except MultipleResultsFound as e:
            message = format(e)
            print(message)
            return {"status": False, "message": message}
        except NoResultFound as e:
            message = format(e)
            print(message)
            return {"status": False, "message": message}

    @staticmethod
    def get_current_user():
        return current_token.user

    def api_me(self):
        user = self.get_current_user()
        return jsonify(id=user.id, username=user.username, name=user.profile_name, city=user.profile_city,
                       age=user.profile_age, area=user.profile_area, community=user.profile_community)