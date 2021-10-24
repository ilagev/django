import graphene
from django.utils import timezone
from graphene.types import schema
from graphene import ObjectType
from graphene.types.field import Field
from .models import Question, Choice, Response, User

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

class UserType(ObjectType):
    id = graphene.ID()
    name = graphene.String()
    responses = graphene.List(ChoiceType)

class ResponseType(ObjectType):
    id = graphene.ID()
    user = graphene.Field(UserType)
    choice = graphene.Field(ChoiceType)

# Queries

class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)
    all_choices = graphene.List(ChoiceType)
    all_users = graphene.List(UserType)
    all_responses = graphene.List(ResponseType)
    question = graphene.Field(QuestionType, id=graphene.Int())
    choices_of_question = graphene.List(ChoiceType, questionId=graphene.Int())
    responses_of_user = graphene.List(ResponseType, userId=graphene.Int())
    filtered_questions = graphene.List(QuestionType, substring=graphene.String())

    def resolve_all_questions(root, info):
        return Question.objects.all()   

    def resolve_all_choices(root, info):
        return Choice.objects.all()

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_responses(root, info):
        return Response.objects.all() 

    def resolve_question(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_choices_of_question(root, info, questionId):
        return Choice.objects.filter(question_id=questionId)

    def resolve_responses_of_user(root, info, userId):
        return Response.objects.filter(user_id=userId)

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

class ChoiceMutation(graphene.Mutation):
    
    class Arguments:
        text = graphene.String(required=True)
        question_id = graphene.Int()

    choice = graphene.Field(ChoiceType)

    @classmethod
    def mutate(cls, root, info, text, question_id):
        question = Question.objects.get(pk=question_id)
        choice = Choice(question=question, choice_text=text, votes=0)
        choice.save()
        return ChoiceMutation(choice=choice)

class UserMutation(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, name):
        user = User(name=name)
        user.save()
        return UserMutation(user=user)

class VoteMutation(graphene.Mutation):
    
    class Arguments:
        user_id = graphene.ID()
        choice_id = graphene.ID()

    response = graphene.Field(ResponseType)

    @classmethod
    def mutate(cls, root, info, user_id, choice_id):
        user = User.objects.get(pk=user_id)
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        response = Response(user=user, choice=choice)
        response.date = timezone.now()
        response.save()
        return VoteMutation(response=response)

class Mutation(graphene.ObjectType):
    update_question = QuestionMutation.Field()
    update_choice = ChoiceMutation.Field()
    update_user = UserMutation.Field()
    vote = VoteMutation.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)