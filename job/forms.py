from django import forms
from job.models import Job, Applicant, ParsedResume
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


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'
        exlude = ['job', 'applicant']


class ParsedResumeForm(forms.ModelForm):
    class Meta:
        model = ParsedResume
        fields = '__all__'


# from haystack.forms import FacetedSearchForm


# class FacetedProductSearchForm(FacetedSearchForm):

#     def __init__(self, *args, **kwargs):
#         data = dict(kwargs.get("data", []))
#         self.categories = data.get('category', [])
#         self.brands = data.get('brand', [])
#         # self.job_types = data.get('job_type', [])
#         self.experiences = data.get('experience', [])
#         self.salary = data.get

#         super(FacetedProductSearchForm, self).__init__(*args, **kwargs)

#     def search(self):
#         sqs = super(FacetedProductSearchForm, self).search()
#         if self.categories:
#             query = None
#             for category in self.categories:
#                 if query:
#                     query += u' OR '
#                 else:
#                     query = u''
#                 query += u'"%s"' % sqs.query.clean(category)
#             sqs = sqs.narrow(u'category_exact:%s' % query)
#         # if self.brands:
#         #     query = None
#         #     for brand in self.brands:
#         #         if query:
#         #             query += u' OR '
#         #         else:
#         #             query = u''
#         #         query += u'"%s"' % sqs.query.clean(brand)
#         # #     sqs = sqs.narrow(u'brand_exact:%s' % query)
#         # if self.job_types:
#         #     query = None
#         #     for job_type in self.job_types:
#         #         if query:
#         #             query += u' OR '
#         #         else:
#         #             query = u''
#         #         query += u'"%s"' % sqs.query.clean(job_type)
#         #     sqs = sqs.narrow(u'job_type_exact:%s' % query)
#         #    # sqs = sqs.narrow(u'brand_exact:%s' % query)
#         # if self.experiences:
#         #     query = None
#         #     for experience in self.experiences:
#         #         if query:
#         #             query += u' OR '
#         #         else:
#         #             query = u''
#         #         query += u'"%s"' % sqs.query.clean(experience)
#         #     sqs = sqs.narrow(u'experience_exact:%s' % query)
#         return sqs


