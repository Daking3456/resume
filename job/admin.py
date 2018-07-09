from django.contrib import admin
from job.models import Field, Job, Applicant

# Register your models here.

admin.site.register(Field)
admin.site.register(Job)
admin.site.register(Applicant)