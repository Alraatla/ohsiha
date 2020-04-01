from django.db import models

class Goat(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    breed = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# class Heard(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     goats =
