import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from time import sleep


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class CanVoteTest(TestCase):
    def test_can_vote_no_end_date(self):
        """A question without an end date and with a publication date in the
        past allows voting."""
        question = create_question("Past question without end date.", days=-5)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_future_question(self):
        """A question without an end date and with a publication date in the
        future does not allow voting."""
        question = create_question("Future question without end date.", days=5)
        self.assertFalse(question.can_vote())

    def test_can_vote_with_end_date(self):
        """
        A question with a publication date in the past and an end date in
        the future allows voting.
        """
        # Adjust the test to fit with the create_question function
        question = create_question("Question with end date.", days=-5)
        # Assuming you add end_date manually or have logic for it
        question.end_date = timezone.now() + datetime.timedelta(days=5)
        question.save()
        self.assertTrue(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        A question does not allow voting after its end date.
        """
        question = create_question("Question with past end date.", days=-10)
        # Adjust the test to fit with the create_question function
        question.end_date = timezone.now() - datetime.timedelta(days=5)
        question.save()
        self.assertFalse(question.can_vote())

    def test_can_vote_right_after_publishing(self):
        """A question allows voting right at the moment of its publication."""
        question = create_question("Question starts now.", days=0)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_right_after_closing(self):
        """A question does not allow voting right at the moment of its closing."""
        now = timezone.now()
        question = create_question("Question ended now.", days=-1)
        question.end_date = now
        question.save()
        sleep(1)
        self.assertFalse(question.can_vote())

    def test_future_question_with_future_end_date(self):
        """
        A question with both publication and end dates in the future does
        not allow voting.
        """
        question = create_question("Future question with future end date.",
                                   days=5)
        # Adjust the test to fit with the create_question function
        question.end_date = timezone.now() + datetime.timedelta(days=10)
        question.save()
        self.assertFalse(question.can_vote())
