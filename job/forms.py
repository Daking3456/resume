from django import forms
from job.models import Job
from datetimewidget.widgets import DateTimeWidget

class JobForm(forms.Form):
    title = forms.CharField(max_length=1000)
    responsibilities = forms.CharField(max_length=10000)
    qualification = forms.CharField(max_length=10000)
    education = forms.CharField(max_length=1000)
    description = forms.CharField(max_length=10000)
    requirements = forms.CharField(max_length=10000)
    salary = forms.IntegerField()
    no_opening = forms.IntegerField()
    type_of_job = forms.CharField(max_length=100)
    deadline = forms.DateTimeField(widget=DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3))

class JobModelForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['slug','is_featured','created_at','status','company']


