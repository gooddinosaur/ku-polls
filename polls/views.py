"""
Views for the polls app.

Handles displaying questions, their details, and results, as well as processing
votes.
"""
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
    """ Displays a list of the latest published questions. """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll_status'] = {
            question.id: 'Open' if question.can_vote() else 'Closed' for
            question in context['latest_question_list']}
        return context


class DetailView(generic.DetailView):
    """ Display the choices for a poll and allow voting."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        """Check if voting is allowed; if not, redirect to index
        with an error message."""
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return redirect('polls:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Add the user's previous vote to the context. """
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            previous_vote = Vote.objects.filter(user=user,
                                                choice__question=question).first()
            context['previous_vote'] = previous_vote
        return context


class ResultsView(generic.DetailView):
    """ Displays the results for a specific question. """
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """ Handles voting on a specific question by updating the selected choice's
    vote count. Redirects to the results page or shows an error if no choice
    was selected. """
    user = request.user
    logger.info(f"User {user.username} is voting on question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        logger.warning(
            f"User {user.username} tried to vote on closed question {question_id}")
        messages.error(request, "Voting is not allowed for this poll.")
        return redirect('polls:index')
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        logger.info(
            f"User {user.username} selected choice {selected_choice.id}")
    except (KeyError, Choice.DoesNotExist):
        logger.error(f"Choice does not exist for question {question_id}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    # Check if the user has already voted for this question
    existing_vote = Vote.objects.get(user=user, choice__question=question)
    if existing_vote:
        # Update the existing vote
        logger.info(
            f"User {user.username} is updating their vote to choice "
            f"{selected_choice.id} on question {question_id}")
        existing_vote.choice = selected_choice
        existing_vote.save()
    else:
        # Create a new vote
        logger.info(
            f"User {user.username} is vote to choice {selected_choice.id} "
            f"on question {question_id}")
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
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
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
