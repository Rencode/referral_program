import unittest
from pyramid import testing
import transaction


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """On inherited classes, run our `setUp` method"""
        # Inspired via http://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class/17696807#17696807
        if cls is not BaseTest and cls.setUp is not BaseTest.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                BaseTest.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def setUp(self):
        from referral_program.models import get_tm_session
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('referral_program.models')
        self.config.include('referral_program.routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

    def init_database(self):
        from referral_program.models.meta import Base
        session_factory = self.config.registry['dbsession_factory']
        engine = session_factory.kw['bind']
        import pdb;pdb.set_trace()
        Base.metadata.create_all(engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def makeUser(self, email):
        from referral_program.models import User
        user = User(email=email)
        return user


class ReferralTest(BaseTest):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_create_referral(self):
        from referral_program.views.views import ReferralView

        # Add test user to the db
        user = self.makeUser('tester@testing.com')
        self.session.add(user)
        self.session.refresh(user)

        # Setup our dummy request before using it
        request = testing.DummyRequest()
        request.matchdict['user_id'] = user.id

        view_being_tested = ReferralView(request)

        response = view_being_tested.create_referral()
        self.assertEqual(response.status_code, 200)


# class ReferralTest(unittest.TestCase):
#
#     def setUp(self):
#         self.config = testing.setUp()
#
#     def tearDown(self):
#         testing.tearDown()
#
#     def test_create_referral(self):
#         from referral_program.views.views import ReferralViews
#
#         # Setup our dummy request before using it
#         request.matchdict['user_id'] = '777'
#         db
#         #     view = ApScanViews(request)
#         #     mongo_db = mock(mongo.MongoDb.InnerMongoDb)
#         #     when(mongo.MongoDb).InnerMongoDb().thenReturn(mongo_db)
#         #     when(mongo_db).get_ap_scan_batch(ANY(str)).thenReturn(
#         #         mongo_entry)
#         request = testing.DummyRequest()
#
#
#
#         view_being_tested = ReferralViews(request)
#
#         response = view_being_tested.create_referral()
#         self.assertEqual(response.status_code, 200)
