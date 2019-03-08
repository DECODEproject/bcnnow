import datetime
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

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(65))
    profile_name = db.Column(db.String(45))
    profile_title = db.Column(db.String(45))
    profile_city = db.Column(db.String(45))
    profile_age = db.Column(db.String(45))
    profile_area = db.Column(db.String(45))
    profile_community = db.Column(db.String(45))
    iot_user_id = db.Column(db.String(45))
    community_id = db.Column(db.BigInteger)
    login_method = db.Column(db.String(45))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, user_password):
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
    id = db.Column(db.BigInteger, primary_key=True)
    typeof = db.Column(db.String(45))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(45))
    community_id = db.Column(db.String(45))
    authorizable_attribute_id = db.Column(db.String(45))
    credential_issuer_endpoint_address = db.Column(db.String(45))
    community_validation_key = db.Column(db.String(100))

    @staticmethod
    def create(community_name, community_id, authorizable_attribute_id, credential_issuer_endpoint_address):
        community = Community()
        community.community_id = community_id
        community.name = community_name
        community.authorizable_attribute_id = authorizable_attribute_id

        if credential_issuer_endpoint_address is not None:
            community.credential_issuer_endpoint_address = credential_issuer_endpoint_address

        db.session.add(community)
        db.session.commit()

        return community

    @staticmethod
    def update(bcn_community_id, community_validation_key):
        community = Community.query.filter_by(id=bcn_community_id).first()
        community.community_validation_key = community_validation_key

        db.session.add(community)
        db.session.commit()

        return community

    @staticmethod
    def get(bcn_community_id):
        community = Community.query.filter_by(id=bcn_community_id).first()
        return community

    @staticmethod
    def get_from_community_id(community_id):
        community = Community.query.filter_by(community_id=community_id).first()
        return community

    @staticmethod
    def get_from_authorizable_attribute_id(authorizable_attribute_id):
        community = Community.query.filter_by(authorizable_attribute_id=authorizable_attribute_id).first()
        return community


class Dashboard(db.Model):
    __tablename__ = 'dashboard'
    id = db.Column(db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    typeof = db.Column(db.String(45))

    @staticmethod
    def create(new_id, typeof):
        dashboard = Dashboard()
        dashboard.id = new_id
        dashboard.typeof = typeof
        db.session.add(dashboard)
        db.session.commit()

    @staticmethod
    def update(dashboard_id, typeof):
        dashboard = Dashboard.query.filter_by(id=dashboard_id).first()
        dashboard.typeof = typeof
        db.session.add(dashboard)
        db.session.commit()


class DataSetCommunity(db.Model):
    __tablename__ = 'dataset_community'
    dataset_id = db.Column('dataset_id', db.BigInteger, db.ForeignKey("dataset.id"), primary_key=True)
    community_id = db.Column('community_id', db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class DashboardCommunity(db.Model):
    __tablename__ = 'dashboard_community'
    dashboard_id = db.Column('dashboard_id', db.BigInteger, db.ForeignKey("dashboard.id"), primary_key=True)
    community_id = db.Column('community_id', db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def add_dashboard_to_community(dashboard_id, community_id):
        dashboard_community = DashboardCommunity()
        dashboard_community.dashboard_id = dashboard_id
        dashboard_community.community_id = community_id
        db.session.add(dashboard_community)
        db.session.commit()

    @staticmethod
    def remove_dashboard_from_community(dashboard_id, community_id):
        dashboard = DashboardCommunity.query.filter_by(dashboard_id=dashboard_id, community_id=community_id).first()
        db.session.delete(dashboard)
        db.session.commit()

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

