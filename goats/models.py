from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
# from ai.middleware.current_user import CommonInfo

class Goat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
            # settings.AUTH_USER_MODEL,
            # on_delete=models.CASCADE,
            # null=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if not self.owner:
    #         self.owner = self.request.user
    #         super(Goat, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class GoatAdmin(admin.ModelAdmin):
#     fields = ('name','age','breed',)
#     def save_model(self, request, obj, form, change):
#         obj.owner = request.user
#         obj.save()
