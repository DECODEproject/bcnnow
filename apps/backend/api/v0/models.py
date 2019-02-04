import time
import hashlib
from flask_sqlalchemy import SQLAlchemy
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from sqlalchemy.sql import select

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(65))
    profile_name = db.Column(db.String(45))
    profile_title = db.Column(db.String(45))
    profile_city = db.Column(db.String(45))
    profile_age = db.Column(db.String(45))
    profile_area = db.Column(db.String(45))
    profile_community = db.Column(db.String(45))
    iot_user_id = db.Column(db.String(45))
    community_id = db.Column(db.String(45))
    login_method = db.Column(db.String(45))

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, user_password):
        # password, salt = self.password.split(':')
        return self.password == hashlib.sha256(user_password.encode()).hexdigest()

    @staticmethod
    def crate_user(username, login_method='internal'):
        user = User()
        user.username = username
        user.login_method = login_method
        db.session.add(user)
        db.session.commit()


class DataSet(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    typeof = db.Column(db.String(45))


class DataSetCommunity(db.Model):
    __tablename__ = 'dataset_community'
    dataset_id = db.Column('dataset_id', db.Integer, db.ForeignKey("dataset.id"), primary_key=True)
    community_id = db.Column('community_id', db.String(45), primary_key=True)


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()

    @staticmethod
    def revoke_token(token_value):
        token = OAuth2Token.query.filter_by(access_token=token_value).first()
        token.revoked = True
        db.session.add(token)
        db.session.commit()

