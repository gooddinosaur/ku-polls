"""
Views for the polls app.

Handles displaying questions, their details, and results, as well as processing votes.
"""
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone
from django.template import loader


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


class DetailView(generic.DetailView):
    """ Displays details for a specific question. """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """ Displays the results for a specific question. """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """ Handles voting on a specific question by updating the selected choice's
    vote count. Redirects to the results page or shows an error if no choice
    was selected. """
    question = get_object_or_404(Question, pk=question_id)
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
