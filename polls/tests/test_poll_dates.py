import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date is in the future.
        """
        future_time = timezone.now() + datetime.timedelta(days=5)
        future_question = Question(question_text='Future question.',
                                   pub_date=future_time)
        future_question.save()
        self.assertFalse(future_question.is_published())

    def test_is_published_with_default_pub_date(self):
        """
        is_published() returns True for questions with the default pub_date (now).
        """
        now = timezone.localtime(timezone.now())
        default_question = Question(question_text='Default pub date question.',
                                    pub_date=now)
        default_question.save()
        self.assertTrue(default_question.is_published())

    def test_is_published_with_past_question(self):
        """
        is_published() returns True for questions whose pub_date is in the past.
        """
        past_time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text='Past question.',
                                 pub_date=past_time)
        past_question.save()
        self.assertTrue(past_question.is_published())

    def test_cannot_vote_before_pub_date(self):
        """Cannot vote if the current date is before the publication date."""
        future_question = Question(
            pub_date=timezone.now() + datetime.timedelta(days=1))
        self.assertFalse(future_question.can_vote())

    def test_can_vote_within_voting_period(self):
        """Can vote if the current date is within the publication date and end date."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=1)
        active_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertTrue(active_question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """Cannot vote if the current date is after the end date."""
        pub_date = timezone.now() - datetime.timedelta(days=2)
        end_date = timezone.now() - datetime.timedelta(days=1)
        expired_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertFalse(expired_question.can_vote())

    def test_can_vote_if_no_end_date(self):
        """Can vote if there is no end date set."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        no_end_date_question = Question(pub_date=pub_date)
        self.assertTrue(no_end_date_question.can_vote())


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
