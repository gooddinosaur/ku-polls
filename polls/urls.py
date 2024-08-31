from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'polls'

urlpatterns = [
    path('', RedirectView.as_view(url='/polls/', permanent=True),
         name='redirect_to_polls'),
    path('polls/', views.IndexView.as_view(), name='index'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(),
         name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
]
