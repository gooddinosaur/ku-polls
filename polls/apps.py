"""
Polls app configuration.

This module contains the configuration for the poll application.
"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Configuration for the Polls application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
