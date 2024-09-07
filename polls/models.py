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
    """ Represents a poll question. """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def was_published_recently(self):
        """ Returns True if the question was published within the last day. """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """ Returns True if the current date and time is on or
        after the question's publication date. """
        now = timezone.localtime(timezone.now())
        return now >= self.pub_date

    def can_vote(self):
        """ Returns True if voting is allowed for this question. """
        now = timezone.localtime(timezone.now())
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date

    def is_voting_allowed(self):
        """ Returns True if voting is allowed. """
        now = timezone.now()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """ Represents a choice for a poll question. """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def vote(self):
        """return the votes for this choice"""
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted for {self.choice.choice_text}"
