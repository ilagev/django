import graphene
from graphene.types import schema
from graphene_django import DjangoObjectType, fields
from .models import Question, Choice

# Types

class QuestionsType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date')

class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ('choice_text', 'question', 'votes')

# Queries

class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionsType)
    all_choices = graphene.List(ChoiceType)

    def resolve_all_questions(root, info):
        return Question.objects.all()

    def resolve_all_choices(root, info):
        return Choice.objects.all()
    

schema = graphene.Schema(query=Query)