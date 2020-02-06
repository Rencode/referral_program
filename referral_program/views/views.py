from pyramid.httpexceptions import exception_response
from pyramid.view import view_config
import io


class ReferralViews(object):
    """A class for all views related to referrals views"""
    def __init__(self, request):
        self.request = request
        self.view_name = 'refViews'
        #self.mongo_db = mongo_db

    @view_config(route_name='hello', request_method='GET', renderer='json')
    def hello_world(self):
        """A quick hello world to get things started"""
        return {"response":"Hello World!"}
