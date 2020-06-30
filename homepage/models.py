from django.db import models

# Create your models here.

class Question(models.Model):
    content = models.CharField(max_length=200, default="Em an com chua")


    def __str__(self):
        return self.content


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    vote = models.IntegerField(default=0)

    def __str__ (self):
        return self.question.content

