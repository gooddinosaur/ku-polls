"""
Models for the polls app.

This module defines the database schema for the polls application, including
the Question and Choice models.
"""
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Represents a poll question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def was_published_recently(self):
        """
        Return True if the question was published within the last day.

        Checks whether the question's publication date is within the
        past 24 hours.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Return True if the question has been published.

        This method checks if the current date and time is on or after
        the question's publication date.
        """
        now = timezone.localtime(timezone.now())
        return now >= self.pub_date

    def can_vote(self):
        """
        Return True if voting is allowed for this question.

        Voting is allowed if the current time is between the publication
        date and the end date (if provided).
        """
        now = timezone.localtime(timezone.now())
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        """Return a string represents the question."""
        return self.question_text


class Choice(models.Model):
    """Represents a choice for a poll question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def vote(self):
        """Return the votes for this choice."""
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return a string represents the choice."""
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string that indicates which user voted for which choice."""
        return f"{self.user.username} voted for {self.choice.choice_text}"
