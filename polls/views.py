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
from .models import Choice, Question


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
    """ Displays details for a specific question. """
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


class ResultsView(generic.DetailView):
    """ Displays the results for a specific question. """
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """ Handles voting on a specific question by updating the selected choice's
    vote count. Redirects to the results page or shows an error if no choice
    was selected. """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Voting is not allowed for this poll.")
        return redirect('polls:index')
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,)))
