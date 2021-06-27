"""Test message model"""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class MessageModelTestCases(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.user_id = 11111
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.user_id
        db.session.commit()

        self.u = User.query.get(self.user_id)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_model(self):
        message = Message(text = "hi", user_id = self.user_id)

        db.session.add(message)
        db.session.commit()

        print('ug')
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "hi")


    def test_likes(self):
        m1 = Message(text = "ola", user_id=self.user_id)

        m2 = Message(text = "como como como", user_id=self.user_id)

        u = User.signup("testuser", "e@e.com", "123456", None)
        user_id = 2222
        u.id = user_id
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        likes = Likes.query.filter(Likes.user_id == user_id).all()
        self.assertEqual(len(likes), 1)
        self.assertEqual(likes[0].message_id, m1.id)