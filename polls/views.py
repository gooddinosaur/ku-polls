"""
Views for the polls app.

Handles displaying questions, their details, and results, as well as processing
votes.
"""
from django.contrib.auth.signals import user_logged_in, user_logged_out, \
    user_login_failed
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from polls.models import Choice, Question, Vote
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import logging

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    """Displays a list of the latest published questions."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return all questions published, ordered by publication date."""
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        """Get the context data and add poll status."""
        context = super().get_context_data(**kwargs)
        context['poll_status'] = {
            question.id: 'Open' if question.can_vote() else 'Closed' for
            question in context['latest_question_list']}
        return context


class DetailView(generic.DetailView):
    """Display the choices for a poll and allow voting."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        """Check if voting is allowed."""
        """If not, redirect to index with an error message."""
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return redirect('polls:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the user's previous vote to the context."""
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            previous_vote = Vote.objects.filter(
                user=user, choice__question=question).first()
            context['previous_vote'] = previous_vote
        return context


class ResultsView(generic.DetailView):
    """Displays the results for a specific question."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Return a response after handling voting on a specific question.

    This function updates the selected choice's vote count. It redirects
    to the results page or shows an error if no choice was selected.
    """
    user = request.user
    logger.info(f"User {user.username} is voting on question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    ip = get_client_ip(request)

    if not question.can_vote():
        logger.warning(
            f"User {user.username} tried to vote on closed question "
            f"{question_id} from {ip}")
        messages.error(request, "Voting is not allowed for this poll.")
        return redirect('polls:index')

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        logger.info(
            f"User {user.username} selected choice "
            f"{selected_choice.id} from {ip}")
    except (KeyError, Choice.DoesNotExist):
        logger.error(f"Choice does not exist for question {question_id}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    try:
        # Check if the user has already voted for this question
        existing_vote = Vote.objects.get(user=user, choice__question=question)
        # If the user has already voted, update the vote
        logger.info(
            f"User {user.username} is updating their vote to choice "
            f"{selected_choice.id} on question {question_id} from {ip}")
        existing_vote.choice = selected_choice
        existing_vote.save()
    except Vote.DoesNotExist:
        # If the user hasn't voted yet, create a new vote
        logger.info(
            f"User {user.username} is voting for choice {selected_choice.id} "
            f"on question {question_id} from {ip}")
        new_vote = Vote(user=user, choice=selected_choice)
        new_vote.save()

    # Show success message
    messages.success(request,
                     f"Your vote for '{selected_choice.choice_text}' "
                     f"has been recorded.")
    return HttpResponseRedirect(reverse("polls:results",
                                        args=(question.id,)))


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Get the cleaned form data
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password1')
            # Authenticate the new user
            user = authenticate(username=username, password=raw_passwd)
            if user is not None:
                # Log the user in and redirect them to the login page
                login(request, user)
                messages.success(request,
                                 'Registration successful. '
                                 'You are now logged in.')
                return redirect('polls:index')
        else:
            messages.error(request, 'Registration failed.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    """Login successful with the user's IP address."""
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged in from {ip_addr}")


@receiver(user_logged_out)
def logout_success(sender, request, user, **kwargs):
    """Logout successful with the user's IP address."""
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged out from {ip_addr}")


@receiver(user_login_failed)
def login_fail(sender, credentials, request, **kwargs):
    """Login failed with the user's IP address."""
    ip_addr = get_client_ip(request)
    logger.warning(
        f"Failed login for {credentials.get('username', 'unknown')} "
        f"from {ip_addr}")
