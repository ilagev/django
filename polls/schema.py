import graphene
from django.utils import timezone
from graphene.types import schema
from graphene import ObjectType
from graphene.types.field import Field
from .models import Question, Choice

# Types

class QuestionType(ObjectType):
    id = graphene.ID()
    question_text = graphene.String()
    pub_date = graphene.Date()

class ChoiceType(ObjectType):
    id = graphene.ID()
    choice_text = graphene.String()
    votes = graphene.Int()
    question = graphene.Field(QuestionType)

# Queries

class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)
    all_choices = graphene.List(ChoiceType)
    question = graphene.Field(QuestionType, id=graphene.Int())
    choices_of_question = graphene.List(ChoiceType, questionId=graphene.Int())
    filtered_questions = graphene.List(QuestionType, substring=graphene.String())

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

# Mutations

class QuestionMutation(graphene.Mutation):
    
    class Arguments:
        text = graphene.String(required=True)

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, text):
        question = Question(question_text=text)
        question.pub_date = timezone.now()
        question.save()
        return QuestionMutation(question=question)

class Mutation(graphene.ObjectType):
    update_question = QuestionMutation.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)