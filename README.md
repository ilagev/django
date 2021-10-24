# Overview

Basic app to learn Python, Django and GraphQL.

Rules:

* Questions can have multiple choices
* Users can respond to many choices
* Choices can be responded by many users
* Each choice belongs to a single question

# Installation

```bash
git clone https://...
```

# Run server

```bash
source ~/.virtualenvs/djangodev/bin/activate
python manage.py runserver
````

# Updating database

```bash
python manage.py makemigrations polls
python manage.py sqlmigrate polls <id>
python manage.py migrate
```

# Reference links

## Django

* [Tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)
* [Related objects reference](https://docs.djangoproject.com/en/3.2/ref/models/relations/)
* [Models](https://docs.djangoproject.com/en/3.2/topics/db/models/#intermediary-manytomany)


## GraphQL

* [Tutorial](https://www.youtube.com/watch?v=kP7wQoFXUSc&list=PLOLrQ9Pn6caxz00JcLeOR-Rtq0Yi01oBH)
* [Graphene](https://docs.graphene-python.org/projects/django/en/latest/queries/)

## Mutation example

```graphql
mutation {
  updateQuestion(text: "What's up?") {
    question {
      questionText
    }
  }
}
```

## Query example

```graphql
query {
  allChoices {
    question {
      id
      questionText
    }
    votes
    choiceText
  }
  allQuestions {
    questionText
    pubDate
  }
  question(id: 2) {
    questionText
  }
  choicesOfQuestion(questionId: 1) {
    choiceText
    votes
  }
  filteredQuestions(substring: "age") {
    questionText
  }
}
```