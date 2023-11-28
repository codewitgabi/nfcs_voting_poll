from django.db import models
import uuid


class Contestant(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=35)
    image = models.ImageField(upload_to="db_img")

    def __str__(self):
        return self.name


class Voter(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.phone


class Category(models.Model):
    name = models.CharField(max_length=50)
    contestants = models.ManyToManyField(Contestant)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)

    def __str__(self):
        return self.voter.phone
