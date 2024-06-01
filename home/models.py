from django.db import models

from django import forms


class ServiceHoursForm(forms.Form):
    service_hours = forms.IntegerField(label='Service Hours')
    date = forms.DateField(label='Date (mm/dd/yyyy)')
    description = forms.CharField(label='Description', widget=forms.Textarea)


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    inductedDate = models.IntegerField(null=True, blank=True)
    numServiceHours = models.IntegerField(default=0)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Submission(models.Model):
    user = models.CharField(max_length=150)
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    service_hours = models.PositiveIntegerField()
    reasoning = models.TextField()
    date = models.DateField()
    authorized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.service_hours} hours on {self.date} | {self.reasoning}"
