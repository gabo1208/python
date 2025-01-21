from django.db import models


class GameOption(models.Model):
    quote = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="")
    option1 = models.CharField(max_length=200, default="")
    option2 = models.CharField(max_length=200, default="")
    option3 = models.CharField(max_length=200, default="")
    option4 = models.CharField(max_length=200, default="")
