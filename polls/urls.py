from django.urls import path

from polls import schema

from . import views
from graphene_django.views import GraphQLView
from .schema import schema

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema), name='graphql'),
]