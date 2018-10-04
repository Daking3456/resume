from django.contrib import admin
from job.models import Field, Job, Applicant, ParsedResume

# Register your models here.

admin.site.register(Field)
admin.site.register(Job)
admin.site.register(Applicant)
admin.site.register(ParsedResume)