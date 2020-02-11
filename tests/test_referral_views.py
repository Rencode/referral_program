import unittest
from pyramid import testing
import sqlalchemy
from referral_program.models import Referral
from mockito import when, mock, unstub, ANY, verify
from uuid import UUID
from sqlalchemy.exc import DBAPIError, IntegrityError


class ReferralViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        unstub()

    def test_create_referral(self):
        from referral_program.views.views import ReferralView

        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.matchdict['user_id'] = '777'
        request.dbsession = mock(sqlalchemy.orm.session.Session)
        when(request.dbsession).add(ANY(Referral))
        when(request.dbsession).flush()
        when(request.dbsession).refresh(ANY(Referral))

        view_being_tested = ReferralView(request)

        response = view_being_tested.create_referral()
        referral = response['referral']

        # validate the value returned is valid UUID
        referral_uuid = UUID(referral, version=4)

    def test_create_referral_with_invalid_user(self):
        from referral_program.views.views import ReferralView

        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.matchdict['user_id'] = '777'
        request.dbsession = mock(sqlalchemy.orm.session.Session)
        when(request.dbsession).add(ANY(Referral))
        err = IntegrityError('', params=None, orig=None)
        err.args = [
            '''(psycopg2.errors.ForeignKeyViolation) insert or update on table "referral" violates foreign key constraint "fk_referral_user_id_user"\nDETAIL:  Key (user_id)=(360) is not present in table "user".\n
        ''']
        when(request.dbsession).flush().thenRaise(err)

        view_being_tested = ReferralView(request)
        response = view_being_tested.create_referral()

        self.assertEqual(response.status_code, 400)
