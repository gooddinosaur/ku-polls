"""
Models for the polls app.

This module defines the database schema for the polls application, including
the Question and Choice models.
"""
import datetime
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
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
