from django.db import models
from django.utils.text import slugify
from django.conf import settings
from accounts.models import Company, User

class Field(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return ('{}'.format(self.name))

class Job(models.Model):
    """
    Author: Daking Rai (daking.rai@infodevelopers.com.np)
    Date: July 05, 2018
    """
    
    title = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    responsibilities = models.TextField(null=True, blank=True)
    qualification = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=500, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    no_opening = models.IntegerField(null= True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)

    type_of_job = models.CharField(max_length=100)
    job_field = models.ForeignKey(Field, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    is_featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    tags = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'job'
        verbose_name_plural = 'jobs'

    def __str__(self):
        return ('{}'.format(self.title))

    def save(self, **kwargs):
        slug_str = "%s %s %s" % (self.title, self.company.user.username,self.created_at)
        self.slug = slugify(self, slug_str)
        super(Job, self).save(**kwargs)



class Applicant (models.Model):
    job = models.ForeignKey(Job, on_delete= models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="uploads/resume/%Y/%m/%d/")
    date_applied = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return ('{}{}'.format(self.applicant.username, self.job.title))
