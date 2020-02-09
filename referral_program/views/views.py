from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import User, Referral

from pyramid.httpexceptions import exception_response
from pyramid.view import view_config
import io
import uuid


class ReferralViews(object):
    """A class for all views related to referrals views"""
    def __init__(self, request):
        self.request = request
        self.view_name = 'refViews'

    @view_config(route_name='hello', request_method='GET', renderer='json')
    def hello_world(self):
        """A quick hello world to get things started"""
        return {"response": "Hello World!"}

    @view_config(route_name='create_user', request_method='POST', renderer='json')
    def create_user(self):
        """Create new user"""
        try:
            email = self.request.params['email']
            new_user = User(email=email)
            db = self.request.dbsession
            db.add(new_user)
            db.flush()
            db.refresh(new_user)
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'id': new_user.id}

    @view_config(route_name='create_referral', request_method='POST',renderer='json')
    def create_referral(self):
        """Create new referral"""
        try:
            user_id = self.request.matchdict['user_id']
            new_referral = Referral(id=uuid.uuid4(), user_id=user_id)
            db = self.request.dbsession
            db.add(new_referral)
            db.flush()
            db.refresh(new_referral)
        except DBAPIError as db_error:
            import pdb;pdb.set_trace()
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'referral': str(new_referral.id)}
