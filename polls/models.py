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
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        """ Returns True if the question was published within the last day. """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """ Represents a choice for a poll question. """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
