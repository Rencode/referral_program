import unittest
from pyramid import testing
import sqlalchemy
from referral_program.models import User, Referral
import referral_program.models.user
from mockito import when, mock, unstub, ANY, verify
from uuid import UUID
import uuid
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import query

from referral_program.views.views import ReferralView


class UserViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        unstub()

    def test_create_user_invalid_email(self):
        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.params['email'] = 'brokenemail.com'

        view_being_tested = ReferralView(request)

        response = view_being_tested.create_user()

        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_referral(self):
        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.params['email'] = 'arbemail@email.com'
        request.params['referral'] = '12345678'

        view_being_tested = ReferralView(request)

        response = view_being_tested.create_user()

        self.assertEqual(response.status_code, 400)

    def test_create_user_non_existing_referral(self):
        """  For this test we use a uuid which is not in the system """
        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.params['email'] = 'arbemail@email.com'
        test_uuid = str(uuid.uuid4())
        request.params['referral'] = test_uuid

        request.dbsession = mock(sqlalchemy.orm.session.Session)
        err = IntegrityError('', params=None, orig=None)
        err.args = [
            '''(psycopg2.errors.ForeignKeyViolation) insert or update on table "referral" violates foreign key constraint "fk_referral_user_id_user"\nDETAIL:  Key (user_id)=(360) is not present in table "user".\n
        ''']
        when(request.dbsession).add(ANY(User)).thenRaise(err)

        view_being_tested = ReferralView(request)
        response = view_being_tested.create_user()

        self.assertEqual(response.status_code, 400)

    def test_create_user_no_referral(self):
        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.params['email'] = 'arbemail@email.com'
        request.dbsession = mock(sqlalchemy.orm.session.Session)
        mock_user = mock(User)
        mock_user.id = 1
        # TODO: take another look at mocking this constructor
        when(referral_program.models.user).User(email=ANY(str)).thenReturn(mock_user)
        when(request.dbsession).add(ANY(User))
        when(request.dbsession).flush()
        when(request.dbsession).refresh(ANY(User))

        view_being_tested = ReferralView(request)
        response = view_being_tested.create_user()

        self.assertEqual(response, {'id': None})

    def test_create_user_with_referral(self):
        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.params['email'] = 'arbemail@email.com'
        test_uuid = str(uuid.uuid4())
        request.params['referral'] = test_uuid

        mock_referral = mock(Referral)
        mock_referral.num_referrals = 0
        mock_referral.user_id = 1
        request.dbsession = mock(sqlalchemy.orm.session.Session)
        mock_user = mock(User)
        mock_user.id = 1
        # TODO: take another look at mocking this constructor
        when(referral_program.models.user).User(email=ANY(str)).thenReturn(mock_user)
        when(request.dbsession).add(ANY(User))
        mock_referral_query = query.Query([])
        when(request.dbsession).query(Referral).thenReturn(mock_referral_query)
        when(mock_referral_query).filter_by(id=ANY).thenReturn(mock_referral_query)
        when(mock_referral_query).first().thenReturn(mock_referral)
        mock_user_query = query.Query([])
        mock_referring_user = mock(User)
        mock_referring_user.total_referrals = 0
        mock_referring_user.balance = 0
        when(request.dbsession).query(User).thenReturn(mock_user_query)
        when(mock_user_query).filter_by(id=ANY).thenReturn(mock_user_query)
        when(mock_user_query).first().thenReturn(mock_referring_user)

        when(request.dbsession).flush()
        when(request.dbsession).refresh(ANY(User))

        view_being_tested = ReferralView(request)
        response = view_being_tested.create_user()
        self.assertEqual(mock_referral.num_referrals, 1)
        self.assertEqual(mock_referring_user.total_referrals, 1)
        self.assertEqual(mock_referring_user.balance, 0)
        self.assertEqual(response, {'id': None})

    def test_create_user_with_referral_increment_referrer_balance(self):
        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.params['email'] = 'arbemail@email.com'
        test_uuid = str(uuid.uuid4())
        request.params['referral'] = test_uuid

        mock_referral = mock(Referral)
        mock_referral.num_referrals = 0
        mock_referral.user_id = 1
        request.dbsession = mock(sqlalchemy.orm.session.Session)
        mock_user = mock(User)
        mock_user.id = 1
        # TODO: take another look at mocking this constructor
        when(referral_program.models.user).User(email=ANY(str)).thenReturn(mock_user)
        when(request.dbsession).add(ANY(User))
        mock_referral_query = query.Query([])
        when(request.dbsession).query(Referral).thenReturn(mock_referral_query)
        when(mock_referral_query).filter_by(id=ANY).thenReturn(mock_referral_query)
        when(mock_referral_query).first().thenReturn(mock_referral)
        mock_user_query = query.Query([])
        mock_referring_user = mock(User)
        mock_referring_user.total_referrals = 4
        mock_referring_user.balance = 0
        when(request.dbsession).query(User).thenReturn(mock_user_query)
        when(mock_user_query).filter_by(id=ANY).thenReturn(mock_user_query)
        when(mock_user_query).first().thenReturn(mock_referring_user)

        when(request.dbsession).flush()
        when(request.dbsession).refresh(ANY(User))

        view_being_tested = ReferralView(request)
        response = view_being_tested.create_user()
        self.assertEqual(mock_referral.num_referrals, 1)
        self.assertEqual(mock_referring_user.total_referrals, 5)
        self.assertEqual(mock_referring_user.balance, 1000)
        self.assertEqual(response, {'id': None})

    def test_create_user_with_non_existing_user(self):
        request = testing.DummyRequest()
        request.params['email'] = 'arbemail@email.com'
        test_uuid = str(uuid.uuid4())
        request.params['referral'] = test_uuid

        mock_referral = mock(Referral)
        mock_referral.num_referrals = 0
        mock_referral.user_id = 1
        request.dbsession = mock(sqlalchemy.orm.session.Session)
        mock_user = mock(User)
        mock_user.id = 1
        # TODO: take another look at mocking this constructor
        when(referral_program.models.user).User(email=ANY(str)).thenReturn(mock_user)
        when(request.dbsession).add(ANY(User))
        mock_referral_query = query.Query([])
        when(request.dbsession).query(Referral).thenReturn(mock_referral_query)
        err = IntegrityError('', params=None, orig=None)
        err.args = [
            '''(psycopg2.errors.ForeignKeyViolation) insert or update on table "referral" violates foreign key constraint "fk_referral_user_id_user"\nDETAIL:  Key (user_id)=(360) is not present in table "user".\n
        ''']
        when(mock_referral_query).filter_by(id=ANY).thenRaise(err)

        view_being_tested = ReferralView(request)
        response = view_being_tested.create_user()
        self.assertEqual(response.status_code, 400)