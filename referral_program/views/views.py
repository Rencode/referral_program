from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError, IntegrityError

from ..models import User, Referral

from pyramid.httpexceptions import exception_response
from pyramid.view import view_config
import io
import re
import uuid
from uuid import UUID


class ReferralView(object):
    """A class for all views related to referrals and users"""
    def __init__(self, request):
        self.request = request
        self.view_name = 'refViews'

    @view_config(route_name='hello', request_method='GET', renderer='json')
    def hello_world(self):
        """A quick hello world to get things started"""
        return {"response": "Hello World!"}

    # All currency values are store in minor currency (cents)
    SIGNUP_REWARD = 1000
    REWARD_PER_REFERRAL = 1000
    EMAIL_REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    NUM_REFERRALS_PER_REWARD = 5

    @view_config(route_name='create_user', request_method='POST', renderer='json')
    def create_user(self):
        """Create new user

        This view creates a new user based on the following request params:
        * email :
            The email of the new user to be created
        * referral : optional
            A referral token created by another user
        """

        email = self.request.params.get('email')
        if not re.search(self.EMAIL_REGEX, email):
            return exception_response(400, explanation='Invalid email address')

        referral = self.request.params.get('referral')
        if referral:
            try:
                UUID(referral, version=4)
            except ValueError:
                return exception_response(400, explanation='Invalid referral')

            new_user = User(email=email, referral=referral, balance=self.SIGNUP_REWARD)
        else:
            new_user = User(email=email)

        try:
            db = self.request.dbsession
            db.add(new_user)

            if referral:
                referral_obj = db.query(Referral).filter_by(id=referral).first()
                referral_obj.num_referrals += 1

                referring_user = db.query(User).filter_by(id=referral_obj.user_id).first()
                referring_user.total_referrals += 1
                referring_user.balance = \
                    referring_user.total_referrals // self.NUM_REFERRALS_PER_REWARD * self.REWARD_PER_REFERRAL

            db.flush()
            db.refresh(new_user)

        except IntegrityError as integrity_error:
            explanation = integrity_error.args[0].split('DETAIL: ')[1]
            return exception_response(400, explanation=explanation)
        except DBAPIError as db_error:
            return exception_response(500)
        return {'id': new_user.id}

    @view_config(route_name='create_referral', request_method='POST',renderer='json')
    def create_referral(self):
        """Create new referral

        This view creates a new referral token and takes the following request params:
        * user_id:
            the used id of the user creating the referral token
        """
        try:
            user_id = self.request.matchdict['user_id']
            new_referral = Referral(id=uuid.uuid4(), user_id=user_id)
            db = self.request.dbsession
            db.add(new_referral)
            db.flush()
            db.refresh(new_referral)
        except DBAPIError as db_error:
            explanation = db_error.args[0].split('DETAIL: ')[1]
            return exception_response(400, explanation=explanation)
        return {'referral': str(new_referral.id)}
