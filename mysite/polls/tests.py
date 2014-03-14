import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Poll
# Create your tests here.

class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        future_poll = Poll(pub_date = timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

