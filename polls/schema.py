import graphene
from graphene.types import schema
from graphene_django import DjangoObjectType, fields
from .models import Question, Choice

# Types

class QuestionsType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date')

class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'question', 'votes')

# Queries

class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionsType)
    all_choices = graphene.List(ChoiceType)
    question = graphene.Field(QuestionsType, id=graphene.Int())
    choices_of_question = graphene.List(ChoiceType, questionId=graphene.Int())
    filtered_questions = graphene.List(QuestionsType, substring=graphene.String())

    def resolve_all_questions(root, info):
        return Question.objects.all()   

    def resolve_all_choices(root, info):
        return Choice.objects.all()

    def resolve_question(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_choices_of_question(root, info, questionId):
        return Choice.objects.filter(question_id=questionId)

    def resolve_filtered_questions(root, info, substring):
        return Question.objects.filter(question_text__contains=substring)
    
schema = graphene.Schema(query=Query)