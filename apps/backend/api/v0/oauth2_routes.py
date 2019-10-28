#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
from random import randint

from datetime import date
from flask import request, session, current_app
from flask import render_template, redirect, jsonify, json, abort
from flask_restful import Resource
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from authlib.specs.rfc6749 import OAuth2Error
from zenroom import zenroom
import requests
from apps.backend.api.v0.models import db, User, OAuth2Client, OAuth2Token, Community
from apps.backend.api.v0.oauth2 import authorization, require_oauth
from apps.backend.api.v0.iot_login import IoTWalletLoginManager
from werkzeug.datastructures import ImmutableMultiDict

from apps.backend.api.v0.token_manager import TokenManager
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
        try:
            return authorization.create_token_response(request)
        except Exception as e:
            current_app.logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            current_app.logger.error("Error description: " + str(e))
        return

    @staticmethod
    def revoke_token():
        return authorization.create_endpoint_response('revocation')

    @staticmethod
    def login_with_iot():

        # get the info of the user and the link from iotlogin library
        iot_login_info = IoTWalletLoginManager.get_qrimg()

        # create user for oit session
        User.crate_user(iot_login_info['session'], 'iot')

        return {"session": iot_login_info['session'],
                "dddc_qr": iot_login_info['dddc_qr'],
                "dddc_url": iot_login_info['dddc_url'],
                "iot_qr": iot_login_info['iot_qr'],
                "iot_url": iot_login_info['iot_url']}

    @staticmethod
    def login_with_iot_callback():

        # username: AzrWLH8xw1xGYoPBBt1lP4xl
        # password: V2CQt67jOXTpeV4BrDMumQOcka1HEpQmDWp72l1mnutz52j8

        data = request.json
        session_token = data['sessionId']

        districts = {
            "1": "Ciutat Vella",
            "2": "Eixample",
            "3": "Sants-Montjuïc",
            "4": "Les Corts",
            "5": "Sarrià-Sant Gervasi",
            "6": "Gràcia",
            "7": "Horta-Guinardó",
            "8": "Nou Barris",
            "9": "Sant Andreu",
            "10": "Sant Martí",
        }

        try:
            contract = """Scenario coconut: verify proof
            Given that I have a valid 'verifier' from 'issuer_identifier'
            and I have a valid 'credential proof'
            When I aggregate the verifiers
            and I verify the credential proof
            Then print 'Success' 'OK' as 'string'
                    """

            current_app.logger.info("starting callback")
            authorizable_attribute_id = data['credential']['authorizable_attribute_id']
            current_app.logger.info("authorizable_attribute_id: " + authorizable_attribute_id)
            credential_issuer_endpoint_address = data['credential']['credential_issuer_endpoint_address']
            current_app.logger.info("credential_issuer_endpoint_address: " + credential_issuer_endpoint_address)

            # read the public key from endpoint
            bcn_community_obj = Community.get_from_authorizable_attribute_id(authorizable_attribute_id)
            # print("bcn_community_obj: " + bcn_community_obj)
            current_app.logger.info("URL: " + credential_issuer_endpoint_address + "/authorizable_attribute/{}".format(
                authorizable_attribute_id))
            res = requests.get(
                credential_issuer_endpoint_address + "/authorizable_attribute/{}".format(authorizable_attribute_id))
            if res.ok:

                credential_key = json.dumps(res.json()["verification_key"])
                value = json.dumps(data['credential']['value'])
                ## check with zenroom if login is valid
                verify_response_msg = "OK"
                current_app.logger.info("\tvalue: {}".format(value))
                current_app.logger.info("\tAll good, got this result: {}".format(res.json()))
                if cfg['iotconfig']['bypass'] == 'no':
                    with open('verifyer.zencode') as file:
                        verify_credential_script = file.read()
                    try:
                        verify_response = zenroom.zencode_exec(contract, data=credential_key, keys=value.replace('"proof"','"credential_proof"'))
                        verify_response_stdout = verify_response.stdout
                        print("response: " + verify_response_stdout)

                        if(verify_response_stdout.find("OK")!=-1):
                            verify_response_msg="OK"
                        else:
                            verify_response_msg="not OK"
                    except Exception as e:
                        print("Error in zenroom")
                        

                if verify_response_msg == "OK":
                    tkn_manager = TokenManager()
                    tkn_status = tkn_manager.validate_token(session_token)
                    print("token status "+tkn_status)
                    if tkn_status == '1':
                        # login
                        print("valid token creating auth")
                        request.headers.environ['HTTP_AUTHORIZATION'] = \
                            'Basic ' + b64encode(bytes(cfg['oauth']['client_username'] + ':'
                                                       + cfg['oauth']['client_password'], 'utf-8')).decode('utf-8')

                        data2 = ImmutableMultiDict([('grant_type', 'password'), ('username', session_token),
                                                    ('scope', 'profile'), ('password', 'dummy')])
                        request.form = data2
                        print("request data created.")


                        # Get personal data
                        name = ""
                        city = "Barcelona"
                        age = ""
                        area = ""
                        profile_data_array = data['optionalAttributes']
                        for profile_data in profile_data_array:
                            if profile_data['attribute_id'] == "schema:dateOfBirth":
                                # process age dd/mm/yyyy
                                day, month, year = profile_data['value'].split('/')
                                today = date.today()
                                age = today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))
                            if profile_data['attribute_id'] == "schema:name":
                                name = profile_data['value']
                            if profile_data['attribute_id'] == "schema:city":
                                city = profile_data['value']
                            if profile_data['attribute_id'] == "schema:district":
                                if profile_data['value'] in districts:
                                    area = districts[profile_data['value']]

                        User.update_user(session_token, name, city, age, area)
                        print("User updated")
                        User.user_add_community(session_token, bcn_community_obj.id)
                        print("User added to community")
                        
                        headers = {'Authorization': 'Basic QXpyV0xIOHh3MXhHWW9QQkJ0MWxQNHhsOlYyQ1F0NjdqT1hUcGVWNEJyRE11bVFPY2thMUhFcFFtRFdwNzJsMW1udXR6NTJqOA=='} #  + b64encode(bytes(cfg['oauth']['client_username'] + ':' + cfg['oauth']['client_password'], 'utf-8')).decode('utf-8')}
                        PARAMS = {'grant_type': 'password', 'username': session_token, 'scope': 'profile', 'password': 'dummy'}
                        r = requests.post(url='http://84.88.76.45:887/oauth/login', params=PARAMS, headers=headers)
                        data = r.json()
                        response = jsonify(message="Logged OK")
                        response.status_code = 200
                        return response
                        
                        # token = authorization.create_token_response(request)
                        # print("token created")
                        # return token
                    else:
                        response = jsonify(message="Invalid Token")
                        response.status_code = 401
                        return response
                else:
                    response = jsonify(message="Invalid Credentials")
                    response.status_code = 401
                    return response
            else:
                current_app.logger.info("\tCalls not getting back, got this error: {}".format(res.json()))
                response = jsonify(message="Could not get public key data from credential_issuer_endpoint_address")
                response.status_code = 412
                return response
        except Exception as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            response = jsonify(message="Unexpected Error in Validation")
            response.status_code = 412
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
            current_app.logger.error("Error description: " + message)
            return {"status": False, "message": message}
        except NoResultFound as e:
            message = format(e)
            current_app.logger.error("Error description: " + message)
            return {"status": False, "message": message}

    @staticmethod
    def get_current_user():
        return current_token.user

    def api_me(self):
        user = self.get_current_user()
        return jsonify(id=user.id, username=user.username, name=user.profile_name, city=user.profile_city,
                       age=user.profile_age, area=user.profile_area, community=user.profile_community)
