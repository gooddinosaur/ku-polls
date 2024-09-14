"""
Registers the Question and Choice models with the Django admin interface,
enabling management of poll questions and choices.
"""

# Register your models here.
from django.contrib import admin
from polls.models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
