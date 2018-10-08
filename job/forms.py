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


from haystack.forms import FacetedSearchForm


class FacetedProductSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):

        data = dict(kwargs.get("data", []))
        self.type_of_job = data.get('type_of_job',[])
        self.industry = data.get('industry', [])
        self.contract_type = data.get('contract_type', [])
        self.level_of_job = data.get('level_of_job', [])
        self.experience = data.get('experience', [])

        super(FacetedProductSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedProductSearchForm, self).search()
        if self.type_of_job:
            query = None
            for type_of_job in self.type_of_job:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(type_of_job)
            sqs = sqs.narrow(u'category_exact:%s' % query)
        
        if self.industry:
            query = None
            for industry in self.industry:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(industry)
            sqs = sqs.narrow(u'category_exact:%s' % query)
        
        if self.contract_type:
            query = None
            for contract_type in self.contract_type:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(contract_type)
            sqs = sqs.narrow(u'category_exact:%s' % query)
       
        if self.level_of_job:
            query = None
            for level_of_job in self.level_of_job:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(level_of_job)
            sqs = sqs.narrow(u'category_exact:%s' % query)

        if self.experience:
            query = None
            for experience in self.experience:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(experience)
            sqs = sqs.narrow(u'category_exact:%s' % query)


        return sqs


