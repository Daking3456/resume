from django import forms
from job.models import Job

class JobForm(forms.Form):
    title = forms.CharField(max_length=1000)
    responsibilities = forms.CharField(max_length=10000)
    qualification = forms.CharField(max_length=10000)
    education = forms.CharField(max_length=1000)
    salary = forms.IntegerField()
    no_opening = forms.IntegerField()


